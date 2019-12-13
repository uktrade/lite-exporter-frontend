from django.urls import path

from sites import views

app_name = "sites"

urlpatterns = [
    path("", views.Sites.as_view(), name="sites"),
    path("new/", views.NewSite.as_view(), name="new"),
    path("<uuid:pk>/", views.ViewSite.as_view(), name="site"),
    path("<uuid:pk>/edit/", views.EditSite.as_view(), name="edit"),
]
