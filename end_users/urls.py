from django.urls import path

from end_users import views

app_name = 'end_users'

urlpatterns = [
    # ex: /end-users/
    path('', views.EndUsersList.as_view(), name='end_users'),
    # ex: /end-users/<int:pk>/
    path('<int:pk>/', views.EndUserDetailEmpty.as_view(), name='end_user'),
    # ex: /end-users/<int:pk>/copy-advisory/
    path('<int:pk>/copy-advisory/', views.CopyAdvisory.as_view(), name='copy'),
    # ex: /end-users/apply-for-an-advisory/
    path('apply-for-an-advisory/', views.ApplyForAnAdvisory.as_view(), name='apply'),
    # ex: /end-users/<int:pk>/<str:type>/
    path('<int:pk>/<str:type>/', views.EndUserDetail.as_view(), name='end_user_detail'),
]
