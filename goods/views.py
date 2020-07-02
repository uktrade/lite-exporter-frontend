from http import HTTPStatus

from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from s3chunkuploader.file_handler import S3FileUploadHandler

from applications.services import (
    get_application_ecju_queries,
    get_case_notes,
    post_case_notes,
    get_ecju_query,
    put_ecju_query,
    add_document_data,
    download_document_from_s3,
    get_status_properties,
    get_case_generated_documents,
)
from goods.forms import (
    attach_documents_form,
    delete_good_form,
    document_grading_form,
    raise_a_goods_query,
    add_good_form_group,
    edit_good_detail_form,
    edit_grading_form,
    product_military_use_form,
    product_component_form,
    product_uses_information_security,
    software_technology_details_form,
)
from goods.helpers import COMPONENT_SELECTION_TO_DETAIL_FIELD_MAP, return_to_good_summary
from goods.services import (
    get_goods,
    post_goods,
    get_good,
    edit_good,
    delete_good,
    get_good_documents,
    get_good_document,
    post_good_documents,
    delete_good_document,
    raise_goods_query,
    post_good_document_sensitivity,
    validate_good,
    edit_good_pv_grading,
    edit_good_details,
    get_good_details,
)
from lite_content.lite_exporter_frontend import strings, goods
from lite_content.lite_exporter_frontend.goods import AttachDocumentForm
from lite_forms.components import HiddenField, BackLink, FiltersBar, TextInput
from lite_forms.generators import error_page, form_page
from lite_forms.views import SingleFormView, MultiFormView


class Goods(TemplateView):
    def get(self, request, **kwargs):
        description = request.GET.get("description", "").strip()
        part_number = request.GET.get("part_number", "").strip()
        control_list_entry = request.GET.get("control_list_entry", "").strip()

        filters = FiltersBar(
            [
                TextInput(title="description", name="description"),
                TextInput(title="control list entry", name="control_list_entry"),
                TextInput(title="part number", name="part_number"),
            ]
        )

        params = {
            "page": int(request.GET.get("page", 1)),
            "description": description,
            "part_number": part_number,
            "control_list_entry": control_list_entry,
        }

        context = {
            "goods": get_goods(request, **params),
            "description": description,
            "part_number": part_number,
            "control_list_entry": control_list_entry,
            "filters": filters,
        }
        return render(request, "goods/goods.html", context)


class GoodsDetailEmpty(TemplateView):
    def get(self, request, **kwargs):
        return redirect(reverse_lazy("goods:good_detail", kwargs={"pk": kwargs["pk"], "type": "case-notes"}))


