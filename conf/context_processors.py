import os

from conf import settings


def export_vars(request):
    data = {'ENVIRONMENT_VARIABLES': dict(os.environ.items()),
            'SERVICE_NAME': settings.SERVICE_NAME}
    return data
