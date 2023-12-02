# import flask session allows to save user session 
from flask import session

# Import DAO for db connection
import DAO as dao

#_______________________________Logging in ___________________________________________________________

# Checks if user account is in DB and saves session
def logged_user(username,password):

    # Checks is user is in DB
    result = dao.checking_user(username,password)

    # Yes saves session
    if result == 0:

        session['username'] = username
        session['password'] = password

    # returns result 0 = success 1 = incorret account
    return result


#_______________________________User Checking___________________________________________________________

# if user is logged in and saved in session
def if_user_logged_in ():

    # Checks is user is in DB
    result = dao.checking_user( session['username'],session['password'])

    # returns result 0 = success 1 = incorret account
    return result

# get info fof tables requests for retriveing data fro viewing
def get_info(tables):

    # if user is logged in from session than return db
    if logged_user(session['username'],session['password']) == 0:

        result = dao.get_db_info(session['username'], session['password'],tables)

    # return db or returns 1 for not logged in
    return result


#_______________________________Animal Insert/Update___________________________________________________________

# inserts new animal 
def insert_animal(species_id, status, birth_year,enclosure_id):

    # checks if user is logged in
    if if_user_logged_in(session['username'],session['password']) == 0:

        # Insert data into the Animal table
        animal_data = [status, birth_year, species_id, enclosure_id]

        # SQL for inserting animal
        animal_sql = "INSERT INTO Animal (Status, BirthYear, SpeciesID, EnclosureID) VALUES (%s, %s, %s, %s)"

        # calls DAO add to add animal
        result = dao.add(session['username'],session['password'],animal_sql,animal_data)

        # returns 0 success 2 duplicate 1 Error with DB
        return result
        
# updates animal with fields
def update_animal(animal_id=None, species_id=None, new_status=None, new_birth_year=None, enclosure_id=None):
    
    # checks if user is logged
    if if_user_logged_in(session['username'],session['password']) == 0:

        # sql update animal
        update_sql = "UPDATE Animal SET"

        # animal data saved for sql
        update_animal = []

        # if staments are used to put in data the user has inputed empty fields will be ignored
        if species_id is not "":
            update_sql += " SpeciesID = %s,"
            update_animal.append(species_id)

        if new_status is not "":
            update_sql += " Status = %s,"
            update_animal.append(new_status)

        if new_birth_year is not "":
            update_sql += " BirthYear = %s,"
            update_animal.append(new_birth_year)

        if enclosure_id is not "":
            update_sql += " EnclosureID = %s,"
            update_animal.append(enclosure_id)

        # Remove the trailing comma for sql
        update_sql = update_sql.rstrip(',')

        # if the set is empty than return 2 and error nothing updated empty fields
        if update_animal == []:

            return 2
        
        # where to say data according to ID
        update_sql += " WHERE ID = %s"

        # append data to saved data set
        update_animal.append(animal_id)
        
        # Update animal
        result = dao.update_info(session['username'], session['password'], update_sql, update_animal)

    # returns 0 success 2 doesn't exist 1 Error with DB
    return result

    
#_______________________________Building Insert/Update___________________________________________________________    

# inserts new building 
def insert_building(building_name, building_type):

    # checks if user is logged in
    if if_user_logged_in(session['username'], session['password']) == 0:

        # Insert data into the Building table
        building_data = [building_name, building_type]

        # SQL for inserting Building
        building_sql = """INSERT IGNORE INTO Building (Name, Type)VALUES (%s, %s);"""

        # calls DAO add to add building
        result = dao.add(session['username'], session['password'], building_sql, building_data)

        # returns 0 success 2 duplicate 1 Error with DB
        return result

# updates Building with fields
def update_building(building_id=None, building_name = None, type = None):
    
    # checks if user is logged
    if if_user_logged_in(session['username'],session['password']) == 0:

        # sql update Building
        update_sql = "UPDATE Building SET"

        # Building data saved for sql
        update_building = []

        # if staments are used to put in data the user has inputed empty fields will be ignored
        if building_name is not "":
            update_sql += " name = %s,"
            update_building.append(building_name)

        if type is not "":
            update_sql += " type = %s,"
            update_building.append(type)

        # Remove the trailing comma for sql
        update_sql = update_sql.rstrip(',')

        # if the set is empty than return 2 and error nothing updated empty fields
        if update_building == []:

            return 2
        
        # where to say data according to ID
        update_sql += " WHERE ID = %s"

        # append data to saved data set
        update_building.append(building_id)
        
        # Update Building
        result = dao.update_info(session['username'], session['password'], update_sql, update_building)

    # returns 0 success 2 doesn't exist 1 Error with DB
    return result


