import time


class SubmittedApplicationsPages:

    def __init__(self, driver):
        self.driver = driver
        self.case_note_field = "case_note"  # id
        self.post_note_btn = "button-post-note"  # id
        self.cancel_note_btn = "case-note-cancel-button"  # id
        self.case_notes_text = ".lite-case-note"  # css
        self.case_note_date_time = ".lite-activity-item .govuk-hint"  # css
        self.case_note_character_warning = "case_note-warning"  # id

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
