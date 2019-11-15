from conf.settings import env
from lite_content.lite_exporter_frontend import strings


def export_vars(request):
    data = {
        'SERVICE_NAME': strings.SERVICE_NAME,
        'GOV_UK_URL': 'https://www.gov.uk',
        'FEEDBACK_URL': env('FEEDBACK_URL'),
        'INTERNAL_URL': env('INTERNAL_FRONTEND_URL'),
        'GOOGLE_ANALYTICS_KEY': env('GOOGLE_ANALYTICS_KEY'),
    }
    return data
