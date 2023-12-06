def employee_insert_schema(first_name, last_name, minit, job_type, start_date, street, city, state, zip_code):

    # Insert data into the Building table
    employee_data = [first_name, last_name, minit, job_type, start_date, street, city, state, zip_code]

    # sql for inserting
    employee_sql = """
                INSERT IGNORE INTO Employee (FirstName, LastName, Minit, JobType, StartDate, Street, City, State, Zip) 
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
                    """

    return employee_sql, employee_data


def employee_info_by_name(first_name,last_name):

    employee_data = [first_name,last_name]

    employee_sql = "SELECT * FROM Employee WHERE FirstName = %s AND LastName = %s;"

    
    return employee_sql, employee_data


def hourly_insert_schema(employee_id, rate):

    # Insert data into the Building table
    hourly_data = [employee_id,rate]

    # sql for inserting
    hourly_rate_sql = """INSERT IGNORE INTO hourlyrate (ID,RateEarned) 
                            VALUES (%s,%s);"""

    return hourly_rate_sql, hourly_data

def insert_supervisor(id_person):

    # obtains user ID
    supervisor_data = [id_person,]

    # adds user to supervisor list
    supervisor_sql = """INSERT IGNORE INTO supervises (SupervisorID) 
                                        VALUES (%s);"""
    
    return supervisor_sql, supervisor_data
