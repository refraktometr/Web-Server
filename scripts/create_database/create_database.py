from scripts.create_database import db

database = 'melafista'
db.create_database(database)
db.create_table_users(name_database=database)
db.create_table_users_message(name_database=database)
db.create_table_sessions(name_database=database)
