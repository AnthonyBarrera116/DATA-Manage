# import flask session allows to save user session 
from flask import session

# Import DAO for db connection
import DAO as dao

import AnimalSchema as a_schema
import BuildingSchema as b_schema
import EmployeeSchema as e_schema
import AttractionSchema as attr_schema
import RevenueSchema as rev_schema

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
        return 2, []

# get info fof tables requests for retriveing data fro viewing
def get_info_revenue():

    if 'username' in session and 'password' in session:

        # Get tables data
        tables_data = dao.get_revenue_info(session['username'], session['password'])

        # return db info, if the db is empty the value is 3, if it is 1 connection to db wasn't established
        return tables_data

    else:

        # 2 mean they never logged in
        return 2, []


#_______________________________Animal Insert/Update___________________________________________________________

# inserts new animal 
def insert_animal(species_id, status, birth_year,enclosure_id):

    # returns 0 = user is logged in 2 = never logged in
    logged_check = if_user_logged_in()

    # checks if user is logged in
    if logged_check == 0:

        schema_sql = []

        schema_data = []

        # fetches schmema of animal insert with building ID and how big
        insert_animal_schema = a_schema.animal_insert_schema(species_id, status, birth_year,enclosure_id)

        schema_sql.append(insert_animal_schema[0])

        schema_data.append(insert_animal_schema[1])

        # adds if 0 = success to add 1 = connection fail 4 = duplicate/exist 7 = constarint failure for result_animal_insert
        result_animal_insert = dao.add_update(session['username'],session['password'],schema_sql,schema_data,"insert animal")

        # returns 0 = success 1 = db connectin error 4 = duplicate 7 = constraint from result_animal_insert
        return result_animal_insert

    # returns 2 = never logged in
    return logged_check

        
# updates animal with fields
def update_animal(animal_id, new_status=None, enclosure_id=None):
    
    # returns 0 = user is logged in 2 = never logged in
    logged_check = if_user_logged_in()

    # checks if user is logged
    if  logged_check == 0:

        # fetches schmema of animal update 
        animal_schema = a_schema.animal_update_schema(animal_id, new_status, enclosure_id)

        # Nothing updated fields inputed (empty fields)
        if animal_schema == []:

            # 5 = empty fields
            return 5
        
        schema_sql = []

        schema_data = []
        
        schema_sql.append(animal_schema[0])

        schema_data.append(animal_schema[1])

        # Update animal 0 = success 1 = connection failure 6 = doesn't exist 7 = constraint for update_animal_result
        animal_result = dao.add_update(session['username'], session['password'], schema_sql,  schema_data,"update animal")

        # returns 0 = success 1 = connection failure 6 = doesn't exist 7 = constraint from update_animal_result
        return animal_result

   # return 2 = not logged in 
    return logged_check
    
    
    
#_______________________________Building Insert/Update___________________________________________________________    

# inserts new building 
def insert_building(building_name, building_type, enclosure, sq_ft):

    # returns 0 = user is logged in 2 = never logged in
    logged_check = if_user_logged_in()

    # checks if user is logged in
    if logged_check == 0:

        schema_sql = []

        schema_data = []

        # fetches schmema of building insert with building ID
        insert_building_schema = b_schema.building_insert_schema(building_name, building_type)

        insert_enclousre_schema = b_schema.enclosure_insert_schema(sq_ft)

        schema_sql.append(insert_building_schema[0])

        schema_sql.append(insert_enclousre_schema[0])

        schema_data.append(insert_building_schema[1])

        schema_data.append(insert_enclousre_schema[1])

        result_building_insert = dao.add_update(session['username'], session['password'], schema_sql, schema_data, "insert building/enclosure")
    
        # 1 = connection fail 4 = duplicate 7 = constraint error
        return result_building_insert

    # returns 2 = never logged in for logged_check
    return logged_check

# updates Building with fields
def update_building(building_id, building_name = None, type = None):

    # returns 0 = user is logged in 2 = never logged in
    logged_check = if_user_logged_in()

    # checks if user is logged in
    if logged_check == 0:
        
        # fetches schmema of update building with building ID
        update_building_schema = b_schema.building_update_schema(building_id,building_name,type)

        # if empty fields
        if update_building_schema == []:
                
            return 5

        schema_sql = []

        schema_data = []
        
        schema_sql.append(update_building_schema[0])

        schema_data.append(update_building_schema[1])

        # Update Building
        update_building_result = dao.add_update(session['username'], session['password'],schema_sql, schema_data ,"update building")

        # returns 0 = success 1 = connection issuse 6 = doesn't exist 7 = constraint 
        return update_building_result
            
    # returns 0 success 2 never signed in 1 Error with DB
    return logged_check


