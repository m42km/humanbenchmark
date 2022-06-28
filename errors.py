class UnauthenticatedException(Exception):
    def __init__(self):
        super().__init__("The user is not logged in.")
    def __str__(self):
        print("The user is not logged in.")

class NoPasswordException(Exception):
    def __init__(self):
        super().__init__("The user has no password.")
    def __str__(self):
        print("The user has no password.")

class LoginFailedException(Exception):
    def __init__(self):
        super().__init__("Failed to login with credentials provided.")
    def __str__(self):
        print("Failed to login, username and/or password may be incorrect.")
