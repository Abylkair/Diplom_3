import allure
import pytest

@allure.tag('main')
@allure.title('Тестовые сценарии главной страницы')
class TestMainPage:
    
    @allure.title('Проверка перехода на главную страницу с ленты заказов')
    @allure.description('Открыть страницу ленты заказов, перейти на главную страницу')
    def test_main_page_open_from_order_feed_page_success(self, order_feed_page):
        order_feed_page.open()
        
        main_page = order_feed_page.navigate_to_main_page()
        
        assert main_page.is_loaded(), 'Главная страница не загрузилась'
    
    @allure.title('Проверка появления окна с деталями ингредиента')
    @allure.description('Кликнуть на ингредиент, проверить отображение окна')
    def test_main_page_click_ingredient_details_popup_displayed(self, main_page):
        main_page.open()
        
        main_page.click_random_ingredient()
        
        assert main_page.is_details_popup_displayed(), 'Окно с деталями ингредиента не появилось'
        
    @allure.title('Проверка закрытия окна с деталями ингредиента')
    @allure.description('Закрыть окно с деталями, проверить что оно исчезло')
    def test_main_page_close_details_popup_not_displayed(self, main_page):
        main_page.open()
        main_page.click_random_ingredient()
        
        main_page.close_details_popup()
        
        assert not main_page.is_details_popup_displayed(), 'Окно с деталями ингредиента не закрылось'
        
    @allure.description('Добавить ингредиент к бургеру, проверить увеличение счетчика')
    @pytest.mark.parametrize('ingredient_type', ['bun', 'ingredient'])
    def test_main_page_add_ingredient_increased_count(self, ingredient_type, main_page):
        allure.dynamic.title(f'Проверка добавления ингредиента типа {ingredient_type} в бургер')
        main_page.open()
        
        is_success = main_page.add_ingredient_to_order(ingredient_type)
        
        assert is_success, f'Счетчик ингредиента типа {ingredient_type} не увеличился'

    @allure.description('Создать заказ с разным количеством ингредиентов')
    @pytest.mark.parametrize('ingredient_count', [0, 1, 3])
    def test_main_page_create_order_auth_success(self, ingredient_count, create_user, login_page):
        allure.dynamic.title(f'Проверка создания заказа с {ingredient_count} ингредиентами')
        email, password = create_user()
        login_page.open()
        
        main_page = login_page.auth(email, password)
        is_success, order_number = main_page.create_new_order(ingredient_count)
        
        assert is_success, 'Заказ не был создан'
        assert order_number != '9999', 'Получен некорректный номер заказа'
        assert order_number.isdigit(), 'Номер заказа должен быть числом'