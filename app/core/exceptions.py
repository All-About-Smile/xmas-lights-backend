from typing import Optional


class AppException(Exception):
    """
    비즈니스 로직에서 사용하는 공통 예외
    """

    def __init__(self, code: int, message: str, meta: Optional[dict] = None):
        self.code = code
        self.message = message
        self.meta = meta or {}


class AuthException(AppException):
    """
    인증 실패 (토큰 불일치, 만료 등)
    """

    pass


class PermissionDeniedException(AppException):
    """
    권한 부족 (권한 없는 리소스 접근 등)
    """

    pass


# 에러 코드 모음
class ErrorCodes:
    # Auth
    AUTH_INVALID_TOKEN = 1001
    AUTH_EXPIRED_TOKEN = 1002
    AUTH_REQUIRED = 1003
    AUTH_INVALID_CREDENTIALS = 1004

    # Permission
    PERMISSION_DENIED = 2001

    # User / Resource
    USER_ALREADY_EXISTS = 4001
    USER_NOT_FOUND = 4004
    
    # Letter / Resource
    LETTER_NUMBER_CONFLICT = 4101

    # Validation / Request
    VALIDATION_ERROR = 4220

    # Server
    INTERNAL_ERROR = 9000
