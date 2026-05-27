import allure
import random
import re
from selenium.webdriver.support import expected_conditions as ec
from pages.base_page import BasePage
from locators.order_feed_locators import OrderFeedLocators
from locators.general_locators import GeneralLocators
from data import URL

class OrderFeedPage(BasePage):
    
    BASE_URL = URL.ORDER_FEED_PAGE
    
    def _get_random_order_locator(self):
        orders_locator = OrderFeedLocators.LINK_ORDERS
        self.wait_for_visibility(orders_locator)
        orders = self.driver.find_elements(*orders_locator)
        orders_count = len(orders)
        if orders_count == 0:
            raise AssertionError('Список заказов пуст')
        index = random.randint(1, orders_count)
        return orders_locator[0], f'{orders_locator[1]}[{index}]'
    
    @allure.step('Клик по случайному заказу')
    def click_random_order(self):
        locator = self._get_random_order_locator()
        self.wait_for_visibility(locator)
        self.click_to_element(locator)

    @allure.step('Проверка отображения окна деталей заказа')
    def is_details_popup_displayed(self):
        try:
            self.find_visible_element(OrderFeedLocators.SECTION_ORDER_DETAILS)
            return True
        except Exception:
            return False

    @allure.step('Проверка наличия заказа в ленте')
    def is_order_exists(self, order_number):
        orders_locator = OrderFeedLocators.LINK_ORDERS
        self.wait_for_visibility(orders_locator)
        orders = self.driver.find_elements(*orders_locator)
        clean_number = str(int(order_number))
        for order in orders:
            order_text = order.text.splitlines()[0]
            order_clean = order_text.lstrip('#').lstrip('0')
            if order_clean == clean_number:
                return True
        return False
    
    @allure.step('Получение глобального счетчика заказов')
    def get_orders_global_counter(self):
        self.wait_for_visibility(OrderFeedLocators.P_ORDERS_GLOBAL_COUNTER)
        return self.get_text_from_element(OrderFeedLocators.P_ORDERS_GLOBAL_COUNTER)
    
    @allure.step('Получение счетчика заказов за сегодня')
    def get_orders_today_counter(self):
        self.wait_for_visibility(OrderFeedLocators.P_ORDERS_TODAY_COUNTER)
        return self.get_text_from_element(OrderFeedLocators.P_ORDERS_TODAY_COUNTER)
    
    @allure.step('Ожидание увеличения глобального счетчика')
    def wait_for_global_counter_increase(self, expected_value):
        self.wait.until(
            lambda d: int(self.get_orders_global_counter()) > expected_value
        )
    
    @allure.step('Ожидание увеличения счетчика за сегодня')
    def wait_for_today_counter_increase(self, expected_value):
        self.wait.until(
            lambda d: int(self.get_orders_today_counter()) > expected_value
        )
    
    @allure.step('Получение всех номеров заказов в работе')
    def get_all_orders_in_progress_numbers(self):
        try:
            self.wait_for_visibility(OrderFeedLocators.LI_ORDERS_IN_PROGRESS)
            order_elements = self.driver.find_elements(*OrderFeedLocators.LI_ORDERS_IN_PROGRESS)
            order_numbers = []
            for element in order_elements:
                try:
                    text = element.text
                    numbers = re.findall(r'\d+', text)
                    if numbers:
                        order_numbers.extend(numbers)
                except Exception:
                    continue
            return order_numbers
        except Exception:
            return []
    
    @allure.step('Клик по ссылке конструктора')
    def click_constructor_link(self):
        self.click_to_element(GeneralLocators.LINK_CONSTRUCTOR)
        return self
    
    @allure.step('Проверка загрузки страницы')
    def _verify_page_loaded(self):
        return bool(self.find_visible_element(OrderFeedLocators.LINK_ORDER_FEED_ACTIVE))