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

# checks if user is in db and closes 0 sucess 1 doesn't exist
def checking_user(username,password):

    connection = _db_connection(username,password)

    if connection == 1:

        return 1

    else:
        connection.close()

        return 0

def get_db_info(username, password, tables):

    try:

        # Assuming _db_connection is a function that returns a valid database connection
        connection = _db_connection(username, password)

        cursor = connection.cursor(dictionary=True)

        db_table_info = {}

        for table in tables:

            query = f"SELECT * FROM {table}"

            cursor.execute(query)

            records = cursor.fetchall()

            db_table_info[table] = records

        if db_table_info[tables[0]] != []:

            connection.close()

            return 0, db_table_info
        
        connection.close()      
        
        return 3, db_table_info

    except Exception as e:

        # Log the error instead of printing

        print(f"Error: {e}")

        connection.close()
        
        cursor.close()

        return 1 , None # Other errors


# gets employee info only to obatain ID and update hourly rate and supervisor
def get_info(username, password, query, params):

    try:
        # Assuming _db_connection is a function that returns a valid database connection
        connection = _db_connection(username, password)
        
        if not connection.is_connected():

            return 1, None

        cursor = connection.cursor(dictionary=True)

        cursor.execute(query, params)

        # Fetch the results if needed
        result = cursor.fetchall()

        connection.close()

        if cursor.rowcount > 0:
            
            return 4, result  
        
        
        connection.close()

        cursor.close()

        return 6, None


    except Error as e:
        connection.close()
        cursor.close()

        print("Error while connecting to MySQL", e)
    
        return 7, None  # Failure with an error message

def add(username, password, sql, data):

    try:

        # Assuming _db_connection is a function that returns a valid database connection
        connection = _db_connection(username, password)

        if not connection.is_connected():

            return 1

        cursor = connection.cursor()

        cursor.execute(sql, tuple(data))

        # Commit the changes
        connection.commit()

        affected_rows = cursor.rowcount

        if affected_rows > 0:

            connection.close()

            cursor.close()

            return 0  # Success
        
        

        connection.close()

        cursor.close()

        return 4  # No rows affected (possible duplicate)

    except Exception as e:

        # Log the error instead of printing

        print(f"Error: {e}")

        connection.close()
        
        cursor.close()
        return 7  # Other errors

    

# updates info for anything
def update_info(username,password,update_sql,update_data):

    try:

        connection = _db_connection(username, password)

        if not connection.is_connected():

            return 1
        
        cursor = connection.cursor()

        # Execute the SQL query
        cursor.execute(update_sql, tuple(update_data))

        # Commit the changes and close the cursor and connection
        connection.commit()
        
        affected_rows = cursor.rowcount

        if affected_rows > 0:

            connection.close()

            cursor.close()

            return 0  # Success
        
        else:

            connection.close()

            cursor.close()

            return 6  # Doesn't exist


    except Exception as e:

        print(f"Error: {e}")
        cursor.close()
        connection.close()
    
        return 7
