from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
import time


class ApplicationPage():

    def __init__(self, driver):
        self.driver = driver
        self.case_note_field = "case_note"   # ID
        self.post_note_btn = "button-post-note"   # ID
        self.cancel_note_btn = "case-note-cancel-button"   # ID
        self.case_notes_text = ".lite-case-note"   # CSS
        self.case_note_date_time = ".lite-activity-item .govuk-hint"   # CSS
        self.case_note_character_warning = "case_note-warning"   # ID
        self.progress_app_btn = '.govuk-button[href*="manage"]'
        self.record_decision_btn = '.govuk-button[href*="decide"]'   # CSS
        self.headers = self.driver.find_elements_by_css_selector(".lite-heading-s")   # CSS
        self.activity_case_note_subject = self.driver.find_elements_by_css_selector(".lite-activity-item .govuk-body")
        self.activity_dates = ".lite-activity-item .govuk-hint"
        self.activity_user = ".user"
        self.is_visible_to_exporter_checkbox_id = 'is_visible_to_exporter'
        self.case_note_tab = "case-notes-tab"  # ID
        self.ecju_query_tab = "ecju-queries-tab"  # ID
        self.ecju_queries_open = "open-ecju-query"
        self.ecju_query_response_text = 'Respond to query'
        self.ecju_queries_closed = "closed-ecju-query"
        self.respond = "govuk-link govuk-link--no-visited-state"  # css

    def click_visible_to_exporter_checkbox(self):
        self.driver.find_element_by_id(self.is_visible_to_exporter_checkbox_id).click()

    def enter_case_note(self, text):
        self.driver.find_element_by_id(self.case_note_field).send_keys(text)

    def get_text_of_case_note_field(self):
        return self.driver.find_element_by_id(self.case_note_field).text

    def click_post_note_btn(self):
        self.driver.find_element_by_id(self.post_note_btn).click()

    def click_cancel_btn(self):
        self.driver.find_element_by_id(self.cancel_note_btn).click()

    def get_text_of_case_note(self, no):
        return self.driver.find_elements_by_css_selector(self.case_notes_text)[no].text

    def get_text_of_case_note_date_time(self, no):
        return self.driver.find_elements_by_css_selector(self.case_note_date_time)[no].text

    def get_text_of_case_note_warning(self):
        time.sleep(1)
        return self.driver.find_element_by_id(self.case_note_character_warning).text

    def get_disabled_attribute_of_post_note(self):
        return self.driver.find_element_by_id(self.post_note_btn).get_attribute("disabled")

    def click_progress_application(self):
        self.driver.find_element_by_css_selector(self.progress_app_btn).click()

    def click_record_decision(self):
        self.driver.find_element_by_css_selector(self.record_decision_btn).click()

    def select_status(self, status):
        case_status_dropdown = Select(self.driver.find_element_by_id('status'))
        time.sleep(1)
        case_status_dropdown.select_by_visible_text(status)

    def get_text_of_application_headings(self):
        return self.headers

    def get_text_of_case_note_subject(self, no):
        return self.activity_case_note_subject[no].text

    def get_text_of_activity_dates(self, no):
        return self.driver.find_elements_by_css_selector(self.activity_dates)[no].text

    def get_text_of_activity_users(self, no):
        return self.driver.find_elements_by_css_selector(self.activity_user)[no].text

    def click_case_note_tab(self):
        self.driver.find_element_by_id(self.case_note_tab).click()

    def click_ecju_query_tab(self):
        self.driver.find_element_by_id(self.ecju_query_tab).click()

    def get_count_of_open_ecju_queries(self):
        return len(self.driver.find_elements_by_id(self.ecju_queries_open))

    def get_count_of_closed_ecju_queries(self):
        return len(self.driver.find_elements_by_id(self.ecju_queries_closed))

    def respond_to_ecju_query(self, no):
        response = '//a[contains(text(), "' + self.ecju_query_response_text + '")]'
        self.driver.find_elements_by_xpath(response)[no].click()

    def get_bubble_value(self, text):
        bubble = '//a[contains(text(), "' + text + '")]//div'
        try:
            return int(self.driver.find_element_by_xpath(bubble).text)
        except NoSuchElementException:
            return 0
