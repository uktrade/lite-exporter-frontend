from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    # ex: /users/
    path('', views.Users.as_view(), name='users'),
    # ex: /user/43a88949-5db9-4334-b0cc-044e91827451
    # path('<uuid:pk>', views.EditUser.as_view(), name='user'),
    # ex: /user/add/
    path('add', views.AddUser.as_view(), name='add'),
    path('deactivate', views.deactivate, name='deactivate'),
    # ex: /draft/cancel-confirm?id=abc
    path('users/deactivate-confirm/', views.deactivate_confirm, name='deactivate_confirm'),
    path('reactivate', views.reactivate, name='reactivate'),
    path('users/reactivate-confirm/', views.reactivate_confirm, name='reactivate_confirm'),
    path('profile/', views.ViewUser.as_view(), name='profile'),
    path('edit', views.EditUser.as_view(), name='edit')
]
