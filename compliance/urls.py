from django.urls import path

from compliance import views

app_name = "compliance"

urlpatterns = [
    path("open-licence-returns/", views.AnnualReturnsList.as_view(), name="open_licence_returns_list"),
    path(
        "open-licence-returns/<uuid:pk>/download/",
        views.AnnualReturnsDownload.as_view(),
        name="open_licence_returns_download",
    ),
    path("open-licence-returns/add/", views.AddAnnualReturn.as_view(), name="add_open_licence_return"),
    path(
        "open-licence-returns/<uuid:pk>/success/",
        views.AddAnnualReturnSuccess.as_view(),
        name="add_open_licence_return_success",
    ),
]