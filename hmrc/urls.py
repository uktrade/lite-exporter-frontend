from django.urls import path

from hmrc import views

app_name = 'hmrc'

urlpatterns = [
    # ex: /drafts/
    path('drafts/', views.DraftsList.as_view(), name='drafts'),
    # ex: /raise-a-query/
    path('raise-a-query/', views.SelectAnOrganisation.as_view(), name='raise_a_query'),
]
