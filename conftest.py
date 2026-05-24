import pytest
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService

@pytest.fixture(params=['chrome', 'firefox'])
def driver(request):
    browser = request.param
    driver_instance = None
    
    browser_width = 1400
    browser_height = 800
    
    print(f"\n=== Запуск браузера: {browser} ===")
    
    if browser == 'chrome':
        options = ChromeOptions()
        options.add_argument("--incognito")
        options.add_argument(f"--window-size={browser_width},{browser_height}")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        service = ChromeService(ChromeDriverManager().install())
        driver_instance = webdriver.Chrome(service=service, options=options)
        
    elif browser == 'firefox':
        options = FirefoxOptions()
        options.add_argument("--private")
        options.add_argument(f"--width={browser_width}")
        options.add_argument(f"--height={browser_height}")
        service = FirefoxService(GeckoDriverManager().install())
        driver_instance = webdriver.Firefox(service=service, options=options)
    
    yield driver_instance
    
    print(f"\n=== Закрытие браузера: {browser} ===")
    driver_instance.quit()


@pytest.fixture
def login_page(driver):
    from pages.login_page import LoginPage
    return LoginPage(driver)


@pytest.fixture
def profile_page(driver):
    from pages.profile_page import ProfilePage
    return ProfilePage(driver)


@pytest.fixture
def forgot_password_page(driver):
    from pages.forgot_password_page import ForgotPasswordPage
    return ForgotPasswordPage(driver)


@pytest.fixture
def main_page(driver):
    from pages.main_page import MainPage
    return MainPage(driver)


@pytest.fixture
def order_feed_page(driver):
    from pages.order_feed_page import OrderFeedPage
    return OrderFeedPage(driver)


@pytest.fixture
def create_user():
    from helpers import generate_unique_email
    from data import URL
    
    users_to_delete = []

    def _create_user():
        email = generate_unique_email()
        password = 'password'
        
        payload = {
            'email': email,
            'password': password,
            'name': 'Test User'
        }
        
        print(f"\n=== Создание пользователя: {email} ===")
        
        response = requests.post(
            url=f'{URL.API_AUTH}/register',
            json=payload
        )
        
        if response.status_code == 200:
            users_to_delete.append(email)
            print(f"=== Пользователь {email} успешно создан ===")
            return email, password
        else:
            print(f"=== Ошибка создания пользователя: {response.text} ===")
            raise Exception(f"Failed to create user: {response.text}")
    
    yield _create_user
    
    for email in users_to_delete:
        try:
            print(f"\n=== Удаление пользователя: {email} ===")
            login_response = requests.post(
                url=f'{URL.API_AUTH}/login',
                json={'email': email, 'password': 'password'}
            )
            if login_response.status_code == 200:
                token = login_response.json()['accessToken']
                delete_response = requests.delete(
                    url=f'{URL.API_AUTH}/user',
                    headers={'Authorization': token}
                )
                if delete_response.status_code == 200:
                    print(f"=== Пользователь {email} успешно удален ===")
                else:
                    print(f"=== Ошибка удаления: {delete_response.text} ===")
        except Exception as e:
            print(f"\n=== Не удалось удалить {email}: {e} ===")