from ui_automation_tests.shared.BasePage import BasePage


class GreatSigninPage(BasePage):
    LOGIN_SECTION_ID = "login-form"
    EMAIL_INPUT_ID = "id_login"
    PASSWORD_INPUT_ID = "id_password"  # noqa
    SUBMIT_BUTTON_CSS_SELECTOR = "button[type='submit']"

    def enter_email(self, form, email):
        email_input = form.find_element_by_id(self.EMAIL_INPUT_ID)
        email_input.clear()
        email_input.send_keys(email)

    def enter_password(self, form, password):
        password_input = form.find_element_by_id(self.PASSWORD_INPUT_ID)
        password_input.clear()
        password_input.send_keys(password)

    def click_sign_in(self, form):
        form.find_element_by_css_selector(self.SUBMIT_BUTTON_CSS_SELECTOR).click()

    def sign_in(self, email, password):
        form = self.driver.find_element_by_id(self.LOGIN_SECTION_ID)
        self.enter_email(form, email)
        self.enter_password(form, password)
        self.click_sign_in(form)

