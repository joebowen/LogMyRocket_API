class UserAlreadyExistsError(Exception):
    def __init__(self):
        Exception.__init__(self, "A user with that user name already exists.")


class UnableToPerformOperationError(Exception):
    def __init__(self):
        Exception.__init__(self, "Unable to perform the requested operation.")


class MissingPasswordError(Exception):
    def __init__(self):
        Exception.__init__(self, "Missing password in the request.")


class UserDoesNotExistError(Exception):
    def __init__(self):
        Exception.__init__(self, "The user does not exist.")


class UsersDoNotExistError(Exception):
    def __init__(self, user_ids):
        Exception.__init__(self, "The following user ids do not exist: %s" % user_ids)


class UserAuthError(Exception):
    def __init__(self):
        Exception.__init__(self, "User authentication error.")


class AuthRequiredError(Exception):
    def __init__(self):
        Exception.__init__(self, "Request does not contain an access token.")


class InvalidTokenError(Exception):
    def __init__(self):
        Exception.__init__(self, "Invalid token error.")


class PermissionsError(Exception):
    def __init__(self):
        Exception.__init__(self, "User does not have permissions to access this resource.")


class UnableToPerformOperationError(Exception):
    def __init__(self):
        Exception.__init__(self, "Unable to perform the requested operation.")


class MissingUserIdError(Exception):
    def __init__(self):
        Exception.__init__(self, "Missing user ID in request.")


class MissingUserIdsError(Exception):
    def __init__(self):
        Exception.__init__(self, "Missing user IDs in request.")


class MissingUsernameError(Exception):
    def __init__(self):
        Exception.__init__(self, "Missing username in request.")


class MalformedUserObjectError(Exception):
    def __init__(self):
        Exception.__init__(self, "Malformed user object in request.")


class MissingRocketIdError(Exception):
    def __init__(self):
        Exception.__init__(self, "Missing rocket ID in request.")


class RocketDoesNotExistError(Exception):
    def __init__(self):
        Exception.__init__(self, "Rocket model does not exist.")


class MissingRocketIdsError(Exception):
    def __init__(self):
        Exception.__init__(self, "Missing rocket IDs in request.")


class RocketsDoNotExistError(Exception):
    def __init__(self, rocket_ids):
        Exception.__init__(self, "The following rocket ids do not exist: %s" % rocket_ids)
