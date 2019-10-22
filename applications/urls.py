from django.urls import path

from applications import views

app_name = 'applications'
urlpatterns = [
    # ex: /applications/
    path('', views.ApplicationsList.as_view(), name='applications'),
    # ex: /applications/43a88949-5db9-4334-b0cc-044e91827451/
    path('<uuid:pk>/', views.ApplicationDetailEmpty.as_view(), name='application'),
    # ex: /applications/43a88949-5db9-4334-b0cc-044e91827451/edit/type
    path('<uuid:pk>/edit/type/', views.ApplicationEditType.as_view(), name='application-edit-type'),
    # ex: /applications/43a88949-5db9-4334-b0cc-044e91827451/edit/overview
    path('<uuid:pk>/edit/overview/', views.ApplicationEditOverview.as_view(), name='application_edit_overview'),
    # ex: /applications/43a88949-5db9-4334-b0cc-044e91827451/case-notes/
    path('<uuid:pk>/<str:type>/', views.ApplicationDetail.as_view(), name='application-detail'),
    # ex: /applications/43a88949-5db9-4334-b0cc-044e91827451/
    path('<uuid:pk>/ecju-queries/<uuid:query_pk>/', views.RespondToQuery.as_view(), name='respond_to_query'),
]