#_______________________________Employee Insert/Update___________________________________________________________    

# inserts new employee 
def insert_employee(first_name, last_name, minit, job_type, start_date, street, city, state, zip_code, supervisor,rate):

    # checks if user is logged in
    if if_user_logged_in(session['username'], session['password']) == 0:

        # checks if person already exists in db
        person = dao.get_employee_info(session['username'], session['password'], first_name, last_name)

        # if 2 means user doesn't exist so add
        if person[0] == 2:

            # set of employee data
            employee_data = [first_name, last_name, minit, job_type, start_date, street, city, state, zip_code]

            # sql for inserting
            employee_sql = """
                        INSERT IGNORE INTO Employee (FirstName, LastName, Minit, JobType, StartDate, Street, City, State, Zip) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
                    """

            # Inserts employee
            result = dao.add(session['username'], session['password'], employee_sql, employee_data)

            # Here to obtain new employee ID
            person = dao.get_employee_info(session['username'], session['password'], first_name, last_name)

            # person is a list code if 0 = success,1=error with db ,2 = doesn't exist. but this obtains uesr ID
            hourly_rate_data = [person[1][0][0], float(rate)]

            # sql for inserting
            hourly_rate_sql = """INSERT IGNORE INTO hourlyrate (ID,RateEarned) 
                            VALUES (%s,%s);"""

            # Inserts employee rate
            result = dao.add(session['username'], session['password'], hourly_rate_sql,hourly_rate_data)

            # if they are a new employee and supervisor
            if supervisor == "yes":

                # obtains user ID
                supervisor_data = [person[1][0][0]]

                # adds user to supervisor list
                supervisor_sql = """INSERT IGNORE INTO supervises (SupervisorID) 
                                VALUES (%s);"""

                # Assuming dao.add expects the SQL query first and then the data
                result = dao.add(session['username'], session['password'], supervisor_sql, supervisor_data)


            # returns most likely 0 for success 
            return result
        
        else:
            
            # if user exist already
            return 1


# Update employee
def update_employee(employee_id,job_type=None, street=None, city=None, state=None, zip_code=None, supervisor=None,rate=None):

    # for return if everything is blank
    result = 2
    
    # checks if user is logged in
    if if_user_logged_in(session['username'],session['password']) == 0:

         # SQL for updating employee
        update_sql = "UPDATE Employee SET"

        # Building data saved for sql
        update_employee = []

        # if staments are used to put in data the user has inputed empty fields will be ignored
        if job_type is not "":
            update_sql += " JobType = %s,"
            update_employee.append(job_type)

        if street is not "":
            update_sql += " Street = %s,"
            update_employee.append(street)

        if city is not "":
            update_sql += " City = %s,"
            update_employee.append(city)

        if state is not "":
            update_sql += " State = %s,"
            update_employee.append(state)

        if zip_code is not "":
            update_sql += " Zip = %s,"
            update_employee.append(zip_code)

        # Remove the trailing comma for sql
        update_sql = update_sql.rstrip(',')

        # if the set is not empty than contiue
        if update_employee != []:

            # where to say data according to ID
            update_sql += " WHERE ID = %s"

            # append data to saved data set
            update_employee.append(employee_id)

            # Update employee
            result = dao.update_info(session['username'], session['password'], update_sql, update_employee)
         
        # if they are a now a supervisor
        if supervisor == "yes":

            # obtains user ID
            supervisor_data = [employee_id]
            
            # adds user to supervisor list
            supervisor_sql = """INSERT IGNORE INTO supervises (SupervisorID) 
                                VALUES (%s);"""

            # Assuming dao.add expects the SQL query first and then the data
            result = dao.add(session['username'], session['password'], supervisor_sql, supervisor_data)

        # if they a super visor and no longer
        elif supervisor == "no":
            
            # obtains user ID
            supervisor_data = [employee_id]

            # deletes user to supervisor list
            supervisor_sql = """DELETE FROM supervises WHERE SupervisorID = %s;"""

            # Assuming dao.add expects the SQL query first and then the data
            result = dao.add(session['username'], session['password'], supervisor_sql, supervisor_data)

        # if new hourly rate is place than update
        if rate is not "":

            # obtains user ID
            rate_data = [rate, employee_id]

            # adds user to hourlyrate list
            update_sql = "UPDATE hourlyrate SET RateEarned = %s WHERE ID = %s"

             # Assuming dao.add expects the SQL query first and then the data
            result = dao.update_info(session['username'], session['password'], update_sql, rate_data)

    # returns 2 if user is not logged in our issue with input 
    return result
    
