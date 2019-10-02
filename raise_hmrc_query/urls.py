from django.urls import path

from raise_hmrc_query import views

app_name = 'raise_hmrc_query'

urlpatterns = [
    # ex: /
    path('', views.SelectAnOrganisation.as_view(), name='select_organisation'),
    # ex: /start/
]