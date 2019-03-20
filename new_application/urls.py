from django.conf.urls import url
from django.urls import path

from new_application.forms import NewApplicationForm1, NewApplicationForm2
from new_application.views import ContactWizard
from . import views

named_contact_forms = (
    ('start', NewApplicationForm1),
    ('leavemessage', NewApplicationForm2),
)

contact_wizard = ContactWizard.as_view(named_contact_forms,
                                       url_name='new_application:contact_step',
                                       done_step_name='new_application:finished')

app_name = 'new_application'
urlpatterns = [
    # ex: /
    path('', views.index, name='index'),
    # ex: /page/abc?id=abc
    url(r'^form/(?P<step>.+)/$', contact_wizard, name='contact_step'),
    url(r'^form/$', contact_wizard, name='contact'),
    # ex: /draft/overview?id=abc
    path('draft/overview', views.overview, name='overview'),
    # ex: /draft/cancel?id=abc
    path('draft/cancel', views.cancel, name='cancel'),
    # ex: /draft/cancel-confirm?id=abc
    path('draft/cancel-confirm', views.cancel_confirm, name='cancel_confirm'),
]
