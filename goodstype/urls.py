from django.urls import path

from . import views

app_name = 'goodstype'
urlpatterns = [
    # ex: /goodstype/
    path('<uuid:pk>', views.GoodsType.as_view(), name='goodstype'),
    # ex: /goodstype/43a88949-5db9-4334-b0cc-044e91827451
    # path('<uuid:pk>', views.case, name='goodstype'),
    # ex: /goodstype/add/
    path('add/', views.AddGoodsType.as_view(), name='add'),
]
