from conf.constants import HMRC
from core.services import get_control_list_entries
from lite_content.lite_exporter_frontend.goods_types import CreateGoodsTypeForm
from lite_forms.common import control_list_entries_question
from lite_forms.components import TextArea, RadioButtons, Option, Form
from lite_forms.helpers import conditional


def goods_type_form(request, application_type: str):
    return Form(
        title=CreateGoodsTypeForm.TITLE,
        description=CreateGoodsTypeForm.DESCRIPTION,
        questions=[
            TextArea(title=CreateGoodsTypeForm.Description.TITLE, name="description", extras={"max_length": 2000,}),
            *conditional(
                application_type != HMRC,
                [
                    RadioButtons(
                        title=CreateGoodsTypeForm.IsControlled.TITLE,
                        description=CreateGoodsTypeForm.IsControlled.DESCRIPTION,
                        name="is_good_controlled",
                        options=[
                            Option(
                                key="yes",
                                value=CreateGoodsTypeForm.IsControlled.YES,
                                components=[
                                    control_list_entries_question(
                                        control_list_entries=get_control_list_entries(request, convert_to_options=True),
                                    ),
                                ],
                            ),
                            Option(key="no", value=CreateGoodsTypeForm.IsControlled.NO),
                        ],
                    ),
                    RadioButtons(
                        title=CreateGoodsTypeForm.IsIncorporated.TITLE,
                        description=CreateGoodsTypeForm.IsIncorporated.DESCRIPTION,
                        name="is_good_incorporated",
                        options=[
                            Option(key=True, value=CreateGoodsTypeForm.IsIncorporated.YES),
                            Option(key=False, value=CreateGoodsTypeForm.IsIncorporated.NO),
                        ],
                    ),
                ],
                [],
            ),
        ],
    )
