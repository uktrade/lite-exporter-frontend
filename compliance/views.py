from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from compliance.forms import annual_return_form_group
from compliance.services import post_annual_return
from lite_forms.views import MultiFormView


class AnnualReturns(TemplateView):
    def get(self, request, *args, **kwargs):
        return render(request, "compliance/annual-returns/help.html", {})


class AddAnnualReturn(MultiFormView):
    def init(self, request, **kwargs):
        self.forms = annual_return_form_group()
        self.action = post_annual_return
        self.success_url = reverse_lazy("compliance:annual_returns")
