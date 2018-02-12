import FlaskUsers.utils.database as db
import FlaskUsers.utils.secrets as secrets
from flask_api import status
from config import ITEMS_URL
import requests
import json
from flask import flash


def get_user(user, password, device):  # TODO: need to log session events
    if db.user_exists(user):
        db_hash = db.get_user_hash(user)

        if secrets.bc_checkpw(password, db_hash):
            db_user = db.get_user(user)
            email = user
            confirmed = str(bool(db_user.email_confirmed)).lower()
            first_name = db_user.first_name
            last_name = db_user.last_name
            account_type = str(db_user.account_type)
            usr_id = str(db_user.user_id)
            key = str(db_user.session_key)
            language = db_user.language
            login_json = \
                "{ \"error\": false, \"email\": \"" + email + "\", \"email_confirmed\": \"" + confirmed + "\"," \
                " \"first_name\": \"" + first_name + "\", \"last_name\": \"" + last_name + "\", \"type\": " + \
                account_type + ", \"UserID\": " + usr_id + ", \"session_key\": \"" + key + "\", \"language\": \"" + \
                language + "\", \"message\": \"You were successfully logged in.\" }"

            return login_json, status.HTTP_200_OK
        else:
            return "{ \"error\": true, \"message\": \"Bad username or password\" }", status.HTTP_401_UNAUTHORIZED
    else:
        return "{ \"error\": true, \"message\": \"Bad username or password\" }", status.HTTP_401_UNAUTHORIZED


def start_session(user_id, key, admin, device):
    print("in start_session()")
    print("admin: ")
    print(admin)
    key_query = "INSERT INTO session_keys (user_id, session_key, active, admin, device) VALUES (%s, %s, 1, %s, %s)"
    db.execute_query(key_query, (user_id, key, admin, device))
    start_items_session(user_id, key, admin, device)
    event = "Login From - {}".format(device)
    log_session_event(key, event + " from funct")
    print("user: {}, key: {}, device: {}".format(user_id, key, device))


def end_session(key, device):
    key_query = "UPDATE session_keys SET active = 0 WHERE session_key = %s"
    db.execute_query(key_query, (key, ))
    end_items_session(key)
    event = "Logout From - {}".format(device)
    log_session_event(key, event + " from funct")


#  TODO: implement this
def session_active(key):
    return True


def log_session_event(session_key, event):
    event_query = "INSERT INTO session_events (session_key, event) VALUES (%s, %s)"
    db.execute_query(event_query, (session_key, event))


def start_items_session(user_id, key, admin, device):
    items_url = "{}/session".format(ITEMS_URL)
    print("in start_item_session():")
    print("admin: ")
    print(admin)
    post_data = {"action": "start", "user_id": user_id, "session_key": key, "admin": admin, "device": device}
    r = requests.post(items_url, data=post_data)
    items_dict = dict(json.loads(r.text))
    # flash(items_dict["message"])
    print(items_dict["message"])


def end_items_session(key):
    items_url = "{}/session".format(ITEMS_URL)
    post_data = {"action": "stop", "session_key": key}

    r = requests.post(items_url, data=post_data)
    items_dict = dict(json.loads(r.text))
    # flash(items_dict["message"])
    print(items_dict["message"])
