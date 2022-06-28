import requests, dateutil.parser, json
import errors


class User:
    """Represents a user on the site. Can submit and view scores, use at your own risk.

    :param username: The username of the account.
    :type username: class:`str`

    :param password: The password of the account, if not provided then you can't submit scores.
    :type password: str, optional
    """
    session = requests.Session() # Use a session, obviously
    loggedIn = False
    id = None
    created_at = None

    def __init__(self, username: str, password: str = None):
        """Initialize the User object"""
        self.username = username
        self.password = password
        try:
            r = self.session.get("https://humanbenchmark.com/api/v4/users/{0}".format(self.username))
        except:
           # insert exception here
            del self
        else:
            self.id = r["id"]
            self.created_at = dateutil.parser.isoparse(r["createdAt"])

    def login(self, password=None):
        """Attempt to log in to the account.

        :param password: If no password was provided during initialization, this will be used to login.
        :type password: str, optional

        :raises errors.LoginFailedException: Username or password provided was incorrect or could not connect to the servers.
        :raises errors.NoPasswordException: No password was provided.
        """
        old_password = self.password
        if not self.password and password:
            self.password = password
        if self.password:
            try:
                r = self.session.post("https://humanbenchmark.com/api/v4/session",
                                      json={"username": self.username, "password": self.password})

            except requests.exceptions.RequestException or requests.exceptions.ConnectionError:
                raise errors.LoginFailedException()
            else:
                self.loggedIn = True
        else:
            raise errors.NoPasswordException()

    def submitScore(self, test_id: str, score: int):
        """Submits a score to the site. Use at your own risk.

        :param test_id: A valid test ID on the website. Valid test IDs: `chimp, sequence, verbal-memory, aim, typing, memory, number-memory, reactiontime`
        :type test_id: class:`str`

        :param score: A score value. Warning: Large numbers like 10^1500 may make the dashboard unusable on that account.
        :type score: class:`int`

        :raises errors.UnauthenticatedException: The user is not logged in.
        """
        if not self.loggedIn:
            raise errors.UnauthenticatedException()
        else:
            r = self.session.post("https://humanbenchmark.com/api/v4/scores",
                                  json={"testId": test_id, "score": score})
            if r.status_code != 200:
                # idk just put an exception here
                pass

    def lookupScores(self, amount=None):
        """Lookup scores of the user. Authentication is not required for this method.
        :param amount: The amount of scores to retrieve, from latest to oldest.
        :type amount: int, optional

        :return: A list of scores, from latest to oldest.
        :rtype: list
        """
        try:
            r = self.session.get("https://humanbenchmark.com/api/v4/users/{0}/scores/".format(self.id))
        except:
            # insert exception here
            pass
        else:
            if amount:
                return json.loads(r.text)[:amount]
            else:
                return json.loads(r.text)

    def logout(self):
        """Log out of the account."""
        try:
            r = self.session.delete("https://humanbenchmark.com/api/v4/session")
        except:
            # raise exception
            pass
        else:
            pass


