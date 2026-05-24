from selenium.webdriver.common.by import By

class LoginPageLocators:

    LINK_RESTORE_PASSWORD = By.XPATH, ".//a[text()='Восстановить пароль']"
    H2_LOGIN_TITLE = By.XPATH, ".//h2[text()='Вход']"
    BUTTON_LOGIN = By.XPATH, ".//button[text()='Войти']"
    INPUT_EMAIL = By.XPATH, ".//input[@name='name']"
    INPUT_PASSWORD = By.XPATH, ".//input[@name='Пароль']"