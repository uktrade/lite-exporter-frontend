from django.urls import path

from compliance import views

app_name = "compliance"

urlpatterns = [
    path("annual-returns/", views.AnnualReturnsList.as_view(), name="annual_returns_list"),
    path("annual-returns/<uuid:pk>/download/", views.AnnualReturnsDownload.as_view(), name="annual_returns_download"),
    path("annual-returns/add/", views.AddAnnualReturn.as_view(), name="add_annual_return"),
]
