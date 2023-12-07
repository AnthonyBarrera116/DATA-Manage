# import flask session allows to save user session 
from flask import session

# Import DAO for db connection
import DAO as dao

import AnimalSchema as a_schema
import BuildingSchema as b_schema
import EmployeeSchema as e_schema

#_______________________________Logging in ___________________________________________________________

# Checks if user account is in DB and saves session
def logging_in(username,password):

    # Checks is user is in DB
    logging_sucess_result = dao.checking_user(username,password)

    # Yes saves session
    if logging_sucess_result == 0:

        session['username'] = username
        session['password'] = password

        return logging_sucess_result

    # returns result 0 = success 1 = incorret account
    return logging_sucess_result


#_______________________________User Checking___________________________________________________________

# if user is logged in and saved in session
def if_user_logged_in ():

    if 'username' in session and 'password' in session:
        
        # 0 = user logged in 
        return 0

    else:

        # 2 mean they never logged in
        return 2

    

# get info fof tables requests for retriveing data fro viewing
def get_info(tables):

    if 'username' in session and 'password' in session:

        # Get tables data
        tables_data = dao.get_db_info(session['username'], session['password'],tables)

        # return db info, if the db is empty the value is 3, if it is 1 connection to db wasn't established
        return tables_data

    else:

        # 2 mean they never logged in
        return 2, None


#_______________________________Animal Insert/Update___________________________________________________________

# inserts new animal 
def insert_animal(species_id, status, birth_year,enclosure_id):

    # returns 0 = user is logged in 2 = never logged in
    logged_check = if_user_logged_in()

    # checks if user is logged in
    if logged_check == 0:

        # fetches schmema of animal insert with building ID and how big
        insert_animal_schema = a_schema.animal_insert_schema(species_id, status, birth_year,enclosure_id)

        # adds if 0 = success to add 1 = connection fail 4 = duplicate/exist 7 = constarint failure for result_animal_insert
        result_animal_insert = dao.add(session['username'],session['password'],insert_animal_schema[0],insert_animal_schema[1])

        # returns 0 = success 1 = db connectin error 4 = duplicate 7 = constraint from result_animal_insert
        return result_animal_insert

    # returns 2 = never logged in
    return logged_check

        
# updates animal with fields
def update_animal(animal_id, species_id=None, new_status=None, new_birth_year=None, enclosure_id=None):
    
    # returns 0 = user is logged in 2 = never logged in
    logged_check = if_user_logged_in()

    # checks if user is logged
    if  logged_check == 0:

        # fetches schmema of animal update 
        update_animal_schema = a_schema.animal_update_schema(animal_id, species_id, new_status, new_birth_year, enclosure_id)

        # Nothing updated fields inputed (empty fields)
        if update_animal_schema == []:

            # 5 = empty fields
            return 5
        
        # Update animal 0 = success 1 = connection failure 6 = doesn't exist 7 = constraint for update_animal_result
        update_animal_result = dao.update_info(session['username'], session['password'], update_animal_schema[0],  update_animal_schema[1])

        # returns 0 = success 1 = connection failure 6 = doesn't exist 7 = constraint from update_animal_result
        return update_animal_result

   # return 2 = not logged in 
    return logged_check
    
    
    
#_______________________________Building Insert/Update___________________________________________________________    

# inserts new building 
def insert_building(building_name, building_type, enclosure, sq_ft):

    # returns 0 = user is logged in 2 = never logged in
    logged_check = if_user_logged_in()

    # checks if user is logged in
    if logged_check == 0:

        # if sqruare feet isnt a digit then you have a probelm of a possible string inputed not an integer
        # 7 = constraint fail
        if not sq_ft.isdigit() and enclosure == "yes":

            return 7

        # fetches schmema of building insert with building ID
        insert_building_schema = b_schema.building_insert_schema(building_name, building_type)
       
        # adds if 0 = success to add 1 = connection fail 4 = duplicate/exist 7 = constarint failure for result_buildung_insert
        result_building_insert = dao.add(session['username'], session['password'], insert_building_schema[0], insert_building_schema[1])

        # if building is an enclosure
        if enclosure == "yes" and result_building_insert == 0:

            # fetches schmema of building info to obtain building ID
            check_building_exists_schema = b_schema.building_info_by_name(building_name)
            
            # gets building info for ID but if 1 = connection fail 4 = duplicate/exist 6 = doesn't exist 7 = constarint failure
            building_info = dao.get_info(session['username'], session['password'], check_building_exists_schema[0],check_building_exists_schema[1])

            # connection fail
            if building_info[0] == 4 :

                # fetches schmema of enclosure insert with building ID and how big
                insert_list_enclosure_schema = b_schema.enclosure_insert_schema(building_info[1][0]["ID"],sq_ft)

                # Inserts enclosure 0 = sucess 1 = error connection for enclosure 7 = constraint failure for result_enclosure_insert
                result_enclousre_insert = dao.add(session['username'], session['password'], insert_list_enclosure_schema[0], insert_list_enclosure_schema[1])

                # 0 = success 1 = error connection for enclosure 7 = constraint failure for result_enclosure_insert
                return result_enclousre_insert
            
            # returns 1 = connection fail 4 = duplicate/exist 6 = doesn't exist 7 = constarint failure for building_info
            return building_info[0]
    
        # 1 = connection fail 4 = duplicate/exist 6 = doesn't exist 7 = constarint failure for result_building_insert
        return result_building_insert

    # returns 2 = never logged in for logged_check
    return logged_check

