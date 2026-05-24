import uuid


def generate_unique_email() -> str:
    """Генерация случайного адреса электронной почты на домене test.com
    Returns:
        str: Адрес электронной почты в формате test_****@test.com
    """
    return f"test_{uuid.uuid4().hex}@test.com"
