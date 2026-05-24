import allure
from pages.base_page import BasePage
from locators.profile_page_locators import ProfilePageLocators
from locators.general_locators import GeneralLocators
from data import URL

class ProfilePage(BasePage):

    BASE_URL = URL.PROFILE_PAGE

    @allure.step('Показать историю заказов')
    def show_orders_history(self):
        self.click_to_element(ProfilePageLocators.LINK_HISTORY)
        self.wait_for_invisibility(ProfilePageLocators.DIV_LOADING)
    
    @allure.step('Проверка отображения истории заказов')
    def is_orders_history_displayed(self):
        return bool(self.find_invisible_element(ProfilePageLocators.DIV_ORDER_HISTORY))
    
    @allure.step('Получение последнего номера заказа из истории')
    def get_last_order_number_from_history(self):
        self.show_orders_history()
        return self.get_text_from_element(ProfilePageLocators.P_ORDER_HISTORY_ITEM_TEXT)

    @allure.step('Выход из системы')
    def logout(self):
        self.click_to_element(ProfilePageLocators.BUTTON_LOGOUT)
    
    @allure.step('Переход в ленту заказов')
    def navigate_to_order_feed_page(self):
        self.click_to_element(GeneralLocators.LINK_ORDER_FEED)
        
        from pages.order_feed_page import OrderFeedPage
        destination_page = OrderFeedPage(self.driver)
        
        assert destination_page.is_loaded(), 'Страница ленты заказов не загрузилась'
        return destination_page
            
    @allure.step('Проверка загрузки страницы')
    def _verify_page_loaded(self):
        return bool(self.find_visible_element(ProfilePageLocators.TEXT_PROFILE_HINT))