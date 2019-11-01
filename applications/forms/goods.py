from django.urls import reverse

from lite_forms.components import Form, HiddenField, SideBySideSection, Select, QuantityInput, \
    CurrencyInput, BackLink
from lite_forms.helpers import conditional

from core.services import get_units
from goods.forms import add_goods_questions, attach_documents_form
from goods.helpers import good_summary


def good_on_application_form(good, units, back_form=False):
    form = Form(title='Add a pre-existing good to your application',
                questions=[
                    CurrencyInput(title='What\'s the value of your goods?',
                                  name='value'),
                    SideBySideSection(questions=[
                        QuantityInput(title='Quantity',
                                      name='quantity'),
                        Select(title='Unit of Measurement',
                               name='unit',
                               options=units)
                    ]),
                ],
                use_input_for_back_link=back_form,
                javascript_imports=['/assets/javascripts/specific/add_good.js'])
    if good:
        form.questions.insert(0, good_summary(good))
        form.questions.insert(1, HiddenField(name='good_id', value=good['id']))
    return form


def add_new_good_forms(request, application_id):
    back_link = BackLink('back to application goods', reverse("applications:goods", kwargs={'pk': application_id}))
    return [
        add_goods_questions(clc=False, back_link=back_link),
        good_on_application_form(good=False, units=get_units(request), back_form=True),
        attach_documents_form('#', description="To finish creating the good, you must attach a document."
                                               "\n\nWarning: Do not upload any document which is above "
                                               "“official-sensitive” level\n\nMaximum size: 100MB per file",
                              back_form=True)]
