from db_connection import db

connection = db.get_connection()

if connection:
    print("Connected Successfully!")
    connection.close()
else:
    print("Connection Failed!")