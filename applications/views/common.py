from http import HTTPStatus

from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from applications.forms.application_actions import withdraw_application_confirmation, surrender_application_confirmation
from applications.forms.common import (
    respond_to_query_form,
    ecju_query_respond_confirmation_form,
    edit_type_form,
    application_success_page,
    application_copy_form,
    exhibition_details_form,
    declaration_form,
)
from applications.helpers.check_your_answers import (
    convert_application_to_check_your_answers,
    _convert_goods_categories,
    get_application_type_string,
)
from applications.helpers.summaries import draft_summary
from applications.helpers.task_list_sections import get_reference_number_description
from applications.helpers.task_lists import get_application_task_list
from applications.helpers.validators import (
    validate_withdraw_application,
    validate_delete_draft,
    validate_surrender_application_and_update_case_status,
)
from applications.services import (
    get_activity,
    get_applications,
    get_case_notes,
    get_case_generated_documents,
    get_application_ecju_queries,
    get_ecju_query,
    put_ecju_query,
    post_case_notes,
    submit_application,
    get_application,
    set_application_status,
    get_status_properties,
    copy_application,
    post_exhibition,
)
from conf.constants import HMRC, APPLICANT_EDITING, NotificationType, STANDARD, OPEN
from core.helpers import str_to_bool, convert_dict_to_query_params
from core.services import get_organisation
from lite_content.lite_exporter_frontend import strings
from lite_forms.components import HiddenField
from lite_forms.generators import confirm_form
from lite_forms.generators import error_page, form_page
from lite_forms.views import SingleFormView, MultiFormView


class ApplicationsList(TemplateView):
    def get(self, request, **kwargs):
        params = {"page": int(request.GET.get("page", 1)), "submitted": str_to_bool(request.GET.get("submitted", True))}
        organisation = get_organisation(request, request.user.organisation)
        applications = get_applications(request, **params)

        context = {
            "applications": applications,
            "organisation": organisation,
            "params": params,
            "page": params.pop("page"),
            "params_str": convert_dict_to_query_params(params),
        }
        return render(
            request, "applications/applications.html" if params["submitted"] else "applications/drafts.html", context
        )


