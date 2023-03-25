from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'your secret key'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'mypass@2002'
app.config['MYSQL_DB'] = 'pythonlogin'

# Intialize MySQL
mysql = MySQL(app)
@app.route('/pythonlogin/', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        #cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)     
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
       
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            # Redirect to home page
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('index.html', msg=msg)

# http://localhost:5000/python/logout - this will be the logout page
@app.route('/pythonlogin/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))

    # http://localhost:5000/pythinlogin/register - this will be the registration page, we need to use both GET and POST requests
@app.route('/pythonlogin/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
                # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, password, email,))
            mysql.connection.commit()
            msg = 'You have successfully registered! Do Login...'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)

# http://localhost:5000/pythinlogin/home - this will be the home page, only accessible for loggedin users
@app.route('/pythonlogin/home')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

# http://localhost:5000/pythinlogin/profile - this will be the profile page, only accessible for loggedin users
@app.route('/pythonlogin/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

#endpoint for search
@app.route('/pythonlogin/search', methods=['GET', 'POST'])
def search():
    if 'loggedin' in session:
        if request.method == "POST":
            username = request.form['username']
            cursor = mysql.connection.cursor()
            heading=["Criminal id","UserName","Contect Number"]
            if request.form.get('name'):
                heading.append("LastName")
                cursor.execute("SELECT cid ,firstname,lastname,phone FROM pythonlogin.criminal_details where firstname LIKE %s ", (username+"%",))
                data = cursor.fetchall()
            if request.form.get('area'):
                heading.append("City")
                cursor.execute("SELECT cid ,firstname,phone,city FROM pythonlogin.criminal_details where city LIKE %s ", (username+"%",))
                data = cursor.fetchall()
           
            if request.form.get('crime'):
                heading.append("CrimeType")
                cursor.execute("SELECT cid ,firstname,phone,CrimeType FROM pythonlogin.criminal_details where CrimeType LIKE %s ", (username+"%",))
                data = cursor.fetchall()
            
        # all in the search box will return all the tuples
            if username == 'all':
                heading.append("city")
                heading.append("CrimeType") 
                cursor.execute("SELECT cid ,firstname,phone,city,CrimeType FROM pythonlogin.criminal_details")
                data = cursor.fetchall() 
            elif len(data) == 0:
                msg='No such data Found with User Name '    
                return render_template ('search.html', msg=msg,username=[username])  
            return render_template('search.html', heading=heading,data=data)#,msg=msg,username=[username])
        return render_template('search.html')
     # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/pythonlogin/detail/<string:id_data>', methods = ['GET','POST'])
def details(id_data):
    if 'loggedin' in session:
            flash("Record view Successfully")
            cur =mysql.connection.cursor()
            cur.execute("select cid,firstname,lastname,address,city,state,country,pincode,ssn_number,countrycode,phone,dob,age,company,occupation,height,weight,bloodtype,fav_color,vehicle,CrimeType FROM criminal_details WHERE cid=%s", (id_data,))
            detail = cur.fetchall()
            #print(detail)
            headings=("Criminal id","First Name","Last Name","Address","City","State","Country","Pincode","SSN NO.","Country Code","Phone","DOB","Age","Company","Occupation","Height","Weight","Blood_Type","Favorite Color" )
            
            return render_template('details.html',headings=headings,detail=detail)
        
    return redirect(url_for('login'))

@app.route('/pythonlogin/addCriminal', methods=['GET','POST'])
def addCriminal():
    # Output message if something goes wrong...
    msg = ''
    if request.method == 'POST':
        # Create variables for easy access
        Gender= request.form['gender']
        NameSet= request.form['NameSet']
        GivenName= request.form['UserName']
        Surname= request.form['Surname']
        StreetAddress= request.form['StreetAddress']
        City= request.form['City']
        StateFull= request.form['State']
        ZipCode= request.form['ZipCode']
        EmailAddress= request.form['EmailAddress']#area
        CountryFull= request.form['CountryFull']
        TelephoneNumber= request.form['TelephoneNumber']
        Birthday= request.form['Birthday']
        Age= request.form['Age']
        Occupation= request.form['Occupation']
        Company= request.form['Company']
        Vehicle= request.form['CompanyVehicle']
        BloodType= request.form['BloodType']
        Kilograms= request.form['Kilograms']
        FeetInches= request.form['FeetInches']
        CrimeType= request.form['CrimeType']
        Area = request.form['Area']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if not re.match(r'[^@]+@[^@]+\.[^@]+', EmailAddress):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z]+', GivenName,Surname,NameSet,City):
            msg = 'NameSet,Username,Surname,City must contain only characters !'
        elif not re.match(r'[0-9]+',TelephoneNumber):
            msg = 'TelephoneNumber must contain only number !'
        elif not re.match(r'[0-9]+',Age):
            msg = 'Age must contain only number !'
        else:
            cursor.execute('INSERT INTO criminal VALUES (NULL,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (Gender,NameSet,GivenName,Surname,StreetAddress,City,StateFull,ZipCode,CountryFull,EmailAddress,TelephoneNumber,Birthday,Age,Occupation,Company,Vehicle,BloodType,Kilograms,FeetInches,CrimeType,Area,))
            mysql.connection.commit()
            msg = 'Criminal added successfully !!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
       
    return render_template('addCriminal.html', msg=msg)

if __name__ == '__main__':
    app.run(host = 'localhost', debug = True, port = '5000')
