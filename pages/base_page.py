from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains

class BasePage:
    
    BASE_URL = None
    
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.timeout = 10
        self.wait = WebDriverWait(self.driver, self.timeout)

    def open(self):
        if self.BASE_URL:
            self.go_to_url(self.BASE_URL)
        else:
            raise UnboundLocalError("BASE_URL не установлен")

    def go_to_url(self, url):
        self.driver.get(url)

    def find_visible_element(self, locator):
        try:
            element = self.wait_for_visibility(locator)
            return element
        except Exception:
            return None

    def find_invisible_element(self, locator):
        try:
            element = self.wait.until(ec.presence_of_element_located(locator))
            return element
        except Exception:
            return None
    
    def wait_for_visibility(self, locator):
        return self.wait.until(ec.visibility_of_element_located(locator))
        
    def wait_for_invisibility(self, locator):
        return self.wait.until(ec.invisibility_of_element_located(locator))
    
    def scroll_to_element(self, locator):
        element = self.find_visible_element(locator)
        if element:
            try:
                actions = ActionChains(self.driver)
                actions.move_to_element(element).perform()
            except Exception:
                self.driver.execute_script("arguments[0].scrollIntoView();", element)

    def click_to_element(self, locator):
        element = self.wait.until(ec.element_to_be_clickable(locator))
        self.scroll_to_element(locator)
        try:
            element.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", element)

    def set_text_to_element(self, locator, text):
        element = self.find_visible_element(locator)
        if element:
            element.clear()
            element.send_keys(text)
    
    def get_text_from_element(self, locator):
        element = self.find_visible_element(locator)
        if element:
            return element.text
        return None

    def _verify_page_loaded(self) -> bool:
        return True

    def is_loaded(self):
        try:
            return self._verify_page_loaded()
        except Exception:
            return False