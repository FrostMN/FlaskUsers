import os

_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

# Database Config
MYSQL_HOST = "localhost"
MYSQL_PORT = "3306"
MYSQL_USER = "inv_users_user"
MYSQL_PASSWORD = "(8tEH3gfGfTJEotxufYouEpgIr2SlM5sKrFZbPtEtxRKFUGwkfE3tM5clwf1m5Ms)"
MYSQL_DB = "inv_users"
MYSQL_TEMPLATE = "mysql://{}:{}@{}:{}/{}"

MYSQL_CONN = MYSQL_TEMPLATE.format(MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT, MYSQL_DB)

# Items API URL
ITEMS_PORT = "8090"
ITEMS_HOST = "localhost"
ITEMS_TEMPLATE = "http://{}:{}"
ITEMS_URL = ITEMS_TEMPLATE.format(ITEMS_HOST, ITEMS_PORT)

del os

if __name__ == '__main__':
    print(MYSQL_CONN)