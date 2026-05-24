import allure


@allure.tag('order_feed')
@allure.title('Тестовые сценарии страницы ленты заказов')
class TestOrderFeedPage:
    
    @allure.title('Переход на страницу ленты заказов с главной страницы')
    def test_order_feed_page_open_from_main_page_success(self, main_page):
        main_page.open()
        order_feed_page = main_page.navigate_to_order_feed_page()
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
        main_page = login_page.auth(email, password)
        main_page.create_new_order()
        profile_page = main_page.navigate_to_profile_page()
        order_number = profile_page.get_last_order_number_from_history()
        order_feed_page = profile_page.navigate_to_order_feed_page()
        assert order_feed_page.is_order_exists(order_number), \
            f'Заказ {order_number} не найден в ленте заказов'
        
    @allure.title('Увеличение глобального счетчика заказов')
    def test_order_feed_page_create_order_global_counter_increased(
        self, login_page, create_user
    ):
        email, password = create_user()
        login_page.open()
        main_page = login_page.auth(email, password)
        order_feed_page = main_page.navigate_to_order_feed_page()
        global_counter_before = int(order_feed_page.get_orders_global_counter())
        order_feed_page.navigate_to_main_page()
        main_page.create_new_order()
        main_page.navigate_to_order_feed_page()
        order_feed_page.wait_for_global_counter_increase(global_counter_before)
        global_counter_after = int(order_feed_page.get_orders_global_counter())
        assert global_counter_after > global_counter_before, \
            f'Глобальный счетчик не увеличился: {global_counter_before} -> {global_counter_after}'
        
    @allure.title('Увеличение счетчика заказов за сегодня')
    def test_order_feed_page_create_order_today_counter_increased(
        self, login_page, create_user
    ):
        email, password = create_user()
        login_page.open()
        main_page = login_page.auth(email, password)
        order_feed_page = main_page.navigate_to_order_feed_page()
        today_counter_before = int(order_feed_page.get_orders_today_counter())
        order_feed_page.navigate_to_main_page()
        main_page.create_new_order()
        main_page.navigate_to_order_feed_page()
        order_feed_page.wait_for_today_counter_increase(today_counter_before)
        today_counter_after = int(order_feed_page.get_orders_today_counter())
        assert today_counter_after > today_counter_before, \
            f'Счетчик за сегодня не увеличился: {today_counter_before} -> {today_counter_after}'
        
    @allure.title('Наличие заказа в списке "В работе"')
    def test_order_feed_page_create_order_progress_list_contains_order(
        self, login_page, create_user
    ):
        email, password = create_user()
        login_page.open()
        main_page = login_page.auth(email, password)
        _, order_create_number = main_page.create_new_order()
        order_feed_page = main_page.navigate_to_order_feed_page()
        order_feed_page.wait_for_order_in_progress(int(order_create_number))
        order_numbers_in_progress = order_feed_page.get_all_orders_in_progress_numbers()
        order_numbers_in_progress_int = [int(num) for num in order_numbers_in_progress]
        assert int(order_create_number) in order_numbers_in_progress_int, \
            f'Номер заказа {order_create_number} не найден в списке "В работе". Найдены номера: {order_numbers_in_progress_int}'