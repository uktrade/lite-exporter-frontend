from lite_forms.components import Form, HiddenField, SideBySideSection, Select, QuantityInput, \
    CurrencyInput

from core.services import get_units
from goods.forms import add_goods_questions, attach_documents_form
from goods.helpers import good_summary


def good_on_application_form(good, units):
    if good:
        return Form(title='Add a pre-existing good to your application',
                    questions=[
                        good_summary(good),
                        HiddenField(name='good_id',
                                    value=good['id']),
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
                    javascript_imports=['/assets/javascripts/specific/add_good.js'])
    else:
        return Form(title='Add details for the good on this application',
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
                    javascript_imports=['/assets/javascripts/specific/add_good.js'])


def add_new_good_forms(request):
    return [
        add_goods_questions(clc=False),
        good_on_application_form(good=None, units=get_units(request)),
        attach_documents_form('#', description="To finish creating the good, you must attach a document."
                                               "\n\nWarning: Do not upload any document which is above "
                                               "“official-sensitive” level\n\nMaximum size: 100MB per file")]
