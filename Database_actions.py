from mysql import connector
import json
import config.config as config

DATABASE = None


def db_connection():
    db_config_file = open(config.DATABASE_CONNECTION)
    db_config      = json.load(db_config_file)

    global DATABASE
    DATABASE = connector.connect(host     =  db_config['host'],
                                 user     =  db_config['user'],
                                 password =  db_config['pswd'],
                                 database =  db_config['database'])
    print("Database_actions.py | db_connection(): connection to database is established")


def db_connection_close():
    global DATABASE
    if DATABASE is None: return
    db_cursor = DATABASE.cursor()
    db_cursor.close()

    print("Database_actions.py | db_connection_close(): connection to database is closed")


def db_commit():
    global DATABASE
    if DATABASE is None: return

    DATABASE.commit()
    print("Database_actions.py | db_commit(): commit to database")


def execute_SQL(command):
    global DATABASE
    if DATABASE is None: return

    print("Database_actions.py | execute_SQL(): query to database: ")
    print(command)
    db_cursor = DATABASE.cursor()
    db_cursor.execute(command)

    res = db_cursor.fetchall()
    print("Database_actions.py | execute_SQL(): the query is executed")
    return res

