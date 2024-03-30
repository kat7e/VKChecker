class VKCheckerError(Exception):
    """
    Базовый класс для всех ошибок
    """

class FloodControl(VKCheckerError):
    """
    9 Vk api error Flood Contol
    """

class CaptchaError(VKCheckerError):
    """
    Ошибка капчи
    """

class InvalidTokenError(VKCheckerError):
    """
    Ошибка валидации токена
    """

class InvalidAuthError(VKCheckerError):
    """
    Ошибка аутентификации
    """