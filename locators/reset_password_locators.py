from selenium.webdriver.common.by import By

class ResetPasswordLocators:

    LABEL_CONFIRMATION_CODE = By.XPATH, ".//label[text()='Введите код из письма']"
    SVG_SHOW_HIDE_PASSWORD = By.XPATH, ".//div[contains(@class, 'input_type_password')]/div"
    INPUT_PASSWORD_ACTIVE = By.XPATH, "(.//div[@class='input__container'])[1]/div[contains(@class, 'input_status_active')]"