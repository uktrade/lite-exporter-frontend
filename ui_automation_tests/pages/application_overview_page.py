class ApplicationOverviewPage:

    def __init__(self, driver):
        self.driver = driver
        self.location_link = "location"
        self.countries_link = "countries"
        self.goods_link = "goods"
        self.end_user_link = "end_users"   # ID
        self.ultimate_end_user_link = "ultimate_end_users"   # ID
        self.sites_link = "a[href*='sites']"
        self.goods_link = "goods"
        self.show_countries_link = "[onclick*='showCountries']"
        self.modal_close = "modal-close-button"   # ID
        self.modal_content = ".modal-content"   # CSS
        self.gov_tables = ".govuk-table__body"   # CSS
        self.back_to_overview_text = "Back to Application" #link text
        self.submit_application_button = "button[type*='submit']" # CSS
        self.attach_end_user_document_link = "attach_doc" # ID
        self.download_end_user_document = "end_user_document_download" # ID
        self.delete_end_user_document = "end_user_document_delete" # ID


    def click_application_locations_link(self):
        self.driver.execute_script("document.getElementById('" + self.location_link + "').scrollIntoView(true);")
        self.driver.find_element_by_id(self.location_link).click()

    def click_goods_link(self):
        element = self.driver.find_element_by_id(self.goods_link)
        self.driver.execute_script("arguments[0].click();", element)

    def click_sites_link(self):
        self.driver.find_element_by_css_selector(self.sites_link).click()

    def click_end_user_link(self):
        element = self.driver.find_element_by_id(self.end_user_link)
        self.driver.execute_script("arguments[0].click();", element)

    def click_ultimate_end_user_link(self):
        element = self.driver.find_element_by_id(self.ultimate_end_user_link)
        self.driver.execute_script("arguments[0].click();", element)

    def click_countries_link(self):
        self.driver.execute_script("document.getElementById('" + self.countries_link + "').scrollIntoView(true);")
        self.driver.find_element_by_id(self.countries_link).click()

    def get_text_of_countries_selected(self):
        return self.driver.find_element_by_css_selector(self.show_countries_link).text

    def click_on_countries_selected(self):
        self.driver.find_element_by_css_selector(self.show_countries_link).click()

    def click_on_modal_close(self):
        self.driver.find_element_by_id(self.modal_close).click()

    def click_on_back_to_overview_text(self):
        self.driver.find_element_by_link_text(self.back_to_overview_text).click()

    def get_text_of_country_modal_content(self):
        return self.driver.find_element_by_css_selector(self.modal_content).text

    def get_text_of_end_user_table(self):
        return self.driver.find_elements_by_css_selector(self.gov_tables)[len(self.driver.find_elements_by_css_selector(self.gov_tables))-1].text

    def check_submit_is_enabled(self):
        return self.driver.find_element_by_css_selector(self.submit_application_button).is_enabled()

    def click_on_add_end_user_document(self):
        self.driver.find_element_by_id(self.attach_end_user_document_link).click()

    def click_delete_end_user_document(self):
        self.driver.find_element_by_id(self.delete_end_user_document).click()
