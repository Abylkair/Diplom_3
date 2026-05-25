import allure
import random
from selenium.webdriver.support import expected_conditions as ec
from pages.base_page import BasePage
from locators.main_page_locators import MainPageLocators
from locators.general_locators import GeneralLocators
from data import URL

class MainPage(BasePage):
    
    BASE_URL = URL.MAIN_PAGE
    
    def _get_random_ingredient_locator(self, ingredient_type='bun'):
        ingredient_locator = MainPageLocators.LINK_INGREDIENTS
        self.wait_for_visibility(ingredient_locator)
        ingredients = self.driver.find_elements(*ingredient_locator)
        ingredients_count = len(ingredients)
        
        if ingredients_count == 0:
            raise AssertionError('Список ингредиентов пуст')
        
        if ingredient_type == 'bun':
            index = random.randint(1, min(2, ingredients_count))
        elif ingredient_type == 'ingredient':
            index = random.randint(3, ingredients_count)
        else:
            raise TypeError(f'Неизвестный тип ингредиента: {ingredient_type}')
        
        return ingredient_locator[0], f'{ingredient_locator[1]}[{index}]'
    
    @allure.step('Клик по случайному ингредиенту')
    def click_random_ingredient(self):
        locator = self._get_random_ingredient_locator('ingredient')
        self.wait_for_visibility(locator)
        self.click_to_element(locator)

    @allure.step('Проверка отображения окна деталей')
    def is_details_popup_displayed(self):
        try:
            popup = self.find_visible_element(MainPageLocators.SECTION_INGREDIENT_DETAILS)
            return popup is not None
        except Exception:
            return False
    
    @allure.step('Закрыть окно деталей')
    def close_details_popup(self):
        try:
            close_button = self.wait.until(ec.element_to_be_clickable(MainPageLocators.BUTTON_POPUP_CLOSE))
            self.driver.execute_script("arguments[0].click();", close_button)
        except Exception:
            try:
                self.driver.execute_script("document.querySelector('.Modal_modal_opened button').click()")
            except Exception:
                pass
        self.wait_for_invisibility(MainPageLocators.SECTION_INGREDIENT_DETAILS)

    @allure.step('Добавить ингредиент в заказ')
    def add_ingredient_to_order(self, ingredient_type='bun'):
        locator_from = self._get_random_ingredient_locator(ingredient_type)
        count_locator = locator_from[0], f'{locator_from[1]}/div[1]/p'
        count_before = self.get_text_from_element(count_locator)
        locator_to = MainPageLocators.SECTION_CONSTRUCTOR_BASKET
        self.drag_and_drop(locator_from, locator_to)
        count_after = self.get_text_from_element(count_locator)
        
        if count_before is None or count_after is None:
            raise AssertionError('Не удалось получить количество ингредиентов')
        
        if ingredient_type == 'bun':
            expected_diff = 2
        elif ingredient_type == 'ingredient':
            expected_diff = 1
        else:
            raise TypeError(f'Неизвестный тип: {ingredient_type}')
        
        return int(count_after) - int(count_before) == expected_diff

    @allure.step('Создать новый заказ')
    def create_new_order(self, ingredient_count=1):
        self.add_ingredient_to_order('bun')
        
        for _ in range(ingredient_count):
            self.add_ingredient_to_order('ingredient')
        
        self.click_to_element(MainPageLocators.BUTTON_CREATE_ORDER)
        self.wait_for_visibility(MainPageLocators.IMG_TICK_ANIMATION)
        
        number_locator = MainPageLocators.H2_ORDER_NUMBER_TITLE
        default_number = self.get_text_from_element(number_locator)
        
        try:
            self.wait.until_not(
                lambda d: self.get_text_from_element(number_locator) == default_number
            )
            order_number = self.get_text_from_element(number_locator)
            return True, order_number
        except Exception:
            return False, self.get_text_from_element(number_locator)

    @allure.step('Переход в личный кабинет')
    def navigate_to_profile_page(self):
        self.click_to_element(GeneralLocators.LINK_PROFILE)
        from pages.profile_page import ProfilePage
        return ProfilePage(self.driver)
    
    @allure.step('Переход в ленту заказов')
    def navigate_to_order_feed_page(self):
        self.click_to_element(GeneralLocators.LINK_ORDER_FEED)
        from pages.order_feed_page import OrderFeedPage
        return OrderFeedPage(self.driver)
    
    @allure.step('Проверка авторизации')
    def is_auth(self):
        return bool(self.find_visible_element(MainPageLocators.BUTTON_CREATE_ORDER))
    
    @allure.step('Проверка загрузки страницы')
    def _verify_page_loaded(self):
        return bool(self.find_visible_element(MainPageLocators.LINK_CONSTRUCTOR_ACTIVE))