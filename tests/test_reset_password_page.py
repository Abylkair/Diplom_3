import allure
from pages.forgot_password_page import ForgotPasswordPage
from pages.reset_password_page import ResetPasswordPage

@allure.tag('password_restore')
@allure.title('Тестовые сценарии страницы сброса пароля')
class TestResetPasswordPage:
    
    @allure.title('Проверка ввода почты и перехода на страницу сброса пароля')
    def test_reset_password_enter_email_and_submit_success(self, forgot_password_page):
        forgot_password_page.open()
        forgot_password_page.enter_email()
        forgot_password_page.click_submit_button()
        reset_password_page = ResetPasswordPage(forgot_password_page.driver)
        assert reset_password_page.is_loaded()
        
    @allure.title('Проверка активации поля ввода пароля')
    def test_reset_password_show_password_input_activate_by_click_success(self, forgot_password_page):
        forgot_password_page.open()
        forgot_password_page.enter_email()
        forgot_password_page.click_submit_button()
        reset_password_page = ResetPasswordPage(forgot_password_page.driver)
        assert reset_password_page.is_password_input_activate_by_click()