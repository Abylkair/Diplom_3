class URL:
    
    BASE_URL = 'https://qa-stellarburgers.education-services.ru'
    
    MAIN_PAGE = f'{BASE_URL}'
    LOGIN_PAGE = f'{BASE_URL}/login'
    PROFILE_PAGE = f'{BASE_URL}/account/profile'
    ORDER_FEED_PAGE = f'{BASE_URL}/feed'
    REGISTER_PAGE = f'{BASE_URL}/register'
    FORGOT_PASSWORD_PAGE = f'{BASE_URL}/forgot-password'
    RESET_PASSWORD_PAGE = f'{BASE_URL}/reset-password'
    
    API_AUTH = f'{BASE_URL}/api/auth'


class UserData:
    
    DEFAULT_PASSWORD = 'password'
    DEFAULT_NAME = 'Test User'

