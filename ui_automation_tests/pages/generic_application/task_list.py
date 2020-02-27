from selenium.common.exceptions import NoSuchElementException

from shared import functions
from shared.BasePage import BasePage
from shared.functions import element_with_css_selector_exists, element_with_id_exists


class GenericApplicationTaskStatuses:
    DONE = "done"
    IN_PROGRESS = "in-progress"
    OTHER = "other"


class GenericApplicationTaskListPage(BasePage):

    LINK = "link-"
    STATUS = "-status"

    SECTION_GOOD_ID = "products"
    OPEN_GOODS_LINK = LINK + SECTION_GOOD_ID
    SECTION_GOOD_STATUS_ID = SECTION_GOOD_ID + STATUS

    SECTION_END_USER_ID = "end-user"
    LINK_END_USER_ID = LINK + SECTION_END_USER_ID
    SECTION_END_USER_STATUS_ID = SECTION_END_USER_ID + STATUS

    SECTION_ULTIMATE_END_USER_ID = "ultimate-end-user"
    LINK_ULTIMATE_END_USER_ID = LINK + SECTION_ULTIMATE_END_USER_ID
    SECTION_ULTIMATE_END_USER_STATUS_ID = SECTION_ULTIMATE_END_USER_ID + STATUS

    SECTION_CONSIGNEE_ID = "consignee"
    LINK_CONSIGNEE_ID = LINK + SECTION_CONSIGNEE_ID
    SECTION_CONSIGNEE_STATUS_ID = SECTION_CONSIGNEE_ID + STATUS

    SECTION_THIRD_PARTIES_ID = "third-parties"
    LINK_THIRD_PARTIES_ID = LINK + SECTION_CONSIGNEE_ID
    SECTION_THIRD_PARTIES_STATUS_ID = SECTION_CONSIGNEE_ID + STATUS

    SECTION_SUPPORTING_DOCUMENT_ID = "supporting-documents"
    LINK_SUPPORTING_DOCUMENTS_ID = LINK + SECTION_SUPPORTING_DOCUMENT_ID
    SECTION_SUPPORTING_DOCUMENT_STATUS_ID = SECTION_SUPPORTING_DOCUMENT_ID + STATUS

    SECTION_EXHIBITION_DETAILS_ID = "exhibition-details"
    LINK_EXHIBITION_DETAILS_ID = LINK + SECTION_EXHIBITION_DETAILS_ID
    SECTION_EXHIBITION_DETAILS_STATUS_ID = SECTION_EXHIBITION_DETAILS_ID + STATUS

    LOCATION_LINK = "link-locations"
    OPEN_GOODS_LINK = "link-products"
    LINK_END_USER_ID = "link-end-user"
    LINK_CONSIGNEE_ID = "link-consignee"
    LINK_NOTES_ID = "link-notes"
    LINK_SUPPORTING_DOCUMENTS_ID = "link-supporting-documents"
    ULTIMATE_END_USER_LINK = "link-ultimate_end_users"  # ID
    GOODS_ON_APPLICATION = "[id^=good-on-application-row]"  # CSS
    GOV_TABLES = ".govuk-table__body"  # CSS
    DELETE_END_USER_DOCUMENT = "end_user_document_delete"  # ID
    ATTACH_END_USER_DOCUMENT = "end_user_attach_doc"  # ID
    LINK_COUNTRIES_MATRIX_ID = "link-countries-matrix"
    REMOVE_GOOD_LINK = "a[href*='good-on-application']"
    REMOVE_GOODS_TYPE_LINK = "a[href*='goods-types/remove']"
    REMOVE_END_USER_LINK = "a[href*='remove']"
    REMOVE_CONSIGNEE_LINK = "a[href*='remove']"
    REMOVE_THIRD_PARTY_LINK = "a[href*='remove']"
    REMOVE_ADDITIONAL_DOCUMENT_LINK = "document_delete"  # ID
    LITE_TASK_LIST_ITEMS = ".lite-task-list__items"
    DELETE_ADDITIONAL_DOC_CONFIRM_YES = "delete_document_confirmation-yes"  # ID

    def click_supporting_documents_link(self):
        self.driver.find_element_by_id(self.LINK_SUPPORTING_DOCUMENTS_ID).click()

    def find_remove_goods_type_link(self):
        try:
            return self.driver.find_element_by_css_selector(self.REMOVE_GOODS_TYPE_LINK)
        except NoSuchElementException:
            return None

    def get_remove_good_link(self):
        return self.driver.find_element_by_css_selector(self.REMOVE_GOOD_LINK)

    def find_remove_end_user_link(self):
        try:
            return self.driver.find_element_by_css_selector(self.REMOVE_END_USER_LINK)
        except NoSuchElementException:
            return None

    def does_remove_end_user_exist(self, driver):
        return element_with_css_selector_exists(driver, self.REMOVE_END_USER_LINK)

    def find_remove_consignee_link(self):
        try:
            return self.driver.find_element_by_css_selector(self.REMOVE_CONSIGNEE_LINK)
        except NoSuchElementException:
            return None

    def does_remove_consignee_exist(self, driver):
        return element_with_css_selector_exists(driver, self.REMOVE_CONSIGNEE_LINK)

    def find_remove_third_party_link(self):
        try:
            return self.driver.find_element_by_css_selector(self.REMOVE_THIRD_PARTY_LINK)
        except NoSuchElementException:
            return None

    def find_remove_additional_document_link(self):
        try:
            return self.driver.find_element_by_id(self.REMOVE_ADDITIONAL_DOCUMENT_LINK)
        except NoSuchElementException:
            return None

    def does_remove_additional_document_exist(self, driver):
        return element_with_id_exists(driver, self.REMOVE_ADDITIONAL_DOCUMENT_LINK)

    def confirm_delete_additional_document(self):
        self.driver.find_element_by_id(self.DELETE_ADDITIONAL_DOC_CONFIRM_YES).click()
        functions.click_submit(self.driver)

    def click_application_details_link(self):
        self.driver.find_element_by_id(self.LINK_EXHIBITION_DETAILS_ID).click()

    def click_application_locations_link(self):
        self.driver.execute_script("document.getElementById('" + self.LOCATION_LINK + "').scrollIntoView(true);")
        self.driver.find_element_by_id(self.LOCATION_LINK).click()

    def click_goods_type_link(self):
        self.driver.execute_script("document.getElementById('" + self.OPEN_GOODS_LINK + "').scrollIntoView(true);")
        element = self.driver.find_element_by_id(self.OPEN_GOODS_LINK)
        self.driver.execute_script("arguments[0].click();", element)

    def click_end_user_link(self):
        self.driver.find_element_by_id(self.LINK_END_USER_ID).click()

    def click_consignee_link(self):
        self.driver.find_element_by_id(self.LINK_CONSIGNEE_ID).click()

    def click_goods_countries_link(self):
        self.driver.execute_script(
            "document.getElementById('" + self.LINK_COUNTRIES_MATRIX_ID + "').scrollIntoView(true);"
        )
        self.driver.find_element_by_id(self.LINK_COUNTRIES_MATRIX_ID).click()

    def get_text_of_end_user_table(self):
        return self.driver.find_elements_by_css_selector(self.GOV_TABLES)[
            len(self.driver.find_elements_by_css_selector(self.GOV_TABLES)) - 1
        ].text

    def click_delete_end_user_document(self):
        self.driver.find_element_by_id(self.DELETE_END_USER_DOCUMENT).click()

    def attach_end_user_document_is_present(self):
        return self.driver.find_elements_by_id(self.ATTACH_END_USER_DOCUMENT)

    def get_text_of_lite_task_list_items(self):
        return self.driver.find_element_by_css_selector(self.LITE_TASK_LIST_ITEMS).text

    def click_notes(self):
        self.driver.find_element_by_id(self.LINK_NOTES_ID).click()

    def check_good_section_status(self, status):
        assert status == self.driver.find_element_by_id(self.SECTION_GOOD_STATUS_ID).get_attribute("data-status")

    def check_end_user_section_status(self, status):
        assert status == self.driver.find_element_by_id(self.SECTION_END_USER_STATUS_ID).get_attribute("data-status")

    def check_third_party_section_status(self, status):
        assert status == self.driver.find_element_by_id(self.SECTION_THIRD_PARTIES_STATUS_ID).get_attribute(
            "data-status"
        )

    def check_consignee_section_status(self, status):
        assert status == self.driver.find_element_by_id(self.SECTION_CONSIGNEE_STATUS_ID).get_attribute("data-status")

    def check_supporting_documents_section_status(self, status):
        assert status == self.driver.find_element_by_id(self.SECTION_SUPPORTING_DOCUMENT_STATUS_ID).get_attribute(
            "data-status"
        )

    def check_exhibition_details_section_status(self, status):
        assert status == self.driver.find_element_by_id(self.SECTION_EXHIBITION_DETAILS_STATUS_ID).get_attribute(
            "data-status"
        )
