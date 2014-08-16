from scripts.create_database import db

db.create_database('melafista')
db.create_table_users(name_database='melafista')
db.create_table_users_message(name_database='melafista')
db.create_table_sessions(name_database='melafista')
