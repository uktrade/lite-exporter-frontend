from django.urls import reverse_lazy

from lite_content.lite_internal_frontend import strings
from lite_forms.components import Form, Select, TextInput, BackLink
from lite_forms.helpers import conditional
from roles.services import get_roles


def add_user_form(request):
    return Form(
        title="junk",
        questions=[
            TextInput(title="What's the user's email?", name="email"),
            TextInput(title="What's the user's first name", name="first_name"),
            TextInput(title="What's the user's first name", name="last_name"),
            Select(
                name="role",
                options=get_roles(request, request.user.organisation, True),
                title="What role should this user have?",
            ),
        ],
        back_link=BackLink("Back to Users", reverse_lazy("users:users")),
    )


def edit_user_form(request, user_id, super_user: bool):
    return Form(
        title="Edit User",
        questions=[
            TextInput(title="Email", name="email"),
            TextInput(title="What's the user's first name", name="first_name"),
            TextInput(title="What's the user's first name", name="last_name"),
            conditional(
                not super_user,
                Select(
                    name="role",
                    options=get_roles(request, request.user.organisation, True),
                    title=strings.USER_ROLE_QUESTION,
                ),
            ),
        ],
        back_link=BackLink("Back to User", reverse_lazy("users:user", kwargs={"pk": user_id})),
        default_button_name="Save",
    )
