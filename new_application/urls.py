from django.urls import path

from . import views

app_name = 'new_application'
urlpatterns = [
    # ex: /
    path('', views.index, name='index'),
    # ex: /page/abc?id=abc
    # path('page/<uuid:id>', views.page, name='page'),
    # ex: /page/abc?id=abc
    # path('section/<uuid:id>', views.section, name='section'),
    # ex: /draft/overview?id=abc
    path('draft/overview', views.overview, name='overview'),
    # ex: /draft/cancel?id=abc
    path('draft/cancel', views.cancel, name='cancel'),
    # ex: /draft/cancel-confirm?id=abc
    path('draft/cancel-confirm', views.cancel_confirm, name='cancel_confirm'),
]
