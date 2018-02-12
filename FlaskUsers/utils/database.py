import datetime
import time

import FlaskUsers.utils.secrets as secrets
import config
from FlaskUsers.models.schema import schema
from FlaskUsers.models.user import User

import MySQLdb

sql_host = config.MYSQL_HOST
sql_port = int(config.MYSQL_PORT)
sql_pwd = config.MYSQL_PASSWORD
sql_usr = config.MYSQL_USER
sql_db = config.MYSQL_DB

user_db = MySQLdb.connect(host=sql_host, port=sql_port, user=sql_usr, passwd=sql_pwd, db=sql_db)


def execute_query(qry, params=None):
    if params:
        with user_db.cursor() as cur:
            try:
                cur.execute(qry, params)
                user_db.commit()
            except MySQLdb.MySQLError as e:
                user_db.rollback()
                print("MySql Transaction error:\n" + str(e))
                return e
    else:
        with user_db.cursor() as cur:
            try:
                cur.execute(qry)
                user_db.commit()
            except Exception as e:
                user_db.rollback()
                print("MySql Transaction error:\n" + str(e))
                return e


def execute_remote_query(qry, params=None):
    if params:
        with user_db.cursor() as cur:
            try:
                cur.execute(qry, params)
                user_db.commit()
            except MySQLdb.MySQLError as e:
                user_db.rollback()
                print("MySql Transaction error:\n" + str(e))
                return e
    else:
        with user_db.cursor() as cur:
            try:
                cur.execute(qry)
                user_db.commit()
            except Exception as e:
                user_db.rollback()
                print("MySql Transaction error:\n" + str(e))
                return e


def execute_queries(qry, params=None):
    if params:
        with user_db.cursor() as cur:
            try:
                cur.executemany(qry, params)
                user_db.commit()
            except MySQLdb.MySQLError as e:
                user_db.rollback()
                print("MySql Transaction error:\n" + str(e))
                return e
    else:
        with user_db.cursor() as cur:
            try:
                cur.executemany(qry)
                user_db.commit()
            except Exception as e:
                user_db.rollback()
                print("MySql Transaction error:\n" + str(e))
                return e


def get_rs(qry, params=None):
    if params:
        with user_db.cursor() as cur:
            try:
                cur.execute(qry, params)
                rs = cur.fetchall()
                if len(rs) == 1:
                    rs = rs[0]
                user_db.commit()
                return rs
            except MySQLdb.MySQLError as e:
                user_db.rollback()
                print("MySql Transaction error:\n" + str(e))
                return e
    else:
        with user_db.cursor() as cur:
            try:
                cur.execute(qry)
                rs = cur.fetchall()
                user_db.commit()
                return rs
            except Exception as e:
                user_db.rollback()
                print("MySql Transaction error:\n" + str(e))
                return e


def user_exists(email):
    exists_qry = "SELECT COUNT(*) FROM users WHERE email = %s"
    rs = get_rs(exists_qry, (email, ))
    print("in sb.user_exists(email)")
    print(rs)
    if bool(rs[0]):
        print("User Exists - True")
        return True
    else:
        print("User Exists - False")
        return False


def get_user_hash(email):
    if user_exists(email):
        get_salt_query = "SELECT hash FROM users WHERE email = %s"
        email = (email, )
        print(email)
        return get_rs(get_salt_query, email)[0]
    else:
        return "no user name"  # TODO: this needs to be made propper


def get_user(email):
    print("in db.getuser()")
    user_query = "SELECT * FROM users WHERE email = %s"
    user_data = get_rs(user_query, (email, ))

    print("user_data: ")
    print(user_data)

    # these need to pull from the db query
    usr_email = user_data[1]
    usr_confirmed = user_data[2]
    usr_type = user_data[3]
    usr_fname = user_data[4]
    usr_lname = user_data[5]
    usr_lang = user_data[10]
    user_key = secrets.generate_nonce()
    user_id = user_data[0]

    return User(email=usr_email, email_confirmed = usr_confirmed, account_type=usr_type, first_name=usr_fname,
                last_name=usr_lname, lang=usr_lang, pw_hash=None, nonce=None, creation_time=None,
                session_key=user_key, user_id=user_id)


def _init_db():
    for qry in schema:
        execute_query(qry)


if __name__ == '__main__':
    _init_db()
