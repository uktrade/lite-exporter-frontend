import os


def export_vars(request):
    data = {
        'ENVIRONMENT_VARIABLES': dict(os.environ.items()),
        'SERVICE_NAME': 'LITE',
        'GOV_UK_ADDRESS': 'https://www.gov.uk'
    }
    return data
