from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from compliance.forms import annual_return_form_group
from compliance.services import post_annual_return, get_open_licence_returns, get_open_licence_return_download
from lite_forms.generators import success_page
from lite_forms.views import MultiFormView


class AnnualReturnsList(TemplateView):
    def get(self, request, *args, **kwargs):
        data = get_open_licence_returns(request)
        return render(request, "compliance/open-licence-returns/list.html", {"open_licence_returns": data})


class AnnualReturnsDownload(TemplateView):
    def get(self, request, pk):
        return get_open_licence_return_download(request, pk)


class AddAnnualReturn(MultiFormView):
    def init(self, request, **kwargs):
        self.forms = annual_return_form_group()
        self.action = post_annual_return

    def get_success_url(self):
        return reverse_lazy(
            "compliance:add_annual_return_success", kwargs={"pk": self.get_validated_data()["open_licence_returns"]}
        )


class AddAnnualReturnSuccess(TemplateView):
    def get(self, request, **kwargs):
        return success_page(
            request=request,
            title="Open licence return submitted",
            secondary_title="",
            description="",
            what_happens_next="",
            links={
                "View Open licence returns": reverse_lazy("compliance:open_licence_returns_list"),
                "Return to your export control account dashboard": reverse_lazy("core:home"),
            },
        )
