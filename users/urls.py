from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    # ex: /users/
    path('', views.Users.as_view(), name='users'),
    # ex: /user/43a88949-5db9-4334-b0cc-044e91827451
    # path('<uuid:pk>', views.case, name='user'),
    # ex: /user/add/
    path('add/', views.AddUser.as_view(), name='add'),
]
