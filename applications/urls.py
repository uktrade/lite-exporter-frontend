from django.urls import path

from applications.views.parties import consignees, end_users, third_parties, ultimate_end_users
from applications.views import (
    goods,
    documents,
    locations,
    additional_documents,
    common,
    reference_name,
    told_by_an_official,
    optional_note,
    goods_types,
)

app_name = "applications"
urlpatterns = [
    # Common
    path("", common.ApplicationsList.as_view(), name="applications"),
    path("<uuid:pk>/delete/", common.DeleteApplication.as_view(), name="delete"),
    path("<uuid:pk>/task-list/", common.ApplicationTaskList.as_view(), name="task_list"),
    path("<uuid:pk>/submit-success/", common.ApplicationSubmitSuccessPage.as_view(), name="success_page"),
    path("<uuid:pk>/edit-type/", common.ApplicationEditType.as_view(), name="edit_type"),
    path("<uuid:pk>/check-your-answers/", common.CheckYourAnswers.as_view(), name="check_your_answers"),
    path("<uuid:pk>/submit/", common.Submit.as_view(), name="submit"),
    path("<uuid:pk>/ecju-queries/<uuid:query_pk>/", common.RespondToQuery.as_view(), name="respond_to_query"),
    # Standard and Open Licence
    path(
        "<uuid:pk>/edit/reference-name/",
        reference_name.ApplicationEditReferenceName.as_view(),
        name="edit_reference_name",
    ),
    path(
        "<uuid:pk>/edit/told-by-an-official/",
        told_by_an_official.ApplicationEditToldByAnOfficial.as_view(),
        name="edit_told_by_an_official",
    ),
    # HMRC Query
    path("<uuid:pk>/optional-note/", optional_note.ApplicationOptionalNote.as_view(), name="optional_note"),
    # Goods
    path("<uuid:pk>/goods/", goods.DraftGoodsList.as_view(), name="goods"),
    path("<uuid:pk>/goods/add-new/", goods.AddGood.as_view(), name="new_good"),
    path(
        "<uuid:pk>/goods/add-new/<uuid:good_pk>/add-document/",
        goods.CheckDocumentGrading.as_view(),
        name="add_document",
    ),
    path("<uuid:pk>/goods/add-new/<uuid:good_pk>/attach/", goods.AttachDocument.as_view(), name="attach_documents"),
    path("<uuid:pk>/goods/add-preexisting/", goods.GoodsList.as_view(), name="preexisting_good"),
    path("<uuid:pk>/goods/<uuid:good_pk>/add/", goods.AddGoodToApplication.as_view(), name="add_good_to_application",),
    path(
        "<uuid:pk>/good-on-application/<uuid:good_on_application_pk>/remove/",
        goods.RemovePreexistingGood.as_view(),
        name="remove_preexisting_good",
    ),
    # Goods Types
    path("<uuid:pk>/goods-types/", goods_types.GoodsTypeList.as_view(), name="goods_types"),
    path("<uuid:pk>/goods-types/countries/", goods_types.GoodsTypeCountries.as_view(), name="goods_countries"),
    path("<uuid:pk>/goods-types/add/", goods_types.GoodsTypeAdd.as_view(), name="add_goods_type"),
    path(
        "<uuid:pk>/goods-types/remove/<uuid:goods_type_pk>/",
        goods_types.GoodsTypeRemove.as_view(),
        name="remove_goods_type",
    ),
    path(
        "<uuid:pk>/goods-types/<uuid:obj_pk>/document/attach",
        documents.AttachDocuments.as_view(),
        name="goods_type_attach_document",
    ),
    path(
        "<uuid:pk>/goods-types/<uuid:obj_pk>/document/download",
        documents.DownloadDocument.as_view(),
        name="goods_type_download_document",
    ),
    path(
        "<uuid:pk>/goods-types/<uuid:obj_pk>/document/delete",
        documents.DeleteDocument.as_view(),
        name="goods_type_delete_document",
    ),
    # Goods locations
    path("<uuid:pk>/goods-locations/", locations.GoodsLocation.as_view(), name="location"),
    path("<uuid:pk>/goods-locations/edit/", locations.EditGoodsLocation.as_view(), name="edit_location"),
    path("<uuid:pk>/goods-locations/existing-sites/", locations.ExistingSites.as_view(), name="existing_sites"),
    path(
        "<uuid:pk>/goods-locations/external-locations/select/",
        locations.SelectAddExternalLocation.as_view(),
        name="select_add_external_location",
    ),
    path(
        "<uuid:pk>/goods-locations/external-locations/add/",
        locations.AddExternalLocation.as_view(),
        name="add_external_location",
    ),
    path(
        "<uuid:pk>/goods-locations/external-locations/<uuid:ext_loc_pk>/",
        locations.RemoveExternalLocation.as_view(),
        name="remove_external_location",
    ),
    path(
        "<uuid:pk>/goods-locations/external-locations/preexisting/",
        locations.AddExistingExternalLocation.as_view(),
        name="add_preexisting_external_location",
    ),
    path("<uuid:pk>/goods-locations/countries/", locations.Countries.as_view(), name="countries"),
    # End User
    path("<uuid:pk>/end-user/", end_users.EndUser.as_view(), name="end_user"),
    path("<uuid:pk>/end-user/add/", end_users.AddEndUser.as_view(), name="add_end_user"),
    path("<uuid:pk>/end-user/set/", end_users.SetEndUser.as_view(), name="set_end_user"),
    path("<uuid:pk>/end-user/copy/", end_users.CopyEndUsers.as_view(), name="end_users_copy"),
    path("<uuid:pk>/end-user/<uuid:obj_pk>/", end_users.EndUser.as_view(), name="end_user"),
    path("<uuid:pk>/end-user/<uuid:obj_pk>/edit/", end_users.EditEndUser.as_view(), name="edit_end_user"),
    path("<uuid:pk>/end-user/<uuid:obj_pk>/copy/", end_users.CopyEndUser.as_view(), name="copy_end_user"),
    path("<uuid:pk>/end-user/<uuid:obj_pk>/remove/", end_users.RemoveEndUser.as_view(), name="remove_end_user"),
    path(
        "<uuid:pk>/end-user/<uuid:obj_pk>/document/attach/",
        documents.AttachDocuments.as_view(),
        name="end_user_attach_document",
    ),
    path(
        "<uuid:pk>/end-user/<uuid:obj_pk>/document/download",
        documents.DownloadDocument.as_view(),
        name="end_user_download_document",
    ),
    path(
        "<uuid:pk>/end-user/<uuid:obj_pk>/document/delete",
        documents.DeleteDocument.as_view(),
        name="end_user_delete_document",
    ),
    # Consignee
    path("<uuid:pk>/consignee/", consignees.Consignee.as_view(), name="consignee"),
    path("<uuid:pk>/consignee/add/", consignees.AddConsignee.as_view(), name="add_consignee"),
    path("<uuid:pk>/consignee/set/", consignees.SetConsignee.as_view(), name="set_consignee"),
    path("<uuid:pk>/consignee/copy/", consignees.CopyConsignees.as_view(), name="consignees_copy"),
    path("<uuid:pk>/consignee/<uuid:obj_pk>/", consignees.Consignee.as_view(), name="consignee"),
    path("<uuid:pk>/consignee/<uuid:obj_pk>/edit/", consignees.EditConsignee.as_view(), name="edit_consignee"),
    path("<uuid:pk>/consignee/<uuid:obj_pk>/copy/", consignees.CopyConsignee.as_view(), name="copy_consignee"),
    path("<uuid:pk>/consignee/<uuid:obj_pk>/remove/", consignees.RemoveConsignee.as_view(), name="remove_consignee"),
    path(
        "<uuid:pk>/consignee/<uuid:obj_pk>/document/attach/",
        documents.AttachDocuments.as_view(),
        name="consignee_attach_document",
    ),
    path(
        "<uuid:pk>/consignee/<uuid:obj_pk>/document/download",
        documents.DownloadDocument.as_view(),
        name="consignee_download_document",
    ),
    path(
        "<uuid:pk>/consignee/<uuid:obj_pk>/document/delete",
        documents.DeleteDocument.as_view(),
        name="consignee_delete_document",
    ),
    # Ultimate end users
    path("<uuid:pk>/ultimate-end-users/", ultimate_end_users.UltimateEndUsers.as_view(), name="ultimate_end_users"),
    path(
        "<uuid:pk>/ultimate-end-users/add/",
        ultimate_end_users.AddUltimateEndUser.as_view(),
        name="add_ultimate_end_user",
    ),
    path(
        "<uuid:pk>/ultimate-end-users/set/",
        ultimate_end_users.SetUltimateEndUser.as_view(),
        name="set_ultimate_end_user",
    ),
    path(
        "<uuid:pk>/ultimate-end-users/copy/",
        ultimate_end_users.CopyUltimateEndUsers.as_view(),
        name="ultimate_end_users_copy",
    ),
    path(
        "<uuid:pk>/ultimate-end-users/<uuid:obj_pk>/copy/",
        ultimate_end_users.CopyUltimateEndUser.as_view(),
        name="copy_ultimate_end_user",
    ),
    path(
        "<uuid:pk>/ultimate-end-users/<uuid:obj_pk>/remove/",
        ultimate_end_users.RemoveUltimateEndUser.as_view(),
        name="remove_ultimate_end_user",
    ),
    path(
        "<uuid:pk>/ultimate-end-users/<uuid:obj_pk>/",
        ultimate_end_users.UltimateEndUsers.as_view(),
        name="ultimate_end_users",
    ),
    path(
        "<uuid:pk>/ultimate-end-users/<uuid:obj_pk>/document/attach",
        documents.AttachDocuments.as_view(),
        name="ultimate_end_user_attach_document",
    ),
    path(
        "<uuid:pk>/ultimate-end-users/<uuid:obj_pk>/document/download",
        documents.DownloadDocument.as_view(),
        name="ultimate_end_user_download_document",
    ),
    path(
        "<uuid:pk>/ultimate-end-users/<uuid:obj_pk>/document/delete",
        documents.DeleteDocument.as_view(),
        name="ultimate_end_user_delete_document",
    ),
    # Third parties
    path("<uuid:pk>/third-parties/", third_parties.ThirdParties.as_view(), name="third_parties"),
    path("<uuid:pk>/third-parties/add/", third_parties.AddThirdParty.as_view(), name="add_third_party"),
    path("<uuid:pk>/third-parties/set/", third_parties.SetThirdParty.as_view(), name="set_third_party"),
    path("<uuid:pk>/third-parties/copy/", third_parties.CopyThirdParties.as_view(), name="third_parties_copy"),
    path("<uuid:pk>/third-parties/<uuid:obj_pk>/", third_parties.ThirdParties.as_view(), name="third_parties"),
    path(
        "<uuid:pk>/third-parties/<uuid:obj_pk>/copy/", third_parties.CopyThirdParty.as_view(), name="copy_third_party"
    ),
    path(
        "<uuid:pk>/third-parties/<uuid:obj_pk>/document/attach",
        documents.AttachDocuments.as_view(),
        name="third_party_attach_document",
    ),
    path(
        "<uuid:pk>/third-parties/<uuid:obj_pk>/document/download",
        documents.DownloadDocument.as_view(),
        name="third_party_download_document",
    ),
    path(
        "<uuid:pk>/third-parties/<uuid:obj_pk>/document/delete",
        documents.DeleteDocument.as_view(),
        name="third_party_delete_document",
    ),
    path(
        "<uuid:pk>/third-parties/<uuid:obj_pk>/remove",
        third_parties.RemoveThirdParty.as_view(),
        name="remove_third_party",
    ),
    # Supporting documentation
    path(
        "<uuid:pk>/additional-documents/",
        additional_documents.AdditionalDocuments.as_view(),
        name="additional_documents",
    ),
    path(
        "<uuid:pk>/additional-document/attach", documents.AttachDocuments.as_view(), name="attach_additional_document"
    ),
    path(
        "<uuid:pk>/additional-document/<uuid:obj_pk>/download",
        documents.DownloadDocument.as_view(),
        name="download_additional_document",
    ),
    path(
        "<uuid:pk>/additional-document/<uuid:obj_pk>/delete",
        documents.DeleteDocument.as_view(),
        name="delete_additional_document",
    ),
    path("<uuid:pk>/case-note/", common.CaseNote.as_view(), name="case-note"),
    path("<uuid:pk>/withdraw/", common.WithdrawApplication.as_view(), name="withdraw"),
    path("<uuid:pk>/surrender/", common.SurrenderApplication.as_view(), name="surrender"),
    # Case-relevant documentation
    path(
        "<uuid:pk>/generated-documents/<uuid:obj_pk>/download",
        documents.DownloadDocument.as_view(),
        name="download_generated_document",
    ),
    # This HAS to be at the bottom, otherwise it will swallow other url calls
    path("<uuid:pk>/", common.ApplicationDetail.as_view(), name="application"),
    path("<uuid:pk>/<str:type>/", common.ApplicationDetail.as_view(), name="application"),
]
