from selenium.webdriver.common.by import By

class GeneralLocators:

    LINK_CONSTRUCTOR = By.XPATH, ".//a[contains(@class, 'AppHeader_header__link')]/p[text()='Конструктор']"
    LINK_ORDER_FEED = By.XPATH, ".//a[contains(@class, 'AppHeader_header__link')]/p[text()='Лента Заказов']"
    LINK_PROFILE = By.XPATH, ".//a[contains(@class, 'AppHeader_header__link')]/p[text()='Личный Кабинет']"