from selenium.webdriver.common.by import By

class ForgotPasswordPageLocators:
  
    INPUT_EMAIL = By.XPATH, ".//input[@name='name']"
    BUTTON_SUBMIT_RESTORE = By.XPATH, ".//button[text()='Восстановить']"
    H2_PASSWORD_RESTORING = By.XPATH, ".//h2[text()='Восстановление пароля']"