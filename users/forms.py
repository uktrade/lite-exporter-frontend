from django.urls import reverse_lazy

from lite_content.lite_exporter_frontend import strings
from lite_forms.components import Form, Select, TextInput, BackLink
from lite_forms.helpers import conditional
from roles.services import get_roles


def add_user_form(request):
    return Form(
        title=strings.USER_ADD_TITLE,
        questions=[
            TextInput(title=strings.USER_EMAIL_QUESTION, name="email"),
            TextInput(title=strings.USER_FIRST_NAME_QUESTION, name="first_name"),
            TextInput(title=strings.USER_LAST_NAME_QUESTION, name="last_name"),
            Select(
                name="role",
                options=get_roles(request, request.user.organisation, True),
                title=strings.USER_ROLE_QUESTION,
            ),
        ],
        back_link=BackLink(strings.USER_ADD_FORM_BACK_TO_USERS, reverse_lazy("users:users")),
    )


def edit_user_form(request, user_id, super_user: bool):
    return Form(
        title=strings.USER_EDIT_TITLE,
        questions=[
            TextInput(title=strings.USER_EMAIL_QUESTION, name="email"),
            TextInput(title=strings.USER_FIRST_NAME_QUESTION, name="first_name"),
            TextInput(title=strings.USER_LAST_NAME_QUESTION, name="last_name"),
            conditional(
                not super_user,
                Select(
                    name="role",
                    options=get_roles(request, request.user.organisation, True),
                    title=strings.USER_ROLE_QUESTION,
                ),
            ),
        ],
        back_link=BackLink(strings.USER_EDIT_FORM_BACK_TO_USER, reverse_lazy("users:user", kwargs={"pk": user_id})),
        default_button_name=strings.USER_EDIT_FORM_SAVE,
    )