#_______________________________Employee Insert/Update___________________________________________________________    

# inserts new employee 
def insert_employee(first_name, last_name, minit, job_type, start_date, street, city, state, zip_code, supervisor,rate):

    # returns 0 = user is logged in 2 = never logged in
    logged_check = if_user_logged_in()

    # checks if user is logged in
    if logged_check == 0:
        
        schema_sql = []

        schema_data = []

        # set of employee data
        employee_schema = e_schema.employee_insert_schema(first_name, last_name, minit, job_type, start_date, street, city, state, zip_code)

        hourly_schema = e_schema.hourly_insert_schema(rate)

        schema_sql.append(employee_schema[0])

        schema_sql.append(hourly_schema[0])

        schema_data.append(employee_schema[1])

        schema_data.append(hourly_schema[1])

        if supervisor == "yes":

            supervisor_schema = e_schema.insert_supervisor()

            schema_sql.append(supervisor_schema[0])

            schema_data.append(supervisor_schema[1])
        
        # adds if 0 = success to add 1 = connection fail 4 = duplicate/exist 7 = constarint failure for result_buildung_insert
        insert_person_result = dao.add_update(session['username'], session['password'], schema_sql, schema_data,"employee insert/rate/supervisor")

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

        employee_schema = e_schema.employee_update_schema(employee_id,job_type, street, city, state, zip_code)
        
        schema_sql = []

        schema_data = []

        if employee_schema[1] != []:
                
            schema_sql.append(employee_schema[0])

            schema_data.append(employee_schema[1])
    
        
        if supervisor == "yes":

            supervisor_schema = e_schema.insert_supervisor(employee_id)

            schema_sql.append(supervisor_schema[0])

            schema_data.append(supervisor_schema[1])

        elif supervisor == "no":
            
            supervisor_schema = e_schema.delete_supervisor(employee_id)

            schema_sql.append(supervisor_schema[0])

            schema_data.append(supervisor_schema[1])

        # if new hourly rate is place than update
        if rate is not "":

            update_houlry_schema = e_schema.update_rate(rate, employee_id)

            schema_sql.append(update_houlry_schema[0])

            schema_data.append(update_houlry_schema[1])

        if schema_sql == []:

            return 5

        employee_result = dao.add_update(session['username'], session['password'], schema_sql, schema_data,"employee update")


        return employee_result

    # returns 0 success 2 never signed in 1 Error with DB 
    return logged_check
    
#___________________________________________Attrcation______________________________________________________________

# inserts new revenuetype 
def insert_attraction(name_attraction, s_price, a_price,c_price,num_show,num_req,species_id):

    # returns 0 = user is logged in 2 = never logged in
    logged_check = if_user_logged_in()

    # checks if user is logged in
    if logged_check == 0:

        schema_sql = []

        schema_data = []

        # fetches schmema of revenuetype insert with building ID and how big

        attraction_schema = attr_schema.attraction_insert_schema(name_attraction,s_price, a_price,c_price,num_show,num_req,3,species_id)

        schema_sql.append(attraction_schema[0])

        schema_data.append(attraction_schema[1])

        result_attraction_insert = dao.add_update(session['username'],session['password'],schema_sql,schema_data,"insert revenuetype/attraction")

        # returns 0 = success 1 = db connectin error 4 = duplicate 7 = constraint from result_revenuetype_insert
        return result_attraction_insert

    # returns 2 = never logged in
    return logged_check

# updates animal with fields
def update_attraction(attraction_id, s_price,a_price,c_price,num_show):
    
    # returns 0 = user is logged in 2 = never logged in
    logged_check = if_user_logged_in()

    # checks if user is logged
    if  logged_check == 0:

        # fetches schmema of animal update 
        update_animal_schema = attr_schema.attraction_update_schema(attraction_id,s_price,a_price,c_price,num_show)

        # Nothing updated fields inputed (empty fields)
        if update_animal_schema == []:

            # 5 = empty fields
            return 5
        
        schema_sql = []

        schema_data = []

        schema_sql.append(update_animal_schema[0])

        schema_data.append(update_animal_schema[1])
        
        # Update animal 0 = success 1 = connection failure 6 = doesn't exist 7 = constraint for update_animal_result
        update_animal_result = dao.add_update(session['username'], session['password'], schema_sql,  schema_data, "insert revenuetype/attraction")

        # returns 0 = success 1 = connection failure 6 = doesn't exist 7 = constraint from update_animal_result
        return update_animal_result

   # return 2 = not logged in 
    return logged_check
    
