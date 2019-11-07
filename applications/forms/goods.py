from django.urls import reverse

from core.builtins.custom_tags import get_const_string
from lite_forms.components import Form, HiddenField, SideBySideSection, Select, QuantityInput, \
    CurrencyInput, BackLink, Button
from lite_forms.helpers import conditional

from core.services import get_units
from goods.forms import add_goods_questions, attach_documents_form
from goods.helpers import good_summary


def good_on_application_form(good, units, title, prefix=""):
    return Form(title=title,
                questions=[
                    conditional(good, good_summary(good)),
                    conditional(good, HiddenField(name='good_id', value=good.get('id'))),
                    CurrencyInput(title='What\'s the value of your goods?',
                                  name=prefix+'value'),
                    SideBySideSection(questions=[
                        QuantityInput(title='Quantity',
                                      name=prefix+'quantity'),
                        Select(title='Unit of Measurement',
                               name=prefix+'unit',
                               options=units)
                    ]),
                ],
                javascript_imports=['/assets/javascripts/specific/add_good.js'])


def add_new_good_forms(request, application_id):
    back_link = BackLink(get_const_string("APPLICATION_GOODS_ADD_BACK"), reverse("applications:goods",
                                                                                 kwargs={'pk': application_id}))

    return [
        add_goods_questions(clc=False, back_link=back_link, prefix="good_"),
        good_on_application_form(good={}, units=get_units(request), prefix="good_on_app_",
                                 title=get_const_string('APPLICATION_GOODS_ADD_APPLICATION_DETAILS')),
        attach_documents_form('#', description=get_const_string("APPLICATION_GOODS_ADD_DOCUMENT_DESCRIPTION"))]
