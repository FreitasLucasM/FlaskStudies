import mysql.connector

mydb = mysql.connector.connect(host="localhost", user="root", passwd="try#Honesty2001")

my_cursor = mydb.cursor()

# my_cursor.execute("CREATE DATABASE users")

# later this step, run python3 shell and
# from main import app, db
# with app.app_context():
#   db.create_all()

my_cursor.execute("SHOW DATABASES")
for db in my_cursor:
    print(db)