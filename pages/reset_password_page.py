import allure
from pages.base_page import BasePage
from locators.reset_password_locators import ResetPasswordLocators
from data import URL

class ResetPasswordPage(BasePage):
    
    BASE_URL = URL.RESET_PASSWORD_PAGE
    
    @allure.step('Проверка активации поля ввода пароля')
    def is_password_input_activate_by_click(self):
        self.click_to_element(ResetPasswordLocators.SVG_SHOW_HIDE_PASSWORD)
        return bool(self.find_visible_element(ResetPasswordLocators.INPUT_PASSWORD_ACTIVE))
    
    @allure.step('Проверка загрузки страницы')
    def _verify_page_loaded(self):
        return bool(self.find_visible_element(ResetPasswordLocators.LABEL_CONFIRMATION_CODE))