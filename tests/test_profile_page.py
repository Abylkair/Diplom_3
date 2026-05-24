import allure


@allure.tag('profile')
@allure.title('Тестовые сценарии страницы профиля')
class TestProfilePage:
    
    @allure.title('Проверка перехода на страницу профиля')
    @allure.description('Авторизоваться, перейти в профиль, проверить загрузку')
    def test_profile_page_open_success(self, create_user, login_page):
        email, password = create_user()
        login_page.open()
        main_page = login_page.auth(email, password)
        
        profile_page = main_page.navigate_to_profile_page()
        
        assert profile_page.is_loaded(), 'Страница профиля не загрузилась'
        
    @allure.title('Проверка перехода в историю заказов')
    @allure.description('Создать заказ, перейти в историю заказов, проверить отображение')
    def test_profile_page_show_orders_history_success(self, create_user, login_page):
        email, password = create_user()
        login_page.open()
        main_page = login_page.auth(email, password)
        main_page.create_new_order()
        profile_page = main_page.navigate_to_profile_page()
        
        profile_page.show_orders_history()
        
        assert profile_page.is_orders_history_displayed(), 'История заказов не отображается'

    @allure.title('Проверка выхода из профиля')
    @allure.description('Авторизоваться, выйти из профиля, проверить переход на страницу логина')
    def test_profile_page_logout_success(self, create_user, login_page):
        email, password = create_user()
        login_page.open()
        main_page = login_page.auth(email, password)
        profile_page = main_page.navigate_to_profile_page()
        
        profile_page.logout()
        
        assert login_page.is_loaded(), 'Страница логина не загрузилась после выхода'