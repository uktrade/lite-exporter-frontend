import conftest


def click_submit(driver: conftest):
    driver.find_element_by_css_selector("button[value='submit']").click()
