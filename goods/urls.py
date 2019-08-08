from django.urls import path

from . import views

app_name = 'goods'
urlpatterns = [
    # ex: /goods/
    path('', views.Goods.as_view(), name='goods'),
    # ex: /goods/43a88949-5db9-4334-b0cc-044e91827451
    path('<uuid:pk>', views.GoodsDetail.as_view(), name='good'),
    # ex: /goods/add/
    path('add/', views.AddGood.as_view(), name='add'),
    path('edit/<uuid:pk>/', views.EditGood.as_view(), name='edit'),
    path('delete/<uuid:pk>/', views.DeleteGood.as_view(), name='delete'),
    path('<uuid:pk>/delete', views.DeleteGood.as_view(), name='confirm_delete'),
    path('<uuid:pk>/documents/<str:file_pk>/', views.Document.as_view(), name='document'),
    path('<uuid:pk>/documents/<str:file_pk>/delete', views.DeleteDocument.as_view(), name="remove_document"),
    path('<uuid:pk>/attach/', views.AttachDocuments.as_view(), name='attach_documents'),
]
