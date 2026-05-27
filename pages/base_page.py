from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains

class BasePage:
    
    BASE_URL = None
    
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def open(self):
        if self.BASE_URL:
            self.go_to_url(self.BASE_URL)
        else:
            raise UnboundLocalError("BASE_URL не установлен")

    def go_to_url(self, url):
        self.driver.get(url)

    def find_visible_element(self, locator):
        try:
            return self.wait_for_visibility(locator)
        except Exception:
            return None

    def find_invisible_element(self, locator):
        try:
            return self.wait.until(ec.presence_of_element_located(locator))
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
                self.execute_script("arguments[0].scrollIntoView();", element)

    def click_to_element(self, locator):
        element = self.wait.until(ec.element_to_be_clickable(locator))
        self.scroll_to_element(locator)
        try:
            element.click()
        except Exception:
            self.execute_script("arguments[0].click();", element)

    def set_text_to_element(self, locator, text):
        element = self.find_visible_element(locator)
        if element:
            element.clear()
            element.send_keys(text)
    
    def get_text_from_element(self, locator):
        try:
            element = self.find_visible_element(locator)
            if element:
                return element.text
        except Exception:
            pass
        return None

    def execute_script(self, script, *args):
        return self.driver.execute_script(script, *args)

    def drag_and_drop(self, source_locator, target_locator):
        source = self.wait_for_visibility(source_locator)
        target = self.wait_for_visibility(target_locator)
        self.execute_script("""
            var source = arguments[0];
            var target = arguments[1];
            var evt = document.createEvent("DragEvent");
            evt.initMouseEvent("dragstart", true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);
            source.dispatchEvent(evt);
            evt = document.createEvent("DragEvent");
            evt.initMouseEvent("dragenter", true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);
            target.dispatchEvent(evt);
            evt = document.createEvent("DragEvent");
            evt.initMouseEvent("dragover", true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);
            target.dispatchEvent(evt);
            evt = document.createEvent("DragEvent");
            evt.initMouseEvent("drop", true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);
            target.dispatchEvent(evt);
            evt = document.createEvent("DragEvent");
            evt.initMouseEvent("dragend", true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);
            source.dispatchEvent(evt);
        """, source, target)

    def wait_for_element_clickable(self, locator):
        return self.wait.until(ec.element_to_be_clickable(locator))

    def get_current_url(self):
        return self.driver.current_url

    def _verify_page_loaded(self) -> bool:
        return True

    def is_loaded(self):
        try:
            return self._verify_page_loaded()
        except Exception:
            return False