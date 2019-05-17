from django.urls import path

from apply_for_a_licence import views

app_name = 'apply_for_a_licence'

urlpatterns = [
    # ex: /
    path('', views.StartApplication.as_view(), name='index'),
    # ex: /start/
    path('start/', views.InitialQuestions.as_view(), name='start'),
]
