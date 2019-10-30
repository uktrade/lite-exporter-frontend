from django.shortcuts import render


def get_hmrc_task_list(request, application):
    return render(request, 'applications/hmrc-edit.html')
