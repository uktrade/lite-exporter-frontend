from core.builtins.custom_tags import default_na


def convert_application_to_check_your_answers(application):
    if application['application_type']['key'] == 'standard_licence':
        return _convert_standard_application(application)
    elif application['application_type']['key'] == 'open_licence':
        return _convert_open_application(application)
    elif application['application_type']['key'] == 'hmrc_query':
        return _convert_hmrc_query(application)
    else:
        raise NotImplementedError()


def _convert_standard_application(application):
    raise NotImplementedError()


def _convert_open_application(application):
    raise NotImplementedError()


def _convert_hmrc_query(application):
    return {
        'On behalf of': application['organisation']['name'],
        'Goods': [
            {
                'Description': 'Easy to find',
                'Part number': 'ML1a',
                'Control list entry': 'ML1a',
                'Quantity': 'ML1a',
                'Monetary value': 'ML1a',
            },
            {
                'Description': 'Easy to find',
                'Part number': 'ML1a',
                'Control list entry': 'ML1a',
                'Quantity': 'ML1a',
                'Monetary value': 'ML1a',
            },
            {
                'Description': 'Easy to find',
                'Part number': 'ML1a',
                'Control list entry': default_na(None),
                'Quantity': 'ML1a',
                'Monetary value': 'ML1a',
            }
        ],
        'End User': {
            'Name': 'Matt Berninger',
            'Type': 'Commercial Organisation',
            'Address': '123 Reading Road',
            'Website': default_na(None),
            'Document': 'file.pdf'
        },
        'Ultimate end users': [
            {
                'Name': 'Matt Berninger',
                'Type': 'Commercial Organisation',
                'Address': '123 Reading Road',
                'Website': default_na(None),
                'Document': 'file.pdf'
            }
        ],
        'Optional note': application['reasoning']
    }
