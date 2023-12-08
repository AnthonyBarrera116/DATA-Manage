# imports for secret for Flask and flask libr
from flask import Flask, render_template, request, redirect, url_for
import secrets

# Import User Controller
import Usercontroller as user

# For app
app = Flask(__name__, static_url_path='/static')

# Replace with a strong and unique secret key
app.secret_key = secrets.token_hex(16)

#_______________________________Main Page___________________________________________________________

# Main Page
@app.route('/')
def home():
    
    # returns mainpage
    return render_template('MainPage.html', message='')


#_______________________________Login/login Page___________________________________________________________


# Login Page
@app.route('/login')
def login_page():
    return render_template('login.html', message='')


# Login checking field
@app.route('/login', methods=['POST'])
def login():

    # gets username and passord from user
    entered_username = request.form.get('username')
    entered_password = request.form.get('password')

    # checks if user can login with account inputed
    logged_in_checker = user.logging_in(entered_username,entered_password)
    
    # success
    if logged_in_checker == 0:

        return redirect(url_for('Menu'))
    
    # fail
    else:
        return redirect(url_for('login', error=logged_in_checker))
    
#___________________________________Menu Page______________________________________________________________________


# Manu page route
@app.route('/Menu')
def Menu():
   
   return render_template('Menu.html')#,records = results)
    

#_______________________________Animal Insert/Update___________________________________________________________

# Routes to Animal Management Page and displays all info of animal info
@app.route('/AnimalManagement', methods=['POST',"GET"])
def animal_management():
    
    # retirevs info from db 0 = data is available and sent to html page 1 = not data in dd 
    result = user.get_info(["animal","enclosure","species"])

    # db is connected and retireved empty db or had db info Handles with displaying of no data in html file
    
    if int(result[0]) == 0:
        
        return render_template('AnimalManagement.html',records = result[1])
    
    # Not signed in
    else:
        
        return redirect(url_for('login_page', error=result[0]))


# Inserts new Animal
# Ask all fields below. ID is incremented
# ALL INPUTS MUST BE PUT INTO THE FIELD
@app.route('/InsertAnimal', methods=['POST'])
def insert_new_animal():

    # Requests values from HTML FILE
    species_id = request.form.get('species_ID')
    status = request.form.get('status')
    birth_year = request.form.get('birth_year')
    enclosure_id = request.form.get('enclosure_id')

    # Sends to controller 0 = success, 1 = Error with  2 = never singed in
    result = user.insert_animal(species_id, status, birth_year,enclosure_id)

    # Success
    if result == 0:
         
        return redirect(url_for('Menu'))
    
    # Not logged in
    elif result == 2:
            
        return redirect(url_for('login',error=result))
        
    # Error with inputs
    else:
            
        return redirect(url_for('animal_management',error=result))
    


# Updates Animal info 
# CHANGING OF DB ARE ANIMAL SPEICES,STATUS,BIRTH YEAR, AND ENCLOSURE ID
# VALUES CAN BE LEFT EMPTY AND WILL ONLY UPDATES FIELDS INPUTED BESIDES ID
@app.route('/UpdateAnimal', methods=['POST'])
def update_animal_info():

    # Requests values from HTML FILE
    animal_id = request.form.get('animal_ID')
    status = request.form.get('status')
    enclosure_id = request.form.get('enclosure_id')

    # Sends to controller 0 = success, 1 = user not logged in (SHOULDN't HAVE ACCESS) and 2 = nothing was updated, wrong ID, or already exists
    result = user.update_animal(animal_id,status,enclosure_id)

    print(result)
    
    # Success
    if result == 0:
         
        return redirect(url_for('Menu'))
    
    # Not logged in
    elif result == 2:
            
            return redirect(url_for('login', error=result))
    
    # Error with inputs
    else:
            
            return redirect(url_for('animal_management',error=result))
    

#_______________________________Employee Insert/Update___________________________________________________________

