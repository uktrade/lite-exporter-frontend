from django.shortcuts import render


def get_hmrc_task_list(request, application):
    context = {
        'application': application
    }
    return render(request, 'hmrc/task-list.html', context)
