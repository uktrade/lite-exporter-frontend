from django.urls import path

from drafts import views

app_name = 'drafts'
urlpatterns = [
    # ex: /drafts/ - View all drafts
    path('', views.DraftsList.as_view(), name='drafts'),
]