# Routes to Employee Management Page and displays all info of Employee info
@app.route('/EmployeeManagement', methods=['POST',"GET"])
def Employee_management():
    
    # retirevs info from db 0 = data is available and sent to html page 1 = not data in dd 
    result = user.get_info(["employee","hourlyrate","supervises"])

    # db is connected and retireved empty db or had db info Handles with displaying of no data in html file
    if int(result[0]) == 0:
        
        return render_template('EmployeeManagement.html',records = result[1])
    
    # Not signed in
    else:

        return redirect(url_for('login_page', error=result[0]))

# Inserts new Employee
# Ask all fields below. ID is incremented
# ALL INPUTS MUST BE PUT INTO THE FIELD
@app.route('/InsertEmployee', methods=['POST'])
def insert_new_Employee():

    # Requests values from HTML FILE
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    minit = request.form.get('minit')
    job_type = request.form.get('job_type')
    start_date = request.form.get('start_date')
    street = request.form.get('street')
    city = request.form.get('city')
    state = request.form.get('state')
    zip = request.form.get('zip')
    supervisor = request.form.get('supervisor')
    rate = request.form.get('rate')

    # Sends to controller 0 = success, 1 = user not logged in (SHOULDN't HAVE ACCESS) and 2 = nothing was updated, wrong ID, or already exists
    result = user.insert_employee(first_name, last_name, minit,job_type,start_date,street,city,state,zip,supervisor,rate)

    # Success
    if result == 0:
         
        return redirect(url_for('Menu'))
        
    # Not logged in
    elif result == 2:
            
        return redirect(url_for('login', error=result))
    
    # Error with inputs
    else:
            
        return redirect(url_for('Employee_management',error=result))


# Updates Employee info 
# CHANGING OF DB ARE EMPLOYEE JOB TYPE, STREET,CITY,STATE,CITY,STATE,ZIP,SUPERVISOR, AND RATE
# VALUES CAN BE LEFT EMPTY AND WILL ONLY UPDATES FIELDS INPUTED BESIDES ID
@app.route('/UpdateEmployee', methods=['POST'])
def update_Employee_info():


    # Requests values from HTML FILE
    employee_id = request.form.get('employee_ID')
    update_job_type = request.form.get('update_job_type')
    update_street = request.form.get('update_street')
    update_city = request.form.get('update_city')
    update_state = request.form.get('update_state')
    update_zip = request.form.get('update_zip')
    update_supervisor = request.form.get('update_supervisor')
    update_rate = request.form.get('update_rate')

    # Sends to controller 0 = success, 1 = user not logged in (SHOULDN't HAVE ACCESS) and 2 = nothing was updated, wrong ID, or already exists
    result = user.update_employee(employee_id,update_job_type,update_street,update_city,update_state,update_zip,update_supervisor,update_rate)
    
    # Success
    if result == 0:
         
        return redirect(url_for('Menu'))
    
    # Not logged in
    elif result == 2:
            
            return redirect(url_for('login', error=result))
    
    # Error with inputs
    else:
            
            return redirect(url_for('Employee_management',error=result))
    



#_______________________________Building Insert/Update___________________________________________________________    

# Routes to Building Management Page and displays all info of building info
@app.route('/BuildingManagement', methods=['POST',"GET"])
def building_management():
    
    # retirevs info from db 0 = data is available and sent to html page 1 = not data in dd 
    result = user.get_info(["building","enclosure"])

    # db is connected and retireved empty db or had db info Handles with displaying of no data in html file
    if int(result[0]) == 0:

        return render_template('BuildingManagement.html',records = result[1])
    
    # Not signed in
    else:
        
        return redirect(url_for('login_page', error=result[0]))


# Inserts new Building
# Asks for Building name and Building type. ID is incremented
# ALL INPUTS MUST BE PUT INTO THE FIELD
@app.route('/InsertBuilding', methods=['POST'])
def insert_new_building():

    # Requests values from HTML FILE
    building_name= request.form.get('name_building')
    type = request.form.get('type')
    enclosure= request.form.get('enclosure')
    sq_ft = request.form.get('sq_ft')

    # Sends to controller 0 = success, 1 = user not logged in (SHOULDN't HAVE ACCESS) and 2 = nothing was updated, wrong ID, or already exists
    result = user.insert_building(building_name, type, enclosure, sq_ft)

    # Success
    if result == 0:
         
        return redirect(url_for('Menu'))
        
    # Not logged in
    elif result == 2:
            
        return redirect(url_for('login', error=result))
    
    # Error with inputs
    else:
            
        return redirect(url_for('building_management',error=result))
    



