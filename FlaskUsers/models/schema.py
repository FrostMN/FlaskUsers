# import sqlparse
import FlaskUsers.utils.secrets as secrets

admin_user_email = "admin@devaccount.com"
admin_user_password = "admin"
admin_user_email_confirmed = "1"
admin_user_account_type = "1"
admin_user_first_name = "Admin"
admin_user_last_name = "Account"
admin_user_salt = str(secrets.generate_nonce())
admin_user_hash = str(secrets.hash_password(password=admin_user_password, salt=admin_user_salt))
admin_user_nonce_timestamp = "NULL"

admin_bcrypt_hash = str(secrets.bc_hashpw(admin_user_password, as_string=True))

user_user_email = "user@devaccount.com"
user_user_password = "user"
user_user_email_confirmed = "1"
user_user_account_type = "0"
user_user_first_name = "User"
user_user_last_name = "Account"
user_user_salt = str(secrets.generate_nonce())
user_user_hash = str(secrets.hash_password(password=user_user_password, salt=user_user_salt))
user_user_nonce_timestamp = "NULL"

user_bcrypt_hash = str(secrets.bc_hashpw(user_user_password, as_string=True))

drop_users = "DROP TABLE IF EXISTS users"

drop_keys = "DROP TABLE IF EXISTS session_keys"

drop_events = "DROP TABLE IF EXISTS session_events"

create_users = "CREATE TABLE users( " \
    "user_id INT NOT NULL AUTO_INCREMENT, " \
    "email VARCHAR(120) UNIQUE NOT NULL, " \
    "email_confirmed SMALLINT NOT NULL DEFAULT 0, " \
    "account_type VARCHAR(120) NOT NULL DEFAULT 'user', " \
    "first_name VARCHAR(120) DEFAULT '', " \
    "last_name VARCHAR(120) DEFAULT '', " \
    "hash VARCHAR(60) NOT NULL, " \
    "nonce VARCHAR(64) DEFAULT '', " \
    "nonce_timestamp DATETIME , " \
    "creation_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, " \
    "language VARCHAR(10) NOT NULL DEFAULT 'eng', " \
    "PRIMARY KEY (user_id)" \
    ") "

create_keys = "CREATE TABLE session_keys( " \
     "user_id INT NOT NULL, " \
     "session_key VARCHAR(64), " \
     "active SMALLINT DEFAULT 1, " \
     "admin SMALLINT DEFAULT 0, " \
     "device VARCHAR(128) " \
     ") "

create_events = "CREATE TABLE session_events( " \
     "event_id INT NOT NULL AUTO_INCREMENT, " \
     "session_key VARCHAR(64), " \
     "event VARCHAR(512), " \
     "event_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, " \
     "PRIMARY KEY (event_id)" \
     ")"


insert_admin = "INSERT INTO users ( email, email_confirmed, account_type, " \
    "first_name, last_name, hash, nonce_timestamp ) "\
    "VALUES ( " \
        "'" + admin_user_email + "', " \
        "" + admin_user_email_confirmed + ", " \
        "'" + admin_user_account_type + "', " \
        "'" + admin_user_first_name + "', " \
        "'" + admin_user_last_name + "', " \
        "'" + admin_bcrypt_hash + "', " \
        "" + admin_user_nonce_timestamp + " " \
    ")"


insert_user = "INSERT INTO users ( email, email_confirmed, account_type, " \
    "first_name, last_name, hash, nonce_timestamp ) "\
    "VALUES ( " \
        "'" + user_user_email + "', " \
        "" + user_user_email_confirmed + ", " \
        "'" + user_user_account_type + "', " \
        "'" + user_user_first_name + "', " \
        "'" + user_user_last_name + "', " \
        "'" + user_bcrypt_hash + "', " \
        "" + user_user_nonce_timestamp + " " \
    ")"

schema = (drop_users, drop_keys, drop_events, create_users, create_keys, create_events, insert_admin, insert_user)

if __name__ == '__main__':
    for qry in schema:
        print(qry)
