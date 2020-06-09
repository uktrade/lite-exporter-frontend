from django.urls import path

from compliance import views

app_name = "compliance"

urlpatterns = [
    path("annual-returns/", views.AnnualReturns.as_view(), name="annual_returns"),
    path("annual-returns/add/", views.AddAnnualReturn.as_view(), name="add_annual_return"),
]
