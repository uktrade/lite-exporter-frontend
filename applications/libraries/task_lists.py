from django.shortcuts import render


def get_application_task_list(request, application):
    if application['application_type']['key'] == 'standard_licence':
        return _get_standard_application_task_list(request, application)
    elif application['application_type']['key'] == 'open_licence':
        return _get_open_application_task_list(request, application)
    elif application['application_type']['key'] == 'hmrc_query':
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