# updates Building with fields
def update_building(building_id, building_name = None, type = None):

    # returns 0 = user is logged in 2 = never logged in
    logged_check = if_user_logged_in()

    # checks if user is logged in
    if logged_check == 0:

        # fetches schmema of building update with building ID
        check_building_exists_schema = b_schema.building_info_by_ID(building_id) 

        # gets info 1 = connection issuse 4 = exists 6 = doesn't exist 7 = constraint 
        check_building_exists = dao.get_info(session['username'], session['password'], check_building_exists_schema[0],  check_building_exists_schema[1])

        # if exists
        if check_building_exists[0] == 4:

            # fetches schmema of update building with building ID
            update_building_schema = b_schema.building_update_schema(building_id,building_name,type)

            # if empty fields
            if update_building_schema == []:
                
                return 5
            
            # Update Building
            update_building_result = dao.update_info(session['username'], session['password'], update_building_schema[0], update_building_schema[1])

            # returns 0 = success 1 = connection issuse 6 = doesn't exist 7 = constraint 
            return update_building_result
            
        # 1 = connection issuse 6 = doesn't exist 7 = constraint 
        return check_building_exists[0]

    # returns 0 success 2 never signed in 1 Error with DB
    return logged_check


#_______________________________Employee Insert/Update___________________________________________________________    

# inserts new employee 
def insert_employee(first_name, last_name, minit, job_type, start_date, street, city, state, zip_code, supervisor,rate):

    # returns 0 = user is logged in 2 = never logged in
    logged_check = if_user_logged_in()

    # checks if user is logged in
    if logged_check == 0:

        # if rate isnt a digit then you have a probelm of a possible string inputed not an integer
        # 7 = constraint fail
        if not rate.isdigit():

            return 7

        # set of employee data
        insert_list_employee_schema = e_schema.employee_insert_schema(first_name, last_name, minit, job_type, start_date, street, city, state, zip_code)

        # adds if 0 = success to add 1 = connection fail 4 = duplicate/exist 7 = constarint failure for result_buildung_insert
        insert_person_result = dao.add(session['username'], session['password'], insert_list_employee_schema[0], insert_list_employee_schema[1])

        # person was inserted
        if insert_person_result == 0:

            # set of employee data
            get_list_employee_schema = e_schema.employee_info_by_name(first_name, last_name)

            # Here to obtain new employee ID 1 = connection error 4 = duplicat/exist 6 = doesn't exist
            person_info = dao.get_info(session['username'], session['password'], get_list_employee_schema[0], get_list_employee_schema[1])

            # person exist 4 = dupliocat/exists
            if person_info[0] == 4:

                # Schema for hourly
                hourly_schema = e_schema.hourly_insert_schema(person_info[1][0]["ID"], rate)

                # adds if 0 = success to add 1 = connection fail 4 = duplicate/exist 7 = constarint failure for result_hourly_insert
                hourly_result = dao.add(session['username'], session['password'], hourly_schema[0],hourly_schema[1])

                # if they are a new employee and supervisor
                if supervisor == "yes" and hourly_result == 0:
                        
                    supervisor_result = e_schema.insert_supervisor(person_info[1][0]["ID"])

                    # adds if 0 = success to add 1 = connection fail 4 = duplicate/exist 7 = constarint failure for supervisore_insert
                    supervisor_result = dao.add(session['username'], session['password'], supervisor_result[0], supervisor_result[1])

                    # 0 = success to add 1 = connection fail 4 = duplicate/exist 7 = constarint failure for supervisore_insert
                    return supervisor_result

                # 0 = success to add 1 = connection fail 4 = duplicate/exist 7 = constarint failure for supervisore_insert
                return hourly_result

            # Here to obtain new employee ID 1 = connection error 4 = duplicat/exist 6 = doesn't exist
            return person_info[0]

        # returns most likely 0 for success 
        return insert_person_result
        
    # 2 = not signed in
    return logged_check



# Update employee
def update_employee(employee_id,job_type=None, street=None, city=None, state=None, zip_code=None, supervisor=None,rate=None):

    # returns 0 = user is logged in 2 = never logged in
    logged_check = if_user_logged_in()

    # checks if user is logged
    if  logged_check == 0:

        update_employee_schema = e_schema.employee_update_schema(employee_id,job_type, street, city, state, zip_code)
        

        # Nothing updated fields inputed (empty fields)
        if update_employee_schema[1] != []:

            # Update employee
            result_update_employee = dao.update_info(session['username'], session['password'], update_employee_schema[0], update_employee_schema[1])

        # if they are a now a supervisor
        if supervisor == "yes":

            update_supervisor_schema = e_schema.insert_supervisor(employee_id)

            # Assuming dao.add expects the SQL query first and then the data
            update_sp_result = dao.add(session['username'], session['password'], update_supervisor_schema[0], update_supervisor_schema[1])

            return update_sp_result

        # if they a super visor and no longer
        elif supervisor == "no":
            
            delete_supervisor_schema = e_schema.delete_supervisor(employee_id)

            # Assuming dao.add expects the SQL query first and then the data
            delete_sp_result = dao.add(session['username'], session['password'], delete_supervisor_schema[0], delete_supervisor_schema[1])

            return delete_sp_result

        # if new hourly rate is place than update
        if rate is not " ":

            update_houlry_schema = e_schema.update_rate(rate, employee_id)

             # Assuming dao.add expects the SQL query first and then the data
            update_hourly_result = dao.update_info(session['username'], session['password'], update_houlry_schema[0], update_houlry_schema[1])

            return update_hourly_result

        return result_update_employee

    # returns 0 success 2 never signed in 1 Error with DB 
    return logged_check
    
