from http import HTTPStatus

from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from applications.forms.common import (
    respond_to_query_form,
    ecju_query_respond_confirmation_form,
    edit_type_form,
    application_success_page,
)
from applications.helpers.check_your_answers import convert_application_to_check_your_answers
from applications.helpers.summaries import application_summary, draft_summary
from applications.helpers.task_lists import get_application_task_list
from applications.helpers.validators import validate_withdraw_application, validate_delete_draft
from applications.services import (
    get_applications,
    get_case_notes,
    get_application_ecju_queries,
    get_ecju_query,
    put_ecju_query,
    post_application_case_notes,
    submit_application,
    get_application,
    set_application_status,
    get_status_properties,
    get_application_generated_documents,
)
from conf.constants import HMRC_QUERY, APPLICANT_EDITING, NEWLINE, CASE_NOTE, ECJU_QUERY, GENERATED_CASE_DOCUMENT
from core.helpers import group_notifications, str_to_bool, convert_dict_to_query_params
from core.services import get_notifications, get_organisation
from lite_content.lite_exporter_frontend import strings
from lite_forms.components import HiddenField
from lite_forms.generators import confirm_form
from lite_forms.generators import error_page, form_page
from lite_forms.views import SingleFormView


class ApplicationsList(TemplateView):
    def get(self, request, **kwargs):
        params = {"page": int(request.GET.get("page", 1)), "submitted": str_to_bool(request.GET.get("submitted", True))}
        organisation = get_organisation(request, request.user.organisation)
        applications = get_applications(request, **params)
        notifications = get_notifications(request, unviewed=True)

        context = {
            "applications": applications,
            "notifications": group_notifications(notifications),
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
            back_url=reverse_lazy("applications:application", kwargs={"pk": self.object_pk}),
            side_by_side=True,
        )
        self.return_to = request.GET.get("return_to")
        self.action = validate_delete_draft
        self.success_url = reverse_lazy("applications:applications") + "?submitted=False"

    def get_success_url(self):
        if self.return_to == "application" and self.get_validated_data().get("choice") == "no":
            return reverse_lazy("applications:task_list", kwargs={"pk": self.object_pk})
        else:
            return reverse_lazy("applications:applications") + "?submitted=False"


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
                errors={"edit-type": ["Select what type of edit you'd like to make."]},
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

        return application_success_page(request, application_id)


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
        # add application number to next query
        notifications = get_notifications(request, unviewed=True)
        (
            case_note_notifications,
            ecju_query_notifications,
            generated_case_document_notifications,
        ) = _get_separate_notifications(notifications, self.application_id)

        status_props, _ = get_status_properties(request, self.application["status"]["key"])

        context = {
            "application": self.application,
            "title": self.application["name"],
            "type": self.view_type,
            "case_note_notifications": case_note_notifications,
            "ecju_query_notifications": ecju_query_notifications,
            "generated_case_document_notifications": generated_case_document_notifications,
            "answers": {**convert_application_to_check_your_answers(self.application)},
            "status_is_read_only": status_props["is_read_only"],
            "status_is_terminal": status_props["is_terminal"],
        }

        if self.application["application_type"]["key"] != HMRC_QUERY:
            if self.view_type == "case-notes":
                context["notes"] = get_case_notes(request, self.case_id)["case_notes"]

            if self.view_type == "ecju-queries":
                context["open_queries"], context["closed_queries"] = get_application_ecju_queries(request, self.case_id)

        if self.view_type == "generated-documents":
            context["generated_documents"] = get_application_generated_documents(request, self.application_id)

        return render(request, "applications/application.html", context)

    def post(self, request, **kwargs):
        if self.view_type != "case-notes":
            return Http404

        response, _ = post_application_case_notes(request, self.case_id, request.POST)

        if "errors" in response:
            errors = response.get("errors")
            if errors.get("text"):
                error = errors.get("text")[0]
                error = error.replace("This field", "Case note")
                error = error.replace("this field", "the case note")  # TODO: Move to API

            else:
                error_list = []
                for key in errors:
                    error_list.append("{field}: {error}".format(field=key, error=errors[key][0]))
                error = NEWLINE.join(error_list)
            return error_page(request, error)

        return redirect(
            reverse_lazy("applications:application", kwargs={"pk": self.application_id, "type": "case-notes"})
        )


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
            return error_page(request, strings.UPLOAD_GENERIC_ERROR)


class WithdrawApplication(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        application = get_application(request, self.object_pk)
        self.form = confirm_form(
            title=strings.applications.ApplicationSummaryPage.Withdraw.TITLE,
            confirmation_name="choice",
            summary=application_summary(application),
            back_link_text=strings.applications.ApplicationSummaryPage.Withdraw.BACK_TEXT,
            yes_label=strings.applications.ApplicationSummaryPage.Withdraw.YES_LABEL,
            no_label=strings.applications.ApplicationSummaryPage.Withdraw.NO_LABEL,
            submit_button_text=strings.applications.ApplicationSummaryPage.Withdraw.SUBMIT_BUTTON,
            back_url=reverse_lazy("applications:application", kwargs={"pk": self.object_pk}),
            side_by_side=True,
        )
        self.action = validate_withdraw_application
        self.success_url = reverse_lazy("applications:application", kwargs={"pk": self.object_pk})


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


def _get_separate_notifications(notifications, application_id):
    case_note_notifications = 0
    ecju_query_notifications = 0
    generated_case_document_notifications = 0

    for notification in notifications:
        if notification["parent"] == application_id:
            if notification["object_type"] == CASE_NOTE:
                case_note_notifications += 1
            elif notification["object_type"] == ECJU_QUERY:
                ecju_query_notifications += 1
            elif notification["object_type"] == GENERATED_CASE_DOCUMENT:
                generated_case_document_notifications += 1

    return case_note_notifications, ecju_query_notifications, generated_case_document_notifications
