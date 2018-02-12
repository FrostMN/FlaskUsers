
class User:

    def __init__(self, email=None, email_confirmed = False, account_type="user", first_name=None,
                 last_name=None, lang="eng", pw_hash=None, nonce=None, creation_time=None,
                 session_key=None, user_id=None):
        self.user_id = user_id
        self.email = email
        self.email_confirmed = email_confirmed
        self.account_type = account_type
        self.first_name = first_name
        self.last_name = last_name
        self.pw_hash = pw_hash
        self.nonce = nonce
        self.creation_time = creation_time
        self.session_key = session_key
        self.language = lang

    # def __str__(self) -> str:
    #     return "to string"

    def __str__(self) -> str:
        return super().__str__()



