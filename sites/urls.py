from django.urls import path

from . import views

app_name = 'sites'
urlpatterns = [
    # ex: /
    path('', views.Sites.as_view(), name='sites'),
]