class DeleteApplication(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        application = get_application(request, self.object_pk)
        self.form = confirm_form(
            title=strings.applications.DeleteApplicationPage.TITLE,
            confirmation_name="choice",
            summary=draft_summary(application),
            back_link_text=strings.applications.DeleteApplicationPage.BACK_TEXT,
            yes_label=strings.applications.DeleteApplicationPage.YES_LABEL,
            no_label=strings.applications.DeleteApplicationPage.NO_LABEL,
            submit_button_text=strings.applications.DeleteApplicationPage.SUBMIT_BUTTON,
            back_url=request.GET.get("return_to"),
            side_by_side=True,
        )
        self.action = validate_delete_draft

    def get_success_url(self):
        if self.get_validated_data().get("status"):
            return reverse_lazy("applications:applications") + "?submitted=False"
        else:
            return self.request.GET.get("return_to")


class ApplicationEditType(TemplateView):
    def get(self, request, **kwargs):
        application_id = str(kwargs["pk"])
        data = get_application(request, application_id)

        if data.get("status") and data.get("status").get("key") == APPLICANT_EDITING:
            return redirect(reverse_lazy("applications:task_list", kwargs={"pk": application_id}))

        return form_page(request, edit_type_form(application_id))

    def post(self, request, **kwargs):
        application_id = str(kwargs["pk"])
        edit_type = request.POST.get("edit-type")

        if edit_type == "major":
            data, status_code = set_application_status(request, str(kwargs["pk"]), APPLICANT_EDITING)

            if status_code != HTTPStatus.OK:
                return form_page(request, edit_type_form(str(kwargs["pk"])), errors=data)

        elif edit_type is None:
            return form_page(
                request,
                edit_type_form(application_id),
                errors={"edit-type": ["Select the type of edit you need to make"]},
            )

        return redirect(reverse_lazy("applications:task_list", kwargs={"pk": str(kwargs["pk"])}))


class ApplicationTaskList(TemplateView):
    def get(self, request, **kwargs):
        application = get_application(request, kwargs["pk"])
        return get_application_task_list(request, application)

    def post(self, request, **kwargs):
        application_id = str(kwargs["pk"])
        application = get_application(request, str(kwargs["pk"]))

        data, status_code = submit_application(request, application_id)

        if status_code != HTTPStatus.OK:
            return get_application_task_list(request, application, errors=data.get("errors"))

        if application.sub_type not in [NotificationType.EUA, NotificationType.GOODS]:
            # All other application types direct to the summary page
            return HttpResponseRedirect(reverse_lazy("applications:summary", kwargs={"pk": application_id}))
        else:
            # Redirect to the success page to prevent the user going back after the Post
            # Follows this pattern: https://en.wikipedia.org/wiki/Post/Redirect/Get
            return HttpResponseRedirect(reverse_lazy("applications:success_page", kwargs={"pk": application_id}))


class ApplicationDetail(TemplateView):
    application_id = None
    application = None
    case_id = None
    view_type = None

    def dispatch(self, request, *args, **kwargs):
        self.application_id = str(kwargs["pk"])
        self.application = get_application(request, self.application_id)
        self.case_id = self.application["case"]
        self.view_type = kwargs.get("type")

        return super(ApplicationDetail, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        status_props, _ = get_status_properties(request, self.application["status"]["key"])

        context = {
            "case_id": self.application_id,
            "application": self.application,
            "type": self.view_type,
            "answers": {**convert_application_to_check_your_answers(self.application)},
            "status_is_read_only": status_props["is_read_only"],
            "status_is_terminal": status_props["is_terminal"],
            "errors": kwargs.get("errors"),
            "text": kwargs.get("text", ""),
        }

        context["activity"] = get_activity(request, self.application_id) or {}

        if self.application.sub_type != HMRC:
            if self.view_type == "case-notes":
                context["notes"] = get_case_notes(request, self.case_id)["case_notes"]

            if self.view_type == "ecju-queries":
                context["open_queries"], context["closed_queries"] = get_application_ecju_queries(request, self.case_id)

        if self.view_type == "generated-documents":
            generated_documents, _ = get_case_generated_documents(request, self.application_id)
            context["generated_documents"] = generated_documents["results"]

        return render(request, "applications/application.html", context)

    def post(self, request, **kwargs):
        if self.view_type != "case-notes":
            return Http404

        response, _ = post_case_notes(request, self.case_id, request.POST)

        if "errors" in response:
            return self.get(request, error=response["errors"], text=request.POST.get("text"), **kwargs)

        return redirect(
            reverse_lazy("applications:application", kwargs={"pk": self.application_id, "type": "case-notes"})
        )


class ApplicationSummary(TemplateView):
    application_id = None
    application = None
    case_id = None
    view_type = None

    def dispatch(self, request, *args, **kwargs):
        self.application_id = str(kwargs["pk"])
        self.application = get_application(request, self.application_id)
        self.case_id = self.application["case"]

        return super(ApplicationSummary, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):

        context = {
            "case_id": self.application_id,
            "application": self.application,
            "answers": {**convert_application_to_check_your_answers(self.application, summary=True)},
            "summary_page": True,
        }

        context["application_type"] = get_application_type_string(self.application)
        if self.application.sub_type != HMRC:
            context["notes"] = get_case_notes(request, self.case_id)["case_notes"]
            if self.application.sub_type == OPEN:
                context["reference_code"] = get_reference_number_description(self.application)
                context["contains_firearm_goods"] = self.application["contains_firearm_goods"]

        return render(request, "applications/application.html", context)

    def post(self, request, **kwargs):
        # As it's the summary page, either attempt to submit the application (if of type HMRC)
        # or proceed to the declaration page
        if self.application.sub_type == HMRC:
            data, status_code = submit_application(request, self.application_id, json={"submit_hmrc": True})
            if status_code != HTTPStatus.OK:
                return get_application_task_list(request, self.application, errors=data.get("errors"))

            return HttpResponseRedirect(reverse_lazy("applications:success_page", kwargs={"pk": self.application_id}))
        else:
            return HttpResponseRedirect(reverse_lazy("applications:declaration", kwargs={"pk": self.application_id}))


class RespondToQuery(TemplateView):
    application_id = None
    ecju_query_id = None
    ecju_query = None

    def dispatch(self, request, *args, **kwargs):
        self.application_id = str(kwargs["pk"])
        self.ecju_query_id = str(kwargs["query_pk"])
        self.ecju_query = get_ecju_query(request, str(kwargs["pk"]), str(kwargs["query_pk"]))

        if self.ecju_query["response"]:
            return redirect(
                reverse_lazy("applications:application", kwargs={"pk": self.application_id, "type": "ecju-queries"})
            )

        return super(RespondToQuery, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        """
        Will get a text area form for the user to respond to the ecju_query
        """
        return form_page(request, respond_to_query_form(self.application_id, self.ecju_query))

    def post(self, request, **kwargs):
        """
        will determine what form the user is on:
        if the user is on the input form will then will determine if data is valid, and move user to confirmation form
        else will allow the user to confirm they wish to respond and post data if accepted.
        """
        form_name = request.POST.get("form_name")

        if form_name == "respond_to_query":
            # Post the form data to API for validation only
            data = {"response": request.POST.get("response"), "validate_only": True}
            response, status_code = put_ecju_query(request, self.application_id, self.ecju_query_id, data)

            if status_code != HTTPStatus.OK:
                errors = response.get("errors")
                errors = {error: message for error, message in errors.items()}
                form = respond_to_query_form(self.application_id, self.ecju_query)
                data = {"response": request.POST.get("response")}
                return form_page(request, form, data=data, errors=errors)
            else:
                form = ecju_query_respond_confirmation_form(
                    reverse_lazy(
                        "applications:respond_to_query",
                        kwargs={"pk": self.application_id, "query_pk": self.ecju_query_id},
                    )
                )
                form.questions.append(HiddenField("response", request.POST.get("response")))
                return form_page(request, form)
        elif form_name == "ecju_query_response_confirmation":
            if request.POST.get("confirm_response") == "yes":
                data, status_code = put_ecju_query(request, self.application_id, self.ecju_query_id, request.POST)

                if "errors" in data:
                    return form_page(
                        request,
                        respond_to_query_form(self.application_id, self.ecju_query),
                        data=request.POST,
                        errors=data["errors"],
                    )

                return redirect(
                    reverse_lazy("applications:application", kwargs={"pk": self.application_id, "type": "ecju-queries"})
                )
            elif request.POST.get("confirm_response") == "no":
                return form_page(
                    request, respond_to_query_form(self.application_id, self.ecju_query), data=request.POST
                )
            else:
                error = {"required": ["This field is required"]}
                form = ecju_query_respond_confirmation_form(
                    reverse_lazy(
                        "applications:respond_to_query",
                        kwargs={"pk": self.application_id, "query_pk": self.ecju_query_id},
                    )
                )
                form.questions.append(HiddenField("response", request.POST.get("response")))
                return form_page(request, form, errors=error)
        else:
            # Submitted data does not contain an expected form field - return an error
            return error_page(request, strings.applications.AttachDocumentPage.UPLOAD_GENERIC_ERROR)


class WithdrawApplication(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        application = get_application(request, self.object_pk)
        self.form = withdraw_application_confirmation(application, self.object_pk)
        self.action = validate_withdraw_application
        self.success_url = reverse_lazy("applications:application", kwargs={"pk": self.object_pk})


class SurrenderApplication(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        application = get_application(request, self.object_pk)
        self.form = surrender_application_confirmation(application, self.object_pk)
        self.action = validate_surrender_application_and_update_case_status
        self.success_url = reverse_lazy("applications:application", kwargs={"pk": self.object_pk})


class Notes(TemplateView):
    def get(self, request, **kwargs):
        application_id = str(kwargs["pk"])
        application = get_application(request, application_id)
        notes = get_case_notes(request, application_id)["case_notes"]

        context = {
            "application": application,
            "notes": notes,
            "post_url": reverse_lazy("applications:notes", kwargs={"pk": application_id}),
            "error": kwargs.get("error"),
            "text": kwargs.get("text", ""),
        }
        return render(request, "applications/case-notes.html", context)

    def post(self, request, **kwargs):
        application_id = str(kwargs["pk"])
        response, _ = post_case_notes(request, application_id, request.POST)

        if "errors" in response:
            return self.get(request, error=response["errors"]["text"][0], text=request.POST.get("text"), **kwargs)

        return redirect(reverse_lazy("applications:notes", kwargs={"pk": application_id}))


class CheckYourAnswers(TemplateView):
    def get(self, request, **kwargs):
        application_id = kwargs["pk"]
        application = get_application(request, application_id)

        context = {"application": application, "answers": {**convert_application_to_check_your_answers(application)}}
        return render(request, "applications/check-your-answers.html", context)


class Submit(TemplateView):
    def get(self, request, **kwargs):
        application_id = kwargs["pk"]
        application = get_application(request, application_id)

        context = {
            "application": application,
        }
        return render(request, "applications/submit.html", context)


class ApplicationSubmitSuccessPage(TemplateView):
    def get(self, request, **kwargs):
        """
        Display application submit success page
        This page is accessed one of two ways:
        1. Successful submission of an application
        2. From a bookmark or link - this is intentional as some users will want to
           save the page as evidence
        """
        application_id = kwargs["pk"]
        application = get_application(request, application_id)

        if application.status in ["draft", "applicant_editing"]:
            raise Http404

        return application_success_page(request, application["reference_code"])


class ApplicationCopy(MultiFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        application = get_application(request, self.object_pk)
        self.forms = application_copy_form(application.sub_type)
        self.action = copy_application

    def get_success_url(self):
        id = self.get_validated_data()["data"]
        return reverse_lazy("applications:task_list", kwargs={"pk": id})


class ExhibitionDetail(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        self.data = get_application(request, self.object_pk)
        self.form = exhibition_details_form(self.object_pk)
        self.action = post_exhibition

    def get_data(self):
        data = self.data
        date_fields = ["first_exhibition_date", "required_by_date"]
        for field in date_fields:
            if data.get(field, False):
                date_split = data[field].split("-")
                data[field + "year"], data[field + "month"], data[field + "day"] = date_split
        return data

    def get_success_url(self):
        return reverse_lazy("applications:task_list", kwargs={"pk": self.object_pk})


class ApplicationDeclaration(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        self.form = declaration_form(self.object_pk)
        self.action = submit_application

    def get_success_url(self):
        return reverse_lazy("applications:success_page", kwargs={"pk": self.object_pk})