#___________________________________________Revenue______________________________________________________________

# inserts new revenuetype 
def insert_rev(name, revenue, number_sold, datetime_sold,reveune_id):

    # returns 0 = user is logged in 2 = never logged in
    logged_check = if_user_logged_in()

    # checks if user is logged in
    if logged_check == 0:

        schema_sql = []

        schema_data = []

        # fetches schmema of revenuetype insert with building ID and how big
        revenue_schema = rev_schema.revunetype_insert_schema(name,revenue, number_sold, datetime_sold,reveune_id)

        schema_sql.append(revenue_schema[0])

        schema_data.append(revenue_schema[1])

        result_attraction_insert = dao.add_update(session['username'],session['password'],schema_sql,schema_data,"insert Revenue")

        # returns 0 = success 1 = db connectin error 4 = duplicate 7 = constraint from result_revenuetype_insert
        return result_attraction_insert

    # returns 2 = never logged in
    return logged_check


#___________________________________________Report______________________________________________________________

def report_rev(date):
    # returns 0 = user is logged in 2 = never logged in
    logged_check = if_user_logged_in()

    # checks if user is logged in
    if logged_check == 0:

        revenue_schema = rev_schema.revenue_report(date)

        schema_sql = revenue_schema[0]
        schema_data = revenue_schema[1]

        result_attraction_insert = dao.get_info(session['username'], session['password'], schema_sql, schema_data)

        # returns 0 = success 1 = db connectin error 4 = duplicate 7 = constraint from result_revenuetype_insert
        return result_attraction_insert

    # returns 2 = never logged in
    return logged_check

#___________________________________________Report______________________________________________________________

def produce_report():

    # returns 0 = user is logged in 2 = never logged in
    logged_check = if_user_logged_in()

    # checks if user is logged in
    if logged_check == 0:

        revenue_schema = rev_schema.produce_rep()

        schema_sql = revenue_schema[0]
        schema_data = revenue_schema[1]

        result_attraction_insert = []

        for schmema in schema_sql:

            result_attraction_insert.append(dao.get_info(session['username'], session['password'], schmema, schema_data))

        # returns 0 = success 1 = db connectin error 4 = duplicate 7 = constraint from result_revenuetype_insert
        return result_attraction_insert

    # returns 2 = never logged in
    return logged_check

#___________________________________________Report______________________________________________________________

def top_report(start_date,end_date):

    # returns 0 = user is logged in 2 = never logged in
    logged_check = if_user_logged_in()

    # checks if user is logged in
    if logged_check == 0:

        revenue_schema = rev_schema.top_rep(start_date,end_date)

        schema_sql = revenue_schema[0]
        schema_data = revenue_schema[1]

        result_attraction_insert = dao.get_info(session['username'], session['password'], schema_sql, schema_data)


        # returns 0 = success 1 = db connectin error 4 = duplicate 7 = constraint from result_revenuetype_insert
        return result_attraction_insert

    # returns 2 = never logged in
    return logged_check

#___________________________________________Report______________________________________________________________

def best_report(month,year):

    # returns 0 = user is logged in 2 = never logged in
    logged_check = if_user_logged_in()

    # checks if user is logged in
    if logged_check == 0:

        revenue_schema = rev_schema.best_rep(month,year)

        schema_sql = revenue_schema[0]
        schema_data = revenue_schema[1]

        result_attraction_insert = dao.get_info(session['username'], session['password'], schema_sql, schema_data)


        # returns 0 = success 1 = db connectin error 4 = duplicate 7 = constraint from result_revenuetype_insert
        return result_attraction_insert

    # returns 2 = never logged in
    return logged_check


#___________________________________________Report______________________________________________________________

def average_report(start_date,end_date):

    # returns 0 = user is logged in 2 = never logged in
    logged_check = if_user_logged_in()

    # checks if user is logged in
    if logged_check == 0:

        revenue_schema = rev_schema.avg_rep(start_date,end_date)

        schema_sql = revenue_schema[0]
        schema_data = revenue_schema[1]

        result_attraction_insert = []

        for schmema in schema_sql:

            result_attraction_insert.append(dao.get_info(session['username'], session['password'], schmema, schema_data))

        # returns 0 = success 1 = db connectin error 4 = duplicate 7 = constraint from result_revenuetype_insert
        return result_attraction_insert

    # returns 2 = never logged in
    return logged_check