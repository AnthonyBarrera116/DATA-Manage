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
    
    return 1

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

def add(username, password, sql, data):

    try:

        # Assuming _db_connection is a function that returns a valid database connection
        db_connection = _db_connection(username, password)

        cursor = db_connection.cursor()

        cursor.execute(sql, tuple(data))

        # Commit the changes
        db_connection.commit()

        affected_rows = cursor.rowcount

        if affected_rows > 0:


            db_connection.close()
            cursor.close()
            return 0  # Success
        else:

            db_connection.close()
            cursor.close()
            return 4  # No rows affected (possible duplicate)

    except Exception as e:
        # Log the error instead of printing
        print(f"Error: {e}")
        # Return a specific error code or raise an exception based on your needs
        db_connection.close()
        cursor.close()
        return 1  # Other errors

    
# Retrives data from certain tables passed through
from mysql.connector import Error

def get_db_info(username, password, tables):
    try:
        # Assuming _db_connection is a function that returns a valid database connection
        db_connection = _db_connection(username, password)

        if not db_connection:
            print("Error: Database connection is not established.")
            return 1

        cursor = db_connection.cursor(dictionary=True)

        list_of_all = {}

        for table in tables:
            query = f"SELECT * FROM {table}"
            cursor.execute(query)
            records = cursor.fetchall()
            list_of_all[table] = records

        if list_of_all[tables[0]] != []:
            db_connection.close()
            return list_of_all

    except Error as e:
        print("Error while connecting to MySQL:", e)

    # Return an error code indicating a problem with the database
    db_connection.close()
    return 1


# gets employee info only to obatain ID and update hourly rate and supervisor
def get_building_id_info(username, password, building_name):

    try:
        # Assuming _db_connection is a function that returns a valid database connection
        db_connection = _db_connection(username, password)

        if not db_connection:
            print("Error: Database connection is not established.")
            return 1
        
        cursor = db_connection.cursor()

        query = "SELECT * FROM Building WHERE Name = %s;"
        params = (building_name,)

        cursor.execute(query, params)

        # Fetch the results if needed
        result = cursor.fetchall()

        db_connection.close()
        cursor.close()

        if result == []:

            return 2, result

        return 4, result  # Success

    except Error as e:

        print("Error while connecting to MySQL", e)
    
    return 1, None  # Failure with an error message

# gets employee info only to obatain ID and update hourly rate and supervisor
def get_employee_info(username, password, first, last):
    try:
        # Assuming _db_connection is a function that returns a valid database connection
        db_connection = _db_connection(username, password)

        if not db_connection:
            print("Error: Database connection is not established.")
            return 1
        
        cursor = db_connection.cursor(dictionary=True)

        query = "SELECT * FROM Employee WHERE FirstName = %s AND LastName = %s;"
        params = (first, last)

        cursor.execute(query, params)

        # Fetch the results if needed
        result = cursor.fetchall()

        db_connection.close()
        cursor.close()

        if result == []:

            return 2, result

        return 4, result  # Success

    except Error as e:
        db_connection.close()
        cursor.close()

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
