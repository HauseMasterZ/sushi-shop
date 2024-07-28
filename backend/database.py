import mysql.connector

def get_database_connection():
    # Create a connection to the MySQL database
    connection = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Pqlamz@123",
        database="sushi"
    )
    return connection
