from mysql.connector import connect
db_config={
    'host':'localhost',
    'user':'root',
    'password':'viki#454@mysql',
    'database':'my_db'
}
def initialize_db():
    return connect(**db_config)