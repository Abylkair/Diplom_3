import allure
from pages.base_page import BasePage
from locators.forgot_password_page_locator import ForgotPasswordPageLocators
from helpers import generate_unique_email
from data import URL

class ForgotPasswordPage(BasePage):
    
    BASE_URL = URL.FORGOT_PASSWORD_PAGE
    
    @allure.step('Ввод адреса электронной почты')
    def enter_email(self, email=None):
        email = email or generate_unique_email()
        self.set_text_to_element(ForgotPasswordPageLocators.INPUT_EMAIL, email)
    
    @allure.step('Переход на страницу сброса пароля')
    def navigate_to_reset_password_page(self):
        self.click_to_element(ForgotPasswordPageLocators.BUTTON_SUBMIT_RESTORE)
        
        from pages.reset_password_page import ResetPasswordPage
        destination_page = ResetPasswordPage(self.driver)
        
        assert destination_page.is_loaded(), 'Страница сброса пароля не загрузилась'
        return destination_page
    
    @allure.step('Проверка загрузки страницы')
    def _verify_page_loaded(self):
        conditions = [
            self.find_visible_element(ForgotPasswordPageLocators.H2_PASSWORD_RESTORING),
            self.find_visible_element(ForgotPasswordPageLocators.BUTTON_SUBMIT_RESTORE)
        ]
        return all(conditions)