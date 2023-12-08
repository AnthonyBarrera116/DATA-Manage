# sql and data for inserting employee
def employee_insert_schema(first_name, last_name, minit, job_type, start_date, street, city, state, zip_code):

    employee_data = [first_name, last_name, minit, job_type, start_date, street, city, state, zip_code]

    employee_sql = """
                INSERT IGNORE INTO Employee (FirstName, LastName, Minit, JobType, StartDate, Street, City, State, Zip) 
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
                    """

    return employee_sql, employee_data

# sql and data fro employee by name
def employee_info_by_name(first_name,last_name):

    employee_data = [first_name,last_name]

    employee_sql = "SELECT * FROM Employee WHERE FirstName = %s AND LastName = %s;"

    
    return employee_sql, employee_data

# sql and data insert for new employee
def hourly_insert_schema(rate):

    hourly_data = [rate]

    hourly_rate_sql = """INSERT IGNORE INTO hourlyrate (RateEarned, ID) 
                            VALUES (%s,%s);"""

    return hourly_rate_sql, hourly_data

# sql and data for inserting new supervisor
def insert_supervisor(employee_ID= None):

    if employee_ID != None:
         
        supervisor_data = [employee_ID]

    else:
        supervisor_data = []

    supervisor_sql = """INSERT IGNORE INTO supervises (SupervisorID) 
                                        VALUES (%s);"""
    
    return supervisor_sql, supervisor_data


def delete_supervisor(employee_id):
            
    supervisor_data = [employee_id]

    supervisor_sql = """DELETE FROM supervises WHERE SupervisorID = %s;"""

    return supervisor_sql, supervisor_data

# sql and data for updating employee
def employee_update_schema(employee_id, job_type, street, city, state, zip_code):
    

    update_sql = "UPDATE Employee SET"

    
    update_employee = []

    
    if job_type != "":
        update_sql += " JobType = %s,"
        update_employee.append(job_type)

    if street != "":
        update_sql += " Street = %s,"
        update_employee.append(street)

    if city != "":
        update_sql += " City = %s,"
        update_employee.append(city)

    if state != "":
        update_sql += " State = %s,"
        update_employee.append(state)

    if zip_code != "":
        update_sql += " Zip = %s,"
        update_employee.append(zip_code)

    update_sql = update_sql.rstrip(',')

    if update_employee == []:

        return update_sql, update_employee

    update_sql += " WHERE id = %s"

    update_employee.append(employee_id)

    return update_sql, update_employee



def update_rate(rate, employee_id):

    houlry_data = [rate, employee_id,]

    houlry_sql = "UPDATE hourlyrate SET RateEarned = %s WHERE ID = %s"

    return houlry_sql, houlry_data