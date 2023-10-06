from src.exceptions import BadRequest, NotAuthenticated, PermissionDenied


class AuthRequired(NotAuthenticated):
    DETAIL = "Authentication required."


class AuthorizationFailed(PermissionDenied):
    DETAIL = "Authorization failed. User has no access."


class InvalidToken(NotAuthenticated):
    DETAIL = "Invalid token."


class InvalidCredentials(NotAuthenticated):
    DETAIL = "Invalid credentials."


class EmailTaken(BadRequest):
    DETAIL = "Email is already taken."


class UsernameTaken(BadRequest):
    DETAIL = "Username is already taken."


class RefreshTokenNotValid(NotAuthenticated):
    DETAIL = "Refresh token is not valid."


class AccessTokenNotValid(NotAuthenticated):
    DETAIL = "Access token is not valid."
