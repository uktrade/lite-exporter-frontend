from django.shortcuts import render

from conf.constants import HMRC_QUERY, OPEN_LICENCE, STANDARD_LICENCE


def get_application_task_list(request, application):
    if application['application_type']['key'] == STANDARD_LICENCE:
        return _get_standard_application_task_list(request, application)
    elif application['application_type']['key'] == OPEN_LICENCE:
        return _get_open_application_task_list(request, application)
    elif application['application_type']['key'] == HMRC_QUERY:
        return _get_hmrc_query_task_list(request, application)
    else:
        raise NotImplementedError()


def _get_standard_application_task_list(request, application):
    context = {
        'application': application
    }
    return render(request, 'applications/standard-application-edit.html', context)


def _get_open_application_task_list(request, application):
    context = {
        'application': application
    }
    return render(request, 'applications/open-application-edit.html', context)


def _get_hmrc_query_task_list(request, application):
    context = {
        'application': application
    }
    return render(request, 'hmrc/task-list.html', context)
