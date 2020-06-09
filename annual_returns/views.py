from django.shortcuts import render
from django.views.generic import TemplateView


class AnnualReturns(TemplateView):
    def get(self, request, *args, **kwargs):
        return render(request, "annual-returns/help.html", {})
