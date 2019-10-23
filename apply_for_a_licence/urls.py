from django.urls import path

from apply_for_a_licence.views import common

app_name = 'apply_for_a_licence'

urlpatterns = [
    # ex: /start/
    path('start/', common.InitialQuestions.as_view(), name='start'),
]
