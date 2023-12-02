# imports sql connetor
import mysql.connector

# error from mysql
from mysql.connector import Error


# Conenction to database
def _db_connection(username, password):

    # tries connection and returns connection
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user=username,
            password=password,
            database="zoo",
            port=3306
        )
        if connection.is_connected():
            print("Connected to MySQL")
            return connection
        
    # error connecting
    except Error as e:
        print("Error while connecting to MySQL", e)
        return None

# Close the database connection
def close_connection(connection):

    if connection.is_connected():

        connection.close()

        print("MySQL connection closed")

# checks if user is in db and closes 0 sucess 1 doesn't exist
def checking_user(username,password):

    try:

        db_connection = _db_connection(username,password)
            
        db_connection.close()


        return 0
        
    except:
        return 1
    
# adding users uses a specific where you can just push a sql and data to add rather than indivdual 
def add(username, password, sql, data):

    try:

        # Assuming _db_connection is a function that returns a valid database connection
        db_connection = _db_connection(username, password)

        cursor = db_connection.cursor()

        cursor.execute(sql, tuple(data))

        # Commit the changes
        db_connection.commit()

        affected_rows = cursor.rowcount

        cursor.close()
        db_connection.close()

        if affected_rows > 0:
            return 0  # Success
        else:
            return 2  # No rows affected (possible duplicate)

    except Exception as e:
        print(f"Error: {e}")
        return 1  # Other errors

    
# Retrives data from certain tables passed through
def get_db_info(username, password, tables):

    try:
        # Assuming _db_connection is a function that returns a valid database connection
        db_connection = _db_connection(username, password)

        cursor = db_connection.cursor(dictionary=True)

        list_of_all = {}

        for table in tables:

            query = "SELECT * FROM " + table

            cursor.execute(query)
            records = cursor.fetchall()
            list_of_all[table] = records

        if list_of_all[tables[0]] != []:
            db_connection.close()
            return list_of_all

    except Error as e:
        print("Error while connecting to MySQL", e)
        return 1
    

# gets employee info only to obatain ID and update hourly rate and supervisor
def get_employee_info(username, password, first, last):
    try:
        # Assuming _db_connection is a function that returns a valid database connection
        with _db_connection(username, password) as db_connection:
            cursor = db_connection.cursor()

            query = "SELECT * FROM Employee WHERE FirstName = %s AND LastName = %s;"
            params = (first, last)

            cursor.execute(query, params)

            # Fetch the results if needed
            result = cursor.fetchall()

            if result == []:
                return 2, result

        return 0, result  # Success

    except Error as e:
        print("Error while connecting to MySQL", e)
        return 1, None  # Failure with an error message


# updates info for anything
def update_info(username,password,update_sql,update_data):

    try:

        db_connection = _db_connection(username, password)

        cursor = db_connection.cursor()

        # Execute the SQL query
        cursor.execute(update_sql, tuple(update_data))

        # Commit the changes and close the cursor and connection
        db_connection.commit()
        cursor.close()
        db_connection.close()

        return 0

    except Exception as e:
        print(f"Error: {e}")
        cursor.close()
        db_connection.close()
        return 1
