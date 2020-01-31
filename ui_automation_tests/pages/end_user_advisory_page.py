from pages.shared import Shared
from shared.BasePage import BasePage
from shared.tools import helpers


class EndUserAdvisoryPage(BasePage):

    APPLY_FOR_ADVISORY = "apply"  # id
    TABLE_ROW = ".govuk-table__row"  # css
    CASE_NOTES_TAB = "link-case-notes"  # id
    NOTIFICATION_BUBBLE = ".lite-notification-bubble"  # css

    def click_apply_for_advisories(self):
        self.driver.find_element_by_id(self.APPLY_FOR_ADVISORY).click()

    def open_end_user_advisory(self, end_user_advisory_id):
        end_user_advisory = self.driver.find_element_by_id(end_user_advisory_id)
        end_user_advisory.find_elements_by_css_selector("a")[0].click()

    def is_end_user_advisory_displayed_with_notification(self, end_user_advisory_id):
        end_user_advisory = self.driver.find_element_by_id(end_user_advisory_id)
        return len(end_user_advisory.find_elements_by_css_selector(Shared.NOTIFICATION)) > 0

    def case_note_notification_bubble_text(self):
        tab = self.driver.find_element_by_id(self.CASE_NOTES_TAB)
        return tab.find_element_by_css_selector(self.NOTIFICATION_BUBBLE).text

    def latest_case_note_text(self):
        return self.driver.find_elements_by_css_selector(".lite-application-note")[0].text
