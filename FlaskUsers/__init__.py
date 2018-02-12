from flask import Flask, render_template, request
import FlaskUsers.utils.database as db
import FlaskUsers.utils.api as api
from flask_api import status

import json


app = Flask(__name__)
app.config.from_object("config")


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.get_data():
            request_data = request.get_data().decode("utf-8")
            # print("request_data: ")
            # print(request_data)

            req_dict = unpack_request(request_data)
            # print("req_dict: ")
            # print(req_dict)

            if 'username' in req_dict.keys() and 'password' in req_dict.keys() and 'device' in req_dict.keys():
                print("fields present")
                login_json = api.get_user(req_dict["username"], req_dict["password"], req_dict["device"])
                if "session_key" in login_json[0]:
                    print("in if session key login_json[0]")
                    key = dict(json.loads(login_json[0]))["session_key"]
                    user_id = dict(json.loads(login_json[0]))["UserID"]
                    admin = dict(json.loads(login_json[0]))["type"]
                    print("before api.start_session")
                    print(admin)
                    # print(req_dict)
                    api.start_session(user_id, key, admin, req_dict["device"])
                    print("after api.start_session")
                return login_json
            else:
                return "{ \"error\": true, \"message\": \"Missing Parameter - 400\" }", status.HTTP_400_BAD_REQUEST
        else:
            return "{ \"error\": true, \"message\": \"Missing Parameter - 400\" }", status.HTTP_400_BAD_REQUEST
    else:
        return "{ \"error\": true, \"message\": \"Method Not Allowed - 405\" }", status.HTTP_405_METHOD_NOT_ALLOWED


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    print("in logout")
    if request.method == "POST":
        if request.get_data():
            request_data = request.get_data().decode("utf-8")
            print(request_data)
            try:
                req_json = json.loads(request_data)
                req_dict = dict(req_json)
                print(req_dict["username"])
                print(req_dict["session_key"])
                print(req_dict["device"])
            except ValueError:
                req_dict = request.form
                print(req_dict["username"])
                print(req_dict["session_key"])
                print(req_dict["device"])

            api.end_session(req_dict["session_key"], req_dict["device"])
            return "{ \"error\": false, \"message\": \"You have successfully logged out.\" }", status.HTTP_200_OK
    else:
        return "{ \"error\": true, \"message\": \"Method Not Allowed - 405\" }", status.HTTP_405_METHOD_NOT_ALLOWED


@app.route('/log/<key>/event', methods=['POST', 'GET'])
def log_event(key):
    print("in log_event")
    print(request.method)
    if request.method == "POST":
        print("in log_event if post")

        request_data = request.get_data().decode("utf-8")
        req_dict = unpack_request(request_data)

        print("req_dict: ")
        print(req_dict)

        if api.session_active(key):
            api.log_session_event(req_dict["session_key"], req_dict["event"])
            return "{ \"error\": false, \"message\": \"event logged\" }", status.HTTP_200_OK
        else:
            return "{ \"error\": true, \"message\": \"Session key is inactive\" }", status.HTTP_401_UNAUTHORIZED
    else:
        return "{ \"error\": true, \"message\": \"Method Not Allowed - 405\" }", status.HTTP_405_METHOD_NOT_ALLOWED


def unpack_request(data):
    """ Unpacks the data returned by the api request """
    try:
        req_json = json.loads(data)
        req_dict = dict(req_json)
    except ValueError:
        req_dict = request.form
    return req_dict


if __name__ == '__main__':
    app.run(port=8085)
