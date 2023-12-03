from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def wait_for_element(self, by, locator, timeout=10):
        wait = WebDriverWait(self.driver, timeout)
        try:
            return wait.until(EC.visibility_of_element_located((by, locator)))
        except TimeoutException:
            raise

    def element_to_be_clickable(self, by, locator, timeout=10):
        wait = WebDriverWait(self.driver, timeout)
        try:
            return wait.until(EC.element_to_be_clickable((by, locator)))
        except TimeoutException:
            raise

    def open_url(self, url):
        self.driver.get(url)


class SearchPage(BasePage):
    SEARCH_BOX = (By.ID, 'search')
    SUBMIT_BUTTON = (By.CSS_SELECTOR, 'button.search-form__button')

    def search_for_package(self, package_name):
        search_box = self.wait_for_element(*self.SEARCH_BOX)
        search_box.send_keys(package_name)

        submit_button = self.wait_for_element(*self.SUBMIT_BUTTON)
        submit_button.click()


class ResultsPage(BasePage):
    RESULT_LINK = (By.XPATH, '//h3[@class="package-snippet__title"]//span[@class="package-snippet__name"]')
    RESULT_TITLE = (By.XPATH, '//*[@id="content"]/div[1]/div/div[1]/h1')

    def open_first_result(self):
        self.element_to_be_clickable(*self.RESULT_LINK).click()

    def get_first_result_title(self, timeout=10):
        try:
            result_title = self.wait_for_element(*self.RESULT_TITLE, timeout)
            return result_title.text
        except TimeoutException as e:
            print(f"Timed out waiting for element: {e}")
            return None


def test_search_and_verify_result():

    driver = webdriver.Chrome()

    search_page = SearchPage(driver)
    results_page = ResultsPage(driver)

    search_page.open_url("https://pypi.org/")
    search_page.search_for_package("pytest")

    results_page.open_first_result()

    expected_title = "pytest"
    actual_title = results_page.get_first_result_title(timeout=15)

    print("Expected title:", expected_title)
    print("Actual title:", actual_title)

    if actual_title and expected_title.lower() in actual_title.lower():
        print("Test passed!")
    else:
        print("Test failed: Title mismatch or element not found.")

    driver.quit()


test_search_and_verify_result()