class GoodsDetail(TemplateView):
    good_id = None
    good = None
    view_type = None

    def dispatch(self, request, *args, **kwargs):
        self.good_id = str(kwargs["pk"])
        self.good = get_good(request, self.good_id, full_detail=True)[0]
        self.view_type = kwargs["type"]

        if self.view_type not in ["case-notes", "ecju-queries", "ecju-generated-documents"]:
            return Http404

        return super(GoodsDetail, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        documents = get_good_documents(request, str(self.good_id))

        context = {
            "good": self.good,
            "documents": documents,
            "type": self.view_type,
            "error": kwargs.get("error"),
            "text": kwargs.get("text", ""),
        }

        if self.good["query"]:
            context["case_id"] = self.good["query"]["id"]
            status_props, _ = get_status_properties(request, self.good["case_status"]["key"])
            context["status_is_read_only"] = status_props["is_read_only"]
            context["status_is_terminal"] = status_props["is_terminal"]

            if self.view_type == "ecju-generated-documents":
                generated_documents, _ = get_case_generated_documents(request, self.good["query"]["id"])
                context["generated_documents"] = generated_documents["results"]

        if self.view_type == "case-notes":
            if self.good.get("case_id"):
                case_notes = get_case_notes(request, self.good["case_id"])["case_notes"]
                context["notes"] = filter(lambda note: note["is_visible_to_exporter"], case_notes)

        if self.view_type == "ecju-queries":
            context["open_queries"], context["closed_queries"] = get_application_ecju_queries(
                request, self.good["case_id"]
            )

        return render(request, "goods/good.html", context)

    def post(self, request, **kwargs):
        if self.view_type != "case-notes":
            return Http404

        good_id = kwargs["pk"]
        data, _ = get_good(request, str(good_id), full_detail=True)

        response, _ = post_case_notes(request, data["case_id"], request.POST)

        if "errors" in response:
            return self.get(request, error=response["errors"]["text"][0], text=request.POST.get("text"), **kwargs)

        return redirect(reverse_lazy("goods:good_detail", kwargs={"pk": good_id, "type": "case-notes"}))


class AddGood(MultiFormView):
    def init(self, request, **kwargs):
        self.forms = add_good_form_group(request)
        self.action = validate_good

    def on_submission(self, request, **kwargs):
        copied_request = request.POST.copy()
        is_pv_graded = copied_request.get("is_pv_graded", "").lower() == "yes"
        is_software_technology = copied_request.get("item_category") in ["group3_software", "group3_technology"]
        self.forms = add_good_form_group(request, is_pv_graded, is_software_technology)

        if is_pv_graded:
            # post on step 5 in both software/technology and group 1
            if int(self.request.POST.get("form_pk")) == 5:
                self.action = post_goods
        else:
            # post on step 4 in both software/technology and group 1
            if int(self.request.POST.get("form_pk")) == 4:
                self.action = post_goods

    def get_success_url(self):
        return reverse_lazy("goods:add_document", kwargs={"pk": self.get_validated_data()["good"]["id"]})


class GoodSoftwareTechnology(SingleFormView):
    application_id = None

    def init(self, request, **kwargs):
        if "good_pk" in kwargs:
            # coming from the application
            self.object_pk = str(kwargs["good_pk"])
            self.application_id = str(kwargs["pk"])
        else:
            self.object_pk = str(kwargs["pk"])
        self.data = get_good_details(request, self.object_pk)[0]
        self.form = software_technology_details_form(request, self.data.get("item_category"))
        self.action = edit_good_details

    def get_data(self):
        return {
            "software_or_technology_details": self.data.get("software_or_technology_details"),
        }

    def get_success_url(self):
        good = get_good(self.request, self.object_pk, full_detail=True)[0]
        # Next question military use
        if not good.get("is_military_use"):
            if "good_pk" in self.kwargs:
                return reverse_lazy(
                    "applications:good_military_use", kwargs={"pk": self.application_id, "good_pk": self.object_pk}
                )
            else:
                return reverse_lazy("goods:good_military_use", kwargs={"pk": self.object_pk})
        # Edit
        else:
            return return_to_good_summary(self.kwargs, self.application_id, self.object_pk)


class GoodMilitaryUse(SingleFormView):
    application_id = None

    def init(self, request, **kwargs):
        if "good_pk" in kwargs:
            # coming from the application
            self.object_pk = str(kwargs["good_pk"])
            self.application_id = str(kwargs["pk"])
        else:
            self.object_pk = str(kwargs["pk"])
        self.data = get_good_details(request, self.object_pk)[0]
        self.form = product_military_use_form(request)
        self.action = edit_good_details

    def get_data(self):
        new_data = {
            "is_military_use": self.data.get("is_military_use"),
            "modified_military_use_details": self.data.get("modified_military_use_details"),
        }
        return new_data

    def get_success_url(self):
        good = get_good(self.request, self.object_pk, full_detail=True)[0]
        is_software_technology = good.get("item_category")["key"] in ["group3_software", "group3_technology"]
        # Next question information security if good is software/hardware
        if is_software_technology:
            if good.get("uses_information_security") is None:
                if "good_pk" in self.kwargs:
                    return reverse_lazy(
                        "applications:good_information_security",
                        kwargs={"pk": self.application_id, "good_pk": self.object_pk},
                    )
                else:
                    return reverse_lazy("goods:good_information_security", kwargs={"pk": self.object_pk})
        # Next question good component if good is in category 1
        if not good.get("is_component") and not is_software_technology:
            if "good_pk" in self.kwargs:
                return reverse_lazy(
                    "applications:good_component", kwargs={"pk": self.application_id, "good_pk": self.object_pk}
                )
            else:
                return reverse_lazy("goods:good_component", kwargs={"pk": self.object_pk})
        # Edit
        else:
            return return_to_good_summary(self.kwargs, self.application_id, self.object_pk)


class GoodComponent(SingleFormView):
    application_id = None

    def init(self, request, **kwargs):
        if "good_pk" in kwargs:
            # coming from the application
            self.object_pk = str(kwargs["good_pk"])
            self.application_id = str(kwargs["pk"])
        else:
            self.object_pk = str(kwargs["pk"])
        self.data = get_good_details(request, self.object_pk)[0]
        self.form = product_component_form(request)
        self.action = edit_good_details

    def get_data(self):
        if self.data.get("is_component") and self.data.get("component_details"):
            detail_field = COMPONENT_SELECTION_TO_DETAIL_FIELD_MAP[self.data["is_component"]]
            self.data[detail_field] = self.data["component_details"]
            return {"is_component": self.data.get("is_component"), detail_field: self.data.get(detail_field)}
        return {"is_component": self.data.get("is_component")}

    def get_success_url(self):
        good = get_good(self.request, self.object_pk, full_detail=True)[0]
        # Next question information security - boolean
        if good.get("uses_information_security") is None:
            if "good_pk" in self.kwargs:
                return reverse_lazy(
                    "applications:good_information_security",
                    kwargs={"pk": self.application_id, "good_pk": self.object_pk},
                )
            else:
                return reverse_lazy("goods:good_information_security", kwargs={"pk": self.object_pk})
        # Edit
        else:
            return return_to_good_summary(self.kwargs, self.application_id, self.object_pk)


class GoodInformationSecurity(SingleFormView):
    application_id = None

    def init(self, request, **kwargs):
        if "good_pk" in kwargs:
            # coming from the application
            self.object_pk = str(kwargs["good_pk"])
            self.application_id = str(kwargs["pk"])
        else:
            self.object_pk = str(kwargs["pk"])
        self.data = get_good_details(request, self.object_pk)[0]
        self.form = product_uses_information_security(request)
        self.action = edit_good_details

    def get_data(self):
        new_data = {
            "uses_information_security": self.data.get("uses_information_security"),
            "information_security_details": self.data.get("information_security_details"),
        }
        return new_data

    def get_success_url(self):
        # Return to the application add good summary if adding/editing good from the application
        if "good_pk" in self.kwargs:
            return reverse_lazy(
                "applications:add_good_summary", kwargs={"pk": self.application_id, "good_pk": self.object_pk}
            )
        else:
            return reverse_lazy("goods:good", kwargs={"pk": self.object_pk})


class RaiseGoodsQuery(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = str(kwargs["pk"])
        good, _ = get_good(request, self.object_pk)

        raise_a_clc_query = "unsure" == good["is_good_controlled"]["key"]
        raise_a_pv_query = "grading_required" == good["is_pv_graded"]["key"]

        self.form = raise_a_goods_query(self.object_pk, raise_a_clc_query, raise_a_pv_query)
        self.action = raise_goods_query
        self.success_url = reverse_lazy("goods:good", kwargs={"pk": self.object_pk})


class EditGood(SingleFormView):
    application_id = None

    def init(self, request, **kwargs):
        if "good_pk" in kwargs:
            # coming from the application
            self.object_pk = str(kwargs["good_pk"])
            self.application_id = str(kwargs["pk"])
        else:
            self.object_pk = str(kwargs["pk"])
        self.data = get_good(request, self.object_pk)[0]
        self.form = edit_good_detail_form(request, self.object_pk)
        self.action = edit_good

    def get_data(self):
        self.data["control_list_entries"] = [
            {"key": clc["rating"], "value": clc["rating"]} for clc in self.data["control_list_entries"]
        ]
        return self.data

    def get_success_url(self):
        # Return to the application add good summary if adding good from the application
        if "good_pk" in self.kwargs:
            return reverse_lazy(
                "applications:add_good_summary", kwargs={"pk": self.application_id, "good_pk": self.object_pk}
            )
        else:
            return reverse_lazy("goods:good", kwargs={"pk": self.object_pk})


class EditGrading(SingleFormView):
    application_id = None

    def init(self, request, **kwargs):
        if "good_pk" in kwargs:
            # coming from the application
            self.object_pk = str(kwargs["good_pk"])
            self.application_id = str(kwargs["pk"])
        else:
            self.object_pk = str(kwargs["pk"])
        self.data = get_good(request, self.object_pk)[0]
        self.form = edit_grading_form(request, self.object_pk)
        self.action = edit_good_pv_grading

    def get_data(self):
        data = self.data
        if data.get("pv_grading_details", False):
            for k, v in data["pv_grading_details"].items():
                data[k] = v
            date_of_issue = data["date_of_issue"].split("-")
            data["date_of_issueday"] = date_of_issue[2]
            data["date_of_issuemonth"] = date_of_issue[1]
            data["date_of_issueyear"] = date_of_issue[0]

        return data

    def get_success_url(self):
        if "good_pk" in self.kwargs:
            return reverse_lazy(
                "applications:add_good_summary", kwargs={"pk": self.application_id, "good_pk": self.object_pk}
            )
        good = get_good(self.request, self.object_pk, full_detail=True)[0]

        raise_a_clc_query = "unsure" == good["is_good_controlled"]["key"]
        raise_a_pv_query = "grading_required" == good["is_pv_graded"]["key"]

        if not good.get("documents") and not good.get("missing_document_reason"):
            return reverse_lazy("goods:add_document", kwargs={"pk": self.object_pk})
        elif raise_a_clc_query or raise_a_pv_query:
            return reverse_lazy("goods:raise_goods_query", kwargs={"pk": self.object_pk})
        else:
            return reverse_lazy("goods:good", kwargs={"pk": self.object_pk})


class DeleteGood(TemplateView):
    def get(self, request, **kwargs):
        data, _ = get_good(request, str(kwargs["pk"]))
        return form_page(request, delete_good_form(data))

    def post(self, request, **kwargs):
        delete_good(request, str(kwargs["pk"]))
        return redirect(reverse_lazy("goods:goods"))


class CheckDocumentGrading(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        self.form = document_grading_form(request, self.object_pk)
        self.action = post_good_document_sensitivity

    def get_success_url(self):
        if self.request.POST.get("has_document_to_upload") == "no":
            good = self.get_validated_data()["good"]
            raise_a_clc_query = "unsure" == good["is_good_controlled"]["key"]
            raise_a_pv_query = "grading_required" == good["is_pv_graded"]["key"]

            if not (raise_a_clc_query or raise_a_pv_query):
                url = "goods:good"
            else:
                url = "goods:raise_goods_query"
        else:
            url = "goods:attach_documents"
        return reverse_lazy(url, kwargs={"pk": self.object_pk})


@method_decorator(csrf_exempt, "dispatch")
class AttachDocuments(TemplateView):
    def get(self, request, **kwargs):
        return_to_good_page = request.GET.get("goodpage", "no")
        good_id = str(kwargs["pk"])
        if return_to_good_page == "yes":
            back_link = BackLink(AttachDocumentForm.BACK_GOOD_LINK, reverse("goods:good", kwargs={"pk": good_id}))
        else:
            back_link = BackLink(
                AttachDocumentForm.BACK_FORM_LINK, reverse("goods:add_document", kwargs={"pk": good_id})
            )
        form = attach_documents_form(back_link)
        return form_page(request, form, extra_data={"good_id": good_id})

    @csrf_exempt
    def post(self, request, **kwargs):
        self.request.upload_handlers.insert(0, S3FileUploadHandler(request))

        good_id = str(kwargs["pk"])
        good, _ = get_good(request, good_id)

        data, error = add_document_data(request)

        if error:
            return error_page(request, error)

        data, status_code = post_good_documents(request, good_id, data)
        if status_code != HTTPStatus.CREATED:
            return error_page(request, data["errors"]["file"])

        raise_a_clc_query = "unsure" == good["is_good_controlled"]["key"]
        raise_a_pv_query = "grading_required" == good["is_pv_graded"]["key"]

        if not (raise_a_clc_query or raise_a_pv_query):
            return redirect(reverse("goods:good", kwargs={"pk": good_id}))
        else:
            return redirect(reverse("goods:raise_goods_query", kwargs={"pk": good_id}))


class Document(TemplateView):
    def get(self, request, **kwargs):
        good_id = str(kwargs["pk"])
        file_pk = str(kwargs["file_pk"])

        document = get_good_document(request, good_id, file_pk)
        return download_document_from_s3(document["s3_key"], document["name"])


class DeleteDocument(TemplateView):
    def get(self, request, **kwargs):
        good_id = str(kwargs["pk"])
        file_pk = str(kwargs["file_pk"])

        document = get_good_document(request, good_id, file_pk)

        context = {
            "title": goods.DeleteGoodDocumentPage.TITLE,
            "good_id": good_id,
            "document": document,
        }
        return render(request, "goods/delete-document.html", context)

    def post(self, request, **kwargs):
        good_id = str(kwargs["pk"])
        file_pk = str(kwargs["file_pk"])

        # Delete the file on the API
        delete_good_document(request, good_id, file_pk)

        return redirect(reverse("goods:good", kwargs={"pk": good_id}))
