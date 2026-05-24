import allure

@allure.tag('password_restore')
@allure.title('Тестовые сценарии страницы сброса пароля')
class TestResetPasswordPage:
    
    @allure.title('Проверка ввода почты и перехода на страницу сброса пароля')
    @allure.description('Ввести email, перейти на страницу сброса пароля')
    def test_reset_password_enter_email_and_submit_success(self, forgot_password_page):
        forgot_password_page.open()
        forgot_password_page.enter_email()
        reset_password_page = forgot_password_page.navigate_to_reset_password_page()
        
        assert reset_password_page.is_loaded(), 'Страница сброса пароля не загрузилась'
        
    @allure.title('Проверка активации поля ввода пароля')
    @allure.description('Кликнуть на кнопку показа пароля, проверить активацию поля')
    def test_reset_password_show_password_input_activate_by_click_success(
        self, forgot_password_page
    ):
        forgot_password_page.open()
        forgot_password_page.enter_email()
        reset_password_page = forgot_password_page.navigate_to_reset_password_page()
        
        assert reset_password_page.is_password_input_activate_by_click(), \
            'Поле ввода пароля не активировалось при клике'