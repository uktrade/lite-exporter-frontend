from django.urls import path

from apply_for_a_licence import views

app_name = 'apply_for_a_licence'

urlpatterns = [
    # ex: /
    path('', views.StartApplication.as_view(), name='index'),
    # ex: /start/
    path('start/', views.InitialQuestions.as_view(), name='start'),
    # ex: /<uuid:pk>/overview/
    path('<uuid:pk>/overview/', views.Overview.as_view(), name='overview'),

    # ex: /<uuid:pk>/goods/
    path('<uuid:pk>/goods/', views.DraftGoodsList.as_view(), name='goods'),
    # ex: /<uuid:pk>/goods/add-preexisting/
    path('<uuid:pk>/goods/add-preexisting/', views.GoodsList.as_view(), name='preexisting_good'),
    # ex: /<uuid:pk>/goods/add-preexisting/<uuid:pk>/add/
    path('<uuid:pk>/goods/add-preexisting/<uuid:good_pk>/add/', views.AddPreexistingGood.as_view(),
         name='add_preexisting_good'),

    # ex: /<uuid:pk>/delete/
    path('<uuid:pk>/delete/', views.DeleteApplication.as_view(), name='delete'),

    # ex: /<uuid:pk>/location/
    path('<uuid:pk>/location/', views.Location.as_view(), name='location'),
    # ex: /<uuid:pk>/location/existing-sites/
    path('<uuid:pk>/location/existing-sites/', views.ExistingSites.as_view(), name='existing_sites'),
    # ex: /<uuid:pk>/location/external-locations/
    path('<uuid:pk>/location/external-locations/', views.ExternalLocations.as_view(), name='external_locations'),
    # ex: /<uuid:pk>/location/external-locations/add/
    path('<uuid:pk>/location/external-locations/add/', views.AddExternalLocation.as_view(), name='add_external_location'),
    # ex: /<uuid:pk>/location/external-locations/preexisting/
    path('<uuid:pk>/location/external-locations/preexisting/', views.AddExistingExternalLocation.as_view(), name='add_preexisting_external_location'),

    # ex: /<uuid:pk>/end-user/
    path('<uuid:pk>/end-user/', views.EndUser.as_view(), name='end_user'),
]
