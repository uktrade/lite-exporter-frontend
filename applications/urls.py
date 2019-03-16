from django.urls import path

from . import views

app_name = 'applications'
urlpatterns = [
    # ex: /
    path('', views.index, name='applications'),
  	# ex: /
    path('<uuid:id>', views.application, name='application'),
]
