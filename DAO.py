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

#ge info form database 0 = success 1 = DB connection  3 = empty db
def get_db_info(username, password, tables):

    try:

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

        print(f"Error: {e}")

        connection.close()
        
        cursor.close()

        return 1 , None
    

def get_revenue_info(username, password):
    
    try:

        connection = _db_connection(username, password)
        cursor = connection.cursor(dictionary=True)

        attendance_revenue_result=[]

        attendance_revenue_query = """
            SELECT * 
            FROM RevenueEvents 
            WHERE RevenueTypeID = (SELECT ID FROM RevenueType WHERE Type = 'Admission');
        """
        cursor.execute(attendance_revenue_query)
        attendance_revenue_result.append(cursor.fetchall())
        
        # Retrieve information from AnimalShow table
        attendance_revenue_query = """
            SELECT * 
            FROM RevenueEvents 
            WHERE RevenueTypeID = (SELECT ID FROM RevenueType WHERE Type = 'Concession');
        """
        cursor.execute(attendance_revenue_query)
        attendance_revenue_result.append(cursor.fetchall())

        attendance_revenue_query = """
            SELECT * 
            FROM RevenueEvents 
            WHERE RevenueTypeID = (SELECT ID FROM RevenueType WHERE Type = 'Entertainment');
        """
        cursor.execute(attendance_revenue_query)
        attendance_revenue_result.append(cursor.fetchall())

        if attendance_revenue_result != [[],[],[]]:

            connection.close()

            return 0, attendance_revenue_result

        connection.close()
        return 3, attendance_revenue_result

    except Exception as e:
        print(f"Error: {e}")
        connection.close()
        cursor.close()
        return 1, None



# get info of person/ building/ employee/ attration 1 = connection error 4 = duplicate/exist 6 = doesn't exist 7 = constraint error
def get_info(username, password, query, params):

    try:
        
        connection = _db_connection(username, password)
        
        if not connection.is_connected():

            return 1, None

        cursor = connection.cursor(dictionary=True)

        cursor.execute(query, params)

        result = cursor.fetchall()

        connection.close()

        if cursor.rowcount > 0:
            
            return 3, result  
        
        
        connection.close()

        cursor.close()

        return 6, None


    except Error as e:
        connection.close()
        cursor.close()

        print("Error while connecting to MySQL", e)
    
        return 7, None

# add to database 0 = success 1 = connection error 4 = duplicate 7 = constraint 
def add_update(username, password, sql_list, data_list,operation):

    try:

        connection = _db_connection(username, password)

        if not connection.is_connected():

            return 1

        cursor = connection.cursor()

        id = ""
        

        for number, (sql, data) in enumerate(zip(sql_list, data_list), start=0):

            print(sql)

            print(data)

            if (operation == "insert building/enclosure" and number != 0):
                
                data += (id, )

                cursor.execute(sql,tuple(data))
                

            elif (operation == "employee insert/rate/supervisor" and number != 0):
                
                data += (id, )
                
                print(sql)

                print(data)

                cursor.execute(sql,tuple(data))


            elif (operation == "insert revenuetype/attraction" and number != 0):

                data += (id, )

                cursor.execute(sql,tuple(data))
                
            else:
                cursor.execute(sql,tuple(data))

                cursor.fetchall()
                
                id = cursor.lastrowid

                if cursor.rowcount == 0:

                    return 3

        connection.commit()

        return 0 


    except Exception as e:

        print(f"Error: {e}")

        connection.close()
        
        cursor.close()
        return 4

