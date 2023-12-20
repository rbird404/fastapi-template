from src.common.exceptions import NotAuthenticated, PermissionDenied


class AuthRequired(NotAuthenticated):
    DETAIL = "Authentication required."


class AuthorizationFailed(PermissionDenied):
    DETAIL = "Authorization failed. User has no access."


class InvalidToken(NotAuthenticated):
    DETAIL = "Invalid token."


class InvalidCredentials(NotAuthenticated):
    DETAIL = "Invalid credentials."
