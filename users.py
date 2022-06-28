import requests, datetime, dateutil.parser
import exceptions

class User:
    '''Represents a user on the site. Can submit and view scores, use at your own risk.'''
    session = requests.Session()
    loggedIn = False
    id = None
    created_at = None

    def __init__(self, username: str, password: str = None):
        self.username = username
        self.password = password
    def login(self, password=None):
        '''Attempt to log in to the account.
        Password given to the User object during declaration will be used first, then the password argument used in the function will be tried if unsuccessful.'''
        old_password =
        if not self.password and password:
            self.password = password
        '''Attempts to log in to the account.'''
        if self.password:
            try:
                r = session.post("https://humanbenchmark.com/api/v4/session",
                        json={"username": self.username, "password": self.password})

                self.id = r["id"]
                self.created_at = dateutil.parser.isoparse(r["createdAt"])
            except:
                raise exceptions.LoginFailedException()
            else:
                self.loggedIn = True
        else:
            raise exceptions.NoPasswordException()
    def submitScore(self, mode: str, score: int):
        '''Submits a score to the site. Use at your own risk.'''
        if not self.loggedIn:
            raise exceptions.UnauthenticatedException()
        else:
            pass