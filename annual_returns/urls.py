from django.urls import path

from annual_returns import views

app_name = "annual_returns"

urlpatterns = [
    path("", views.AnnualReturns.as_view(), name="annual_returns"),
]
