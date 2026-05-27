import allure
from pages.main_page import MainPage
from pages.profile_page import ProfilePage
from pages.login_page import LoginPage


@allure.tag('profile')
@allure.title('Тестовые сценарии страницы профиля')
class TestProfilePage:
    
    @allure.title('Проверка перехода на страницу профиля')
    @allure.description('Авторизоваться, перейти в профиль, проверить загрузку')
    def test_profile_page_open_success(self, create_user, login_page):
        email, password = create_user()
        login_page.open()
        login_page.auth(email, password)
        main_page = MainPage(login_page.driver)
        
        main_page.click_profile_link()
        profile_page = ProfilePage(main_page.driver)
        
        assert profile_page.is_loaded(), 'Страница профиля не загрузилась'
        
    @allure.title('Проверка перехода в историю заказов')
    @allure.description('Создать заказ, перейти в историю заказов, проверить отображение')
    def test_profile_page_show_orders_history_success(self, create_user, login_page):
        email, password = create_user()
        login_page.open()
        login_page.auth(email, password)
        main_page = MainPage(login_page.driver)
        main_page.create_new_order()
        main_page.click_profile_link()
        profile_page = ProfilePage(main_page.driver)
        
        profile_page.show_orders_history()
        
        assert profile_page.is_orders_history_displayed(), 'История заказов не отображается'

    @allure.title('Проверка выхода из профиля')
    @allure.description('Авторизоваться, выйти из профиля, проверить переход на страницу логина')
    def test_profile_page_logout_success(self, create_user, login_page):
        email, password = create_user()
        login_page.open()
        login_page.auth(email, password)
        main_page = MainPage(login_page.driver)
        main_page.click_profile_link()
        profile_page = ProfilePage(main_page.driver)
        
        profile_page.logout()
        
        assert login_page.is_loaded(), 'Страница логина не загрузилась после выхода'