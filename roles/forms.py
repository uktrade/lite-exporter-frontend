from django.http import HttpRequest
from django.urls import reverse_lazy

from lite_content.lite_exporter_frontend import strings
from lite_forms.components import Form, TextInput, Checkboxes, BackLink
from roles.services import get_permissions


def add_role(request: HttpRequest):
    return Form(
        title=strings.roles.AddRoleForm.TITLE,
        description=strings.roles.AddRoleForm.DESCRIPTION,
        questions=[
            TextInput(title=strings.roles.AddRoleForm.ADD_NAME, name="name"),
            Checkboxes(
                name="permissions[]",
                options=get_permissions(request, True),
                title=strings.roles.AddRoleForm.ADD_PERMISSIONS,
                description=strings.roles.AddRoleForm.ADD_PERMISSIONS_DESCRIPTION,
            ),
        ],
        back_link=BackLink(strings.roles.AddRoleForm.ADD_FORM_BACK_TO_ROLES, reverse_lazy("roles:roles")),
        default_button_name=strings.roles.AddRoleForm.ADD_FORM_CREATE,
    )


def edit_role(request: HttpRequest):
    return Form(
        title=strings.roles.EditRoleForm.TITLE,
        description=strings.roles.EditRoleForm.DESCRIPTION,
        questions=[
            TextInput(title=strings.roles.EditRoleForm.EDIT_NAME, name="name"),
            Checkboxes(
                name="permissions[]",
                options=get_permissions(request, True),
                title=strings.roles.EditRoleForm.EDIT_PERMISSIONS,
                description=strings.roles.EditRoleForm.EDIT_PERMISSIONS_DESCRIPTION,
            ),
        ],
        back_link=BackLink(strings.roles.EditRoleForm.EDIT_FORM_BACK_TO_ROLES, reverse_lazy("roles:roles")),
        default_button_name=strings.roles.EditRoleForm.EDIT_FORM_CREATE,
    )
