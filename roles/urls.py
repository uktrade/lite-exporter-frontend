from django.urls import path

from . import views

app_name = 'roles'
urlpatterns = [
    # ex: /sites/
    path('', views.Roles.as_view(), name='roles'),
    # ex: /sites/new/
    path('new/', views.AddRole.as_view(), name='new'),
    # ex: /sites/new/
    path('<uuid:pk>/edit/', views.EditRole.as_view(), name='edit'),
]
