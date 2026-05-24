import allure
from pages.base_page import BasePage
from locators.login_page_locators import LoginPageLocators
from data import URL

class LoginPage(BasePage):
    
    BASE_URL = URL.LOGIN_PAGE
    
    @allure.step('Авторизация пользователя')
    def auth(self, email, password):
        self.set_text_to_element(LoginPageLocators.INPUT_EMAIL, email)
        self.set_text_to_element(LoginPageLocators.INPUT_PASSWORD, password)
        return self.navigate_to_main_page()
    
    @allure.step('Переход на страницу восстановления пароля')
    def navigate_to_forgot_password_page(self):
        self.click_to_element(LoginPageLocators.LINK_RESTORE_PASSWORD)
        
        from pages.forgot_password_page import ForgotPasswordPage
        destination_page = ForgotPasswordPage(self.driver)
        
        assert destination_page.is_loaded(), 'Страница восстановления пароля не загрузилась'
        return destination_page

    @allure.step('Переход на главную страницу')
    def navigate_to_main_page(self):
        self.click_to_element(LoginPageLocators.BUTTON_LOGIN)
        
        from pages.main_page import MainPage
        destination_page = MainPage(self.driver)
        
        assert destination_page.is_loaded(), 'Главная страница не загрузилась'
        return destination_page
    
    @allure.step('Проверка загрузки страницы')
    def _verify_page_loaded(self):
        return bool(self.find_visible_element(LoginPageLocators.H2_LOGIN_TITLE))