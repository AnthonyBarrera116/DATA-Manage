from flask import Flask, render_template, request, session, redirect, url_for

import mysql.connector
from mysql.connector import Error

app = Flask(__name__)



# Configure your MySQL database connection
def dbconnection(username, password):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user=username,
            password=password,
            database="zoo",
            port=3307
        )
        if connection.is_connected():
            print("Connected to MySQL")
            return connection
        
    except Error as e:
        print("Error while connecting to MySQL", e)
        return None




def get_db():
    try:
        connection = mysql.connector.connect(
                host="localhost",
                user=session["username"],
                password=session["password"],
                database="zoo",
                port=3307
        )
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)  # Using dictionary cursor for easier handling of results

            list_of_all = {}

            all_tables = [
                        "employee",
                        "animal",
                        "animalcare",
                        "animalshow",
                        "building",
                        "caresforspecies",
                        "concession",
                        "customerservice",
                        "enclosure",
                        "host",
                        "hourlyrate",
                        "maintenance",
                        "revenueevents",
                        "species",
                        "supervises",
                        "ticketseller",
                        "veterinarian",
                        "zooadmission",
            ]

            for l in all_tables:

                query = "SELECT * FROM " + l

                cursor.execute(query)
                records = cursor.fetchall()
                list_of_all[l] = records

            if list_of_all:
                connection.close()
                return list_of_all
                    
            else:
                return "No data"
                
    except Error as e:
        print("Error while connecting to MySQL", e)
        return None

# Close the database connection
def close_connection(connection):
    if connection.is_connected():
        connection.close()
        print("MySQL connection closed")




@app.route('/')
def home():
    return render_template('MainPage.html', message='')



@app.route('/login')
def login_page():
    return render_template('login.html', message='')



@app.route('/login', methods=['POST'])
def login():

    render_template('login.html', message='')

    # Access form data from the request
    entered_username = request.form.get('username')
    entered_password = request.form.get('password')

    # Perform your login logic with MySQL database
    db_connection = dbconnection(entered_username, entered_password)
    try:
        db_connection.is_connected()
        
        session['username'] = entered_username
        session['password'] = entered_password
        db_connection.close()

        return redirect(url_for('Menu'))
    
    except:
        return redirect(url_for('login', error=1))
    

    
@app.route('/InsertAnimal', methods=['POST'])
def InsertAnimal():
    db_connection = dbconnection(session['username'], session['password'])

    try:
        db_connection.is_connected()
        db_connection.close()

        return render_template('AnimalInsert.html')
    
    except:
        return redirect(url_for('Menu', error=1))
    


@app.route('/Insert', methods=['POST'])
def Insert():
    db_connection = dbconnection(session['username'], session['password'])

    try:
        db_connection.is_connected()
        db_connection.close()

        return redirect(url_for('Menu'))
    
    except:
        return redirect(url_for('AnimalInsert.html', error=1))
    
    


@app.route('/Menu')
def Menu():
   
   
   results = get_db()
   
   return render_template('Menu.html',records = results)
    
    


if __name__ == '__main__':
    app.run(debug=True)
