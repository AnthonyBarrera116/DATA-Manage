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
    
    # success 0
    if logged_in_checker == 0:

        return redirect(url_for('Menu'))
    
    # fail 1
    else:
        return redirect(url_for('login', error=logged_in_checker))
    
#___________________________________Menu Page______________________________________________________________________


# Manu page route
@app.route('/Menu')
def Menu():
   
   logged = user.if_user_logged_in()

   if logged == 0:
        
        return render_template('Menu.html')#,records = results)
   
   else:
       
        return redirect(url_for('login_page', error=logged))

#_______________________________Animal Insert/Update___________________________________________________________

# Routes to Animal Management Page and displays all info of animal info
@app.route('/AnimalManagement', methods=['POST',"GET"])
def animal_management():
    
    # retirevs info from db 0 = data is available and sent to html page 1 = not data in dd 
    result = user.get_info(["animal","enclosure","species"])
    
    # DB has data 0
    if int(result[0]) == 0:
        
        return render_template('AnimalManagement.html',records = result[1])
    
    # DB is empty 3
    elif int(result[0]) == 3:

        return render_template('BuildingManagement.html',records = [])
    
    # Not signed in 2
    else:
        
        return redirect(url_for('login_page', error=result[0]))


# Inserts new Animal
@app.route('/InsertAnimal', methods=['POST'])
def insert_new_animal():

    # Requests values from HTML FILE
    species_id = request.form.get('species_ID')
    status = request.form.get('status')
    birth_year = request.form.get('birth_year')
    enclosure_id = request.form.get('enclosure_id')

    # 0 = success to add 1 = connection fail 2 = not logged in 4 = duplicate/exist 7 = constarint failure for result_animal_insert
    result = user.insert_animal(species_id, status, birth_year,enclosure_id)

    # Success 0
    if result == 0:
         
        return redirect(url_for('animal_management'))
    
    # Not logged in 2
    elif result == 2:
            
        return redirect(url_for('login',error=result))
        
    # Error with 1 = connection fail 4 = duplicate/exist 7 = constarint failure for result_animal_insert
    else:
            
        return redirect(url_for('animal_management',error=result))
    


# Updates Animal info 
@app.route('/UpdateAnimal', methods=['POST'])
def update_animal_info():

    # Requests values from HTML FILE
    animal_id = request.form.get('animal_ID')
    status = request.form.get('status')
    enclosure_id = request.form.get('enclosure_id')

    # 0 = success 1 = connection failure 2 = not loigged in 6 = doesn't exist 7 = constraint for update_animal_result
    result = user.update_animal(animal_id,status,enclosure_id)

    print(result)
    
    # Success 0
    if result == 0:
         
        return redirect(url_for('animal_management'))
    
    # Not logged in 2
    elif result == 2:
            
            return redirect(url_for('login', error=result))
    
    # 1 = connection failure 6 = doesn't exist 7 = constraint for update_animal_result
    else:
            
            return redirect(url_for('animal_management',error=result))
    

#_______________________________Employee Insert/Update___________________________________________________________

# Routes to Employee Management Page and displays all info of Employee info
@app.route('/EmployeeManagement', methods=['POST',"GET"])
def Employee_management():
    
    # retirevs info from db 0 = data is available and sent to html page 1 = not data in dd 
    result = user.get_info(["employee","hourlyrate","supervises"])

    # DB has data 0
    if int(result[0]) == 0:
        
        return render_template('EmployeeManagement.html',records = result[1])
    
    # DB is empty 3
    elif int(result[0]) == 3:
        return render_template('BuildingManagement.html',records = [])
    
    # Not signed in 2
    else:

        return redirect(url_for('login_page', error=result[0]))

# Inserts new Employee
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

    # 0 = success to add 1 = connection fail 4 = duplicate/exist 7 = constarint failure for result_animal_insert
    result = user.insert_employee(first_name, last_name, minit,job_type,start_date,street,city,state,zip,supervisor,rate)

    # Success 0
    if result == 0:
         
        return redirect(url_for('Employee_management'))
        
    # Not logged in 2
    elif result == 2:
            
        return redirect(url_for('login', error=result))
    
    # 0 = success to add 1 = connection fail 4 = duplicate/exist 7 = constarint failure for result_animal_insert
    else:
            
        return redirect(url_for('Employee_management',error=result))


# Updates Employee info 
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

    # 0 = success 1 = connection failure 2 = not loigged in 6 = doesn't exist 7 = constraint for update_animal_result
    result = user.update_employee(employee_id,update_job_type,update_street,update_city,update_state,update_zip,update_supervisor,update_rate)
    
    # Success 0
    if result == 0:
         
        return redirect(url_for('Employee_management'))
    
    # Not logged in 2
    elif result == 2:
            
            return redirect(url_for('login', error=result))
    
   # 1 = connection failure  6 = doesn't exist 7 = constraint for update_animal_result
    else:
            
            return redirect(url_for('Employee_management',error=result))
    