# Updates Building info 
# CHANGING OF DB ARE BUILDING NAME AND BUILDING TYPE
# VALUES CAN BE LEFT EMPTY AND WILL ONLY UPDATES FIELDS INPUTED BESIDES ID
@app.route('/UpdateBuilding', methods=['POST'])
def update_building_info():

    # Requests values from HTML FILE
    building_id = request.form.get('building_ID')
    building_name= request.form.get('update_name')
    type = request.form.get('update_type')

    # Sends to controller 0 = success, 1 = user not logged in (SHOULDN't HAVE ACCESS) and 2 = nothing was updated, wrong ID, or already exists
    result = user.update_building(building_id ,building_name, type)
    

    # Success
    if result == 0:
         
        return redirect(url_for('Menu'))
        
    # Not logged in
    elif result == 2:
            
        return redirect(url_for('login', error=result))
    
    # Error with inputs
    else:
            
        return redirect(url_for('building_management',error=result))


#_______________________________Attraction Insert/Update___________________________________________________________

# Routes to Animal Management Page and displays all info of animal info
@app.route('/AttractionManagement', methods=['POST',"GET"])
def attraction_management():
    
    # retirevs info from db 0 = data is available and sent to html page 1 = not data in dd 
    result = user.get_info(["AnimalShow","species","RevenueType"])

    # db is connected and retireved empty db or had db info Handles with displaying of no data in html file
    if int(result[0]) == 0:
        
        return render_template('AttractionManagement.html',records = result[1])
    
    # Error with account = 1 or never logged in = 3
    else:
        
        return redirect(url_for('login_page', error=result[0]))
    
# Inserts new Animal
# Ask all fields below. ID is incremented
# ALL INPUTS MUST BE PUT INTO THE FIELD
@app.route('/InsertAttraction', methods=['POST'])
def insert_new_attraction():

    # Requests values from HTML FILE
    name_attraction = request.form.get('name_attraction')
    s_price = request.form.get('s_price')
    a_price = request.form.get('a_price')
    c_price = request.form.get('c_price')
    num_show = request.form.get('num_show')
    num_req = request.form.get('num_req')
    species_id = request.form.get('species_id')

    # Sends to controller 0 = success, 1 = Error with  2 = never singed in
    result = user.insert_attraction(name_attraction, s_price, a_price,c_price,num_show,num_req,species_id)

    # Success
    if result == 0:
         
        return redirect(url_for('Menu'))
    
    # Not logged in
    elif result == 2:
            
        return redirect(url_for('login',error=result))
        
    # Error with inputs
    else:
            
        return redirect(url_for('attraction_management',error=result))
    


# Updates Animal info 
# CHANGING OF DB ARE ANIMAL SPEICES,STATUS,BIRTH YEAR, AND ENCLOSURE ID
# VALUES CAN BE LEFT EMPTY AND WILL ONLY UPDATES FIELDS INPUTED BESIDES ID
@app.route('/UpdateAttraction', methods=['POST'])
def update_attraction_info():

    # Requests values from HTML FILE
    id_attraction = request.form.get('id_attraction')
    s_price = request.form.get('s_price')
    a_price = request.form.get('a_price')
    c_price = request.form.get('c_price')
    num_show = request.form.get('num_show')

     # Sends to controller 0 = success, 1 = Error with  2 = never singed in
    result = user.update_attraction(id_attraction,s_price,a_price,c_price,num_show)
    
    # Success
    if result == 0:
         
        return redirect(url_for('Menu'))
    
    # Not logged in
    elif result == 2:
            
            return redirect(url_for('login', error=result))
    
    # Error with inputs
    else:
            
            return redirect(url_for('attraction_management',error=result))
    


#__________________________________________Main________________________________________________________________

# Main code running
if __name__ == '__main__':

    app.run(debug=True)
    