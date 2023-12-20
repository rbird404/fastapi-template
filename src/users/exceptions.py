from src.common.exceptions import BadRequest


class EmailTaken(BadRequest):
    DETAIL = "Email is already taken."


class UsernameTaken(BadRequest):
    DETAIL = "Username is already taken."
