import allure
from pages.main_page import MainPage
from pages.order_feed_page import OrderFeedPage
from pages.profile_page import ProfilePage

@allure.tag('order_feed')
@allure.title('Тестовые сценарии страницы ленты заказов')
class TestOrderFeedPage:
    
    @allure.title('Переход на страницу ленты заказов с главной страницы')
    def test_order_feed_page_open_from_main_page_success(self, main_page):
        main_page.open()
        main_page.click_order_feed_link()
        order_feed_page = OrderFeedPage(main_page.driver)
        assert order_feed_page.is_loaded(), 'Страница ленты заказов не загрузилась'
        
    @allure.title('Появление окна с деталями заказа')
    def test_order_feed_page_order_details_popup_displayed(self, order_feed_page):
        order_feed_page.open()
        order_feed_page.click_random_order()
        assert order_feed_page.is_details_popup_displayed(), 'Окно с деталями заказа не появилось'
        
    @allure.title('Наличие заказа из истории пользователя в ленте заказов')
    def test_order_feed_page_user_order_history_in_order_feed_contains(
        self, login_page, create_user
    ):
        email, password = create_user()
        login_page.open()
        login_page.auth(email, password)
        main_page = MainPage(login_page.driver)
        main_page.create_new_order()
        main_page.click_profile_link()
        profile_page = ProfilePage(main_page.driver)
        order_number = profile_page.get_last_order_number_from_history()
        profile_page.click_order_feed_link()
        order_feed_page = OrderFeedPage(profile_page.driver)
        assert order_feed_page.is_order_exists(order_number), \
            f'Заказ {order_number} не найден в ленте заказов'
        
    @allure.title('Увеличение глобального счетчика заказов')
    def test_order_feed_page_create_order_global_counter_increased(
        self, login_page, create_user
    ):
        email, password = create_user()
        login_page.open()
        login_page.auth(email, password)
        main_page = MainPage(login_page.driver)
        main_page.click_order_feed_link()
        order_feed_page = OrderFeedPage(main_page.driver)
        global_counter_before = int(order_feed_page.get_orders_global_counter())
        order_feed_page.click_constructor_link()
        main_page = MainPage(order_feed_page.driver)
        main_page.create_new_order()
        main_page.click_order_feed_link()
        order_feed_page = OrderFeedPage(main_page.driver)
        global_counter_after = int(order_feed_page.get_orders_global_counter())
        assert global_counter_after > global_counter_before, \
            f'Глобальный счетчик не увеличился: {global_counter_before} -> {global_counter_after}'
        
    @allure.title('Увеличение счетчика заказов за сегодня')
    def test_order_feed_page_create_order_today_counter_increased(
        self, login_page, create_user
    ):
        email, password = create_user()
        login_page.open()
        login_page.auth(email, password)
        main_page = MainPage(login_page.driver)
        main_page.click_order_feed_link()
        order_feed_page = OrderFeedPage(main_page.driver)
        today_counter_before = int(order_feed_page.get_orders_today_counter())
        order_feed_page.click_constructor_link()
        main_page = MainPage(order_feed_page.driver)
        main_page.create_new_order()
        main_page.click_order_feed_link()
        order_feed_page = OrderFeedPage(main_page.driver)
        today_counter_after = int(order_feed_page.get_orders_today_counter())
        assert today_counter_after > today_counter_before, \
            f'Счетчик за сегодня не увеличился: {today_counter_before} -> {today_counter_after}'
        
    @allure.title('Созданный заказ отображается в истории заказов')
    def test_order_feed_page_create_order_progress_list_contains_order(
        self, login_page, create_user
    ):
        email, password = create_user()
        login_page.open()
        login_page.auth(email, password)
        main_page = MainPage(login_page.driver)
        _, order_create_number = main_page.create_new_order()
        
        main_page.click_profile_link()
        profile_page = ProfilePage(main_page.driver)
        history_order_number = profile_page.get_last_order_number_from_history()
        clean_history_number = history_order_number.lstrip('#').lstrip('0')
        
        assert int(clean_history_number) == int(order_create_number), \
            f'Номер заказа {order_create_number} не совпадает с номером в истории {history_order_number}'