from selenium.webdriver.common.by import By

class ProfilePageLocators:
  
    LINK_HISTORY = By.XPATH, ".//a[text()='История заказов']"
    BUTTON_LOGOUT = By.XPATH, ".//button[text()='Выход']"
    TEXT_PROFILE_HINT = By.XPATH, ".//p[text()='В этом разделе вы можете изменить свои персональные данные']"
    DIV_ORDER_HISTORY = By.XPATH, ".//div[contains(@class, 'OrderHistory_orderHistory')]/ul[1]"
    DIV_LOADING = By.XPATH, ".//div[text()='Загрузка...']"
    P_ORDER_HISTORY_ITEM_TEXT = By.XPATH, "(.//div[contains(@class, 'OrderHistory_textBox')])[last()]/p[1]"