#_______________________________Building Insert/Update___________________________________________________________    

# Routes to Building Management Page and displays all info of building info
@app.route('/BuildingManagement', methods=['POST',"GET"])
def building_management():
    
    # retirevs info from db 0 = data is available and sent to html page 1 = not data in dd 
    result = user.get_info(["building","enclosure"])

    # DB has data 0
    if int(result[0]) == 0:

        return render_template('BuildingManagement.html',records = result[1])
    
    # DB is empty 3
    elif int(result[0]) == 3:
        return render_template('BuildingManagement.html',records = [])
    
    # Not signed in 2
    else:
        
        return redirect(url_for('login_page', error=result[0]))


# Inserts new Building
@app.route('/InsertBuilding', methods=['POST'])
def insert_new_building():

    # Requests values from HTML FILE
    building_name= request.form.get('name_building')
    type = request.form.get('type')
    enclosure= request.form.get('enclosure')
    sq_ft = request.form.get('sq_ft')

    # 0 = success to add 1 = connection fail 2 = not logged in 4 = duplicate/exist 7 = constarint failure for result_animal_insert
    result = user.insert_building(building_name, type, enclosure, sq_ft)

    # Success 0
    if result == 0:
         
        return redirect(url_for('building_management'))
        
    # Not logged in 2
    elif result == 2:
            
        return redirect(url_for('login', error=result))
    
    # Error with 1 = connection fail 4 = duplicate/exist 7 = constarint failure for result_animal_insert
    else:
            
        return redirect(url_for('building_management',error=result))
    

# Updates Building info 
@app.route('/UpdateBuilding', methods=['POST'])
def update_building_info():

    # Requests values from HTML FILE
    building_id = request.form.get('building_ID')
    building_name= request.form.get('update_name')
    type = request.form.get('update_type')

    # 0 = success 1 = connection failure 2 = not loigged in 6 = doesn't exist 7 = constraint for update_animal_result
    result = user.update_building(building_id ,building_name, type)
    

    # Success 0
    if result == 0:
         
        return redirect(url_for('building_management'))
        
    # Not logged in 2
    elif result == 2:
            
        return redirect(url_for('login', error=result))
    
    # 1 = connection failure 6 = doesn't exist 7 = constraint for update_animal_result
    else:
            
        return redirect(url_for('building_management',error=result))


#_______________________________Attraction Insert/Update___________________________________________________________

# Routes to Attraction Management Page and displays all info of animal info
@app.route('/AttractionManagement', methods=['POST',"GET"])
def attraction_management():
    
    # retirevs info from db 0 = data is available and sent to html page 1 = not data in dd 
    result = user.get_info(["AnimalShow","species","RevenueType"])

    # DB has data 0
    if int(result[0]) == 0:
        
        return render_template('AttractionManagement.html',records = result[1])
    
    # DB is empty 3
    elif int(result[0]) == 3:
        return render_template('AttractionManagement.html',records = [])
    
    # Not signed in 2
    else:
        
        return redirect(url_for('login_page', error=result[0]))
    

# Inserts New Attraction
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

    # 0 = success to add 1 = connection fail 2 = not logged in 4 = duplicate/exist 7 = constarint failure for result_animal_insert
    result = user.insert_attraction(name_attraction, s_price, a_price,c_price,num_show,num_req,species_id)

    #  Success 0
    if result == 0:
         
        return redirect(url_for('attraction_management'))
    
    # Not logged in 2
    elif result == 2:
            
        return redirect(url_for('login',error=result))
        
    # Error with 1 = connection fail 4 = duplicate/exist 7 = constarint failure for result_animal_insert
    else:
            
        return redirect(url_for('attraction_management',error=result))
    
# update Attraction
@app.route('/UpdateAttraction', methods=['POST'])
def update_attraction_info():

    # Requests values from HTML FILE
    id_attraction = request.form.get('id_attraction')
    s_price = request.form.get('s_price')
    a_price = request.form.get('a_price')
    c_price = request.form.get('c_price')
    num_show = request.form.get('num_show')

    # 0 = success 1 = connection failure 2 = not loigged in 6 = doesn't exist 7 = constraint for update_animal_result
    result = user.update_attraction(id_attraction,s_price,a_price,c_price,num_show)
    
    # Success 0
    if result == 0:
         
        return redirect(url_for('attraction_management'))
    
    # Not logged in 2
    elif result == 2:
            
            return redirect(url_for('login', error=result))
    
    # 1 = connection failure 6 = doesn't exist 7 = constraint for update_animal_result
    else:
            
            return redirect(url_for('attraction_management',error=result))
    

#_______________________________Attractions Daily zoo___________________________________________________________

# Routes to Revenue and displays all info 
@app.route('/ViewRev', methods=['POST',"GET"])
def view():
    
    # retirevs info from db 0 = data is available and sent to html page 1 = not data in dd 
    result = user.get_info_revenue()

    # DB has data 0
    if int(result[0]) == 0:
        
        return render_template('Revenue.html',records = result[1])
    
    # DB is empty 3
    elif int(result[0]) == 3:

        return render_template('Revenue.html',records = [])
    
    # Not signed in 2
    else:
        
        return redirect(url_for('login_page', error=result[0]))

# insert Revenue
@app.route('/InsertRevenue', methods=['POST'])
def insert_new_rev():

    # Requests values from HTML FILE
    name = request.form.get('Name')
    revenue = request.form.get('revenue')
    number_sold = request.form.get('number_sold')
    datetime_sold = request.form.get('datetime_sold')
    reveune_id = request.form.get('reveune_id')

    # 0 = success to add 1 = connection fail 4 = duplicate/exist 7 = constarint failure for result_animal_insert
    result = user.insert_rev(name, revenue, number_sold, datetime_sold,reveune_id)

    # Success 0*
    if result == 0:
         
        return redirect(url_for('view'))
    
    # Not logged in 2
    elif result == 2:
            
        return redirect(url_for('login',error=result))
        
    # 0 = success to add 1 = connection fail 4 = duplicate/exist 7 = constarint failure for result_animal_insert
    else:
            
        return redirect(url_for('view',error=result))
  
#__________________________________________report________________________________________________________________

@app.route('/ManageReportGivenDay', methods=['POST',"GET"])
def report_view_given():
  
   logged = user.if_user_logged_in()

   if logged == 0:
        
        return render_template('ManageReportGivenDay.html', records = [])
   
   else:
       
        return redirect(url_for('login_page', error=logged))
   
@app.route('/RevReportByDay', methods=['POST',"GET"])
def report_given():
  
   date = request.form.get('date')

   report = user.report_rev(date)
      
   if report == 2:
       
        return redirect(url_for('login_page', error=report))
   
   else:
        
        return render_template('ManageReportGivenDay.html', records = report[1])
   
   

#__________________________________________report________________________________________________________________
@app.route('/ManageReportProduce', methods=['POST',"GET"])
def report_view_produce():
  
   logged = user.if_user_logged_in()

   results = user.produce_report()

   if logged == 0:
        
        return render_template('ManageReportProduce.html', records = results)
   
   else:
       
        return redirect(url_for('login_page', error=logged))
   



#__________________________________________report________________________________________________________________
@app.route('/ManageReportTimePeriodTop', methods=['POST',"GET"])
def report_view_given_time_top():
  
   logged = user.if_user_logged_in()

   if logged == 0:
        
        return render_template('ManageReportTimePeriodTop.html', records = [])
   
   else:
       
        return redirect(url_for('login_page', error=logged))
   
@app.route('/TopThree', methods=['POST',"GET"])
def report_top_three():
  
   start_date = request.form.get('start_date')
   end_date = request.form.get('end_date')

   report = user.top_report(start_date,end_date)
   
   if report == 2:
       
        return redirect(url_for('login_page', error=report))
   
   else:
        
        return render_template('ManageReportTimePeriodTop.html', records = report[1])
   
   


#__________________________________________report________________________________________________________________
@app.route('/ManageReportMonth', methods=['POST',"GET"])
def report_best_view():
  
   logged = user.if_user_logged_in()

   if logged == 0:
        
        return render_template('ManageReportMonth.html', records = [])
   
   else:
       
        return redirect(url_for('login_page', error=logged))
   
@app.route('/BestDays', methods=['POST',"GET"])
def best_days_report():
  
   month = request.form.get('month')

   year = request.form.get('year')

   report = user.best_report(month,year)

   if report == 2:
       
        return redirect(url_for('login_page', error=report))
   
   else:
        
        return render_template('ManageReportMonth.html', records = report[1])

#__________________________________________report________________________________________________________________
@app.route('/ManageReportTimePeriodAvg', methods=['POST',"GET"])
def report_view_avg():
  
   logged = user.if_user_logged_in()

   if logged == 0:
        
        return render_template('ManageReportTimePeriodAvg.html', records = [])
   
   else:
       
        return redirect(url_for('login_page', error=logged))
    

@app.route('/AvgRev', methods=['POST',"GET"])
def avg_report():
  
   start_date = request.form.get('start_date')

   end_date = request.form.get('end_date')

   report = user.average_report(start_date,end_date)

   print(report)

   if report == 2:
       
        return redirect(url_for('login_page', error=report))
   
   else:
        
        return render_template('ManageReportTimePeriodAvg.html', records = report)



#__________________________________________Main________________________________________________________________

# Main code running
if __name__ == '__main__':

    app.run(debug=True)
    