from django.urls import reverse_lazy

from applications.forms.misc import reference_name_form, goods_categories
from applications.services import get_application, put_application
from lite_forms.views import SingleFormView


class EditReferenceName(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        self.data = get_application(request, self.object_pk)
        self.form = reference_name_form(self.object_pk)
        self.action = put_application
        self.success_url = reverse_lazy("applications:task_list", kwargs={"pk": self.object_pk})


class EditGoodsCategories(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        self.data = {"goods_categories": [x["key"] for x in get_application(request, self.object_pk)["goods_categories"]]}
        self.form = goods_categories(self.object_pk)
        self.action = put_application
        self.success_url = reverse_lazy("applications:task_list", kwargs={"pk": self.object_pk})

    def on_submission(self, request, **kwargs):
        data = request.POST.copy()

        if not data.get("goods_categories[]"):
            return {"goods_categories": []}

        return data
