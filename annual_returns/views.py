from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from annual_returns.forms import annual_return_form_group
from annual_returns.services import post_annual_return
from lite_forms.views import MultiFormView


class AnnualReturns(TemplateView):
    def get(self, request, *args, **kwargs):
        return render(request, "annual-returns/help.html", {})


class AddAnnualReturn(MultiFormView):
    def init(self, request, **kwargs):
        self.forms = annual_return_form_group()
        self.action = post_annual_return
        self.success_url = reverse_lazy("annual_returns:annual_returns")
