from django.contrib.auth.models import AnonymousUser
from django.shortcuts import redirect
from django.urls import resolve

from users.services import get_user


class ProtectAllViewsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if resolve(request.path).app_name != 'authbroker_client' and not request.user.is_authenticated:
            return redirect('authbroker:login')

        if not isinstance(request.user, AnonymousUser):
            if not request.user.organisation:
                user = get_user(request)

                if len(user['organisations']) > 1:
                    return redirect('core:pick_organisation')
                else:
                    request.user.organisation = user['organisations'][0]
                    request.user.save()

        response = self.get_response(request)

        return response
