import allure

@allure.tag('login')
@allure.title('Тестовые сценарии страницы логина')
class TestLoginPage:
    
    @allure.title('Проверка открытия страницы логина')
    @allure.description('Открыть страницу логина, проверить загрузку')
    def test_login_page_open_success(self, login_page):
        login_page.open()
        
        assert login_page.is_loaded(), 'Страница логина не загрузилась'
        
    @allure.title('Проверка авторизации пользователя')
    @allure.description('Создать пользователя, авторизоваться, проверить результат')
    def test_login_page_auth_success(self, create_user, login_page):
        email, password = create_user()
        login_page.open()
        
        main_page = login_page.auth(email, password)
        
        assert main_page.is_loaded(), 'Главная страница не загрузилась после авторизации'
        assert main_page.is_auth(), 'Пользователь не авторизован'