from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import hashlib
from selenium import webdriver 
# from cryptography.fernet import Fernet
from time import sleep 
import plotly.express as px
from matplotlib import pyplot as plt 

app = Flask(__name__)

app.secret_key = 'your secret key'

# app.config['MYSQL_HOST'] = 'ibm-project.cnr3cxrsxzux.us-east-1.rds.amazonaws.com'
# app.config['MYSQL_USER'] = 'admin'
# app.config['MYSQL_PASSWORD'] = 'oyTAry1t9ZWsMf9wbNrk'
# app.config['MYSQL_DB'] = 'pythonlogin'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'mypass@2002'
app.config['MYSQL_DB'] = 'pythonlogin'


mysql = MySQL(app)
def write_key():                                #creating a key
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

def load_key():                                 #reading the generated key
    return open("secret.key", "rb").read()
   
@app.route('/pythonlogin/', methods=['GET', 'POST'])
def login():
    
    msg = ''
    
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
  
        username = request.form['username']
        password = request.form['password']   
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # key = load_key() 
        # cipher_suite = Fernet(key)
        # username=bytes(username,'utf-8') 
        # cipherUsername = cipher_suite.encrypt(username)   
        # print(cipherUsername)     
        hashpass=hashlib.sha256(password.encode('utf-8')).hexdigest()
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, hashpass,))
       
        account = cursor.fetchone()
        if account:
           
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
           
            return redirect(url_for('home'))
        else:
            msg = 'Incorrect username/password!'
  
    return render_template('index.html', msg=msg)


@app.route('/pythonlogin/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)

   return redirect(url_for('login'))

   
@app.route('/pythonlogin/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
       
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
                # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s and email = %s', (username,email,))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # write_key()                                     #creating the key
            # key = load_key() 
            # cipher_suite = Fernet(key)
            # username=bytes(username,'utf-8') 
            # cipherUsername = cipher_suite.encrypt(username)
            # print(cipherUsername)
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            hashpass=hashlib.sha256(password.encode('utf-8')).hexdigest()
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username,hashpass , email,))
            mysql.connection.commit()
            msg = 'You have successfully registered! Do Login...'
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('register.html', msg=msg)


@app.route('/pythonlogin/home')
def home():
    
    if 'loggedin' in session:
       
        return render_template('home.html', username=session['username'])
   
    return redirect(url_for('login'))

@app.route('/pythonlogin/profile')
def profile():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
    
        return render_template('profile.html', account=account)
    
    return redirect(url_for('login'))


@app.route('/pythonlogin/search', methods=['GET', 'POST'])
def search():
    if 'loggedin' in session:
        if request.method == "POST":
            username = request.form['username']
            cursor = mysql.connection.cursor()
            heading=["Criminal id","UserName","Contect Number"]
            if request.form.get('name'):
                heading.append("LastName")
                cursor.execute("SELECT cid ,GivenName,TelephoneNumber,Surname FROM pythonlogin.criminal where GivenName LIKE %s ", (username+"%",))
                #cursor.execute("SELECT cid ,firstname,lastname,phone FROM pythonlogin.criminal_details where firstname LIKE %s ", (username+"%",))
                data = cursor.fetchall()
            if request.form.get('area'):
                # heading.append("City")
                # cursor.execute("SELECT cid ,firstname,phone,city FROM pythonlogin.criminal_details where city LIKE %s ", (username+"%",))
                heading.append("Area")
                cursor.execute("SELECT cid ,GivenName,TelephoneNumber,area FROM criminal where area LIKE %s ", (username+"%",))
                data = cursor.fetchall()
           
            if request.form.get('crime'):
                heading.append("CrimeType")
                #cursor.execute("SELECT cid ,firstname,phone,CrimeType FROM pythonlogin.criminal_details where CrimeType LIKE %s ", (username+"%",))
                cursor.execute("SELECT cid ,GivenName,TelephoneNumber,CrimeType FROM pythonlogin.criminal where CrimeType LIKE %s ", (username+"%",))
                data = cursor.fetchall()
            
            if username == 'all':
                heading.append("city")
                heading.append("CrimeType") 
                #cursor.execute("SELECT cid ,firstname,phone,lastname,city,CrimeType FROM pythonlogin.criminal_details")
                cursor.execute("SELECT cid ,GivenName,TelephoneNumber,Surname,City,CrimeType FROM pythonlogin.criminal")
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
            #cur.execute("select cid,firstname,lastname,address,city,state,country,pincode,ssn_number,countrycode,phone,dob,age,company,occupation,height,weight,bloodtype,fav_color,vehicle,CrimeType FROM criminal_details WHERE cid=%s", (id_data,))
            cur.execute("SELECT cid,Gender,NameSet,GivenName,Surname,StreetAddress,City,StateFull,ZipCode,CountryFull,EmailAddress,TelephoneNumber,Birthday,Age,Occupation,Company,Vehicle,BloodType,Kilograms,FeetInches,CrimeType,Area FROM criminal WHERE cid=%s", (id_data,))
            detail = cur.fetchall()
            detail
            #print(detail)
            #headings=("Criminal id","First Name","Last Name","Address","City","State","Country","Pincode","SSN NO.","Country Code","Phone","DOB","Age","Company","Occupation","Height","Weight","Blood_Type","Favorite Color" )
            headings=("Criminal id","Gender","NameSet","First Name","Surname","Street Address","City","StateFull","ZipCode","CountryFull","EmailAddress","TelephoneNumber","Birthday","Age","Occupation","Company","Vehicle","BloodType","Kilograms","FeetInches","CrimeType","Area")
            return render_template('details.html',headings=headings,detail=detail)
        
    return redirect(url_for('login'))

@app.route('/pythonlogin/addCriminal', methods=['GET','POST'])
def addCriminal():
    if 'loggedin' in session:
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
            counter = 0
            for c in TelephoneNumber:
                counter+=1   
            if not re.match(r'[A-Za-z]+', Gender):
                msg = 'Gender must contain only number !'
            # if not re.match(r'[^@]+@[^@]+\.[^@]+', EmailAddress):
            #     msg = 'Invalid email address!'
            # elif not re.match(r'[A-Za-z]+', GivenName):
            #     msg = 'NameSet,Username,Surname,City must contain only characters !'
            # elif not re.match(r'[0-9]+',TelephoneNumber):
            #     msg = 'TelephoneNumber must contain only number !'
            # elif not re.match(r'[0-9]+',Age):
            #     msg = 'Age must contain only number !'
            # elif counter != 10:
            #     msg = 'TelephoneNumber must contain only 10 number !'
            
            else:
                cursor.execute('INSERT INTO criminal VALUES (NULL,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (Gender,NameSet,GivenName,Surname,StreetAddress,City,StateFull,ZipCode,CountryFull,EmailAddress,TelephoneNumber,Birthday,Age,Occupation,Company,Vehicle,BloodType,Kilograms,FeetInches,CrimeType,Area,))
                mysql.connection.commit()
                msg = 'Criminal added successfully !!'
        elif request.method == 'POST':
            # Form is empty... (no POST data)
            msg = 'Please fill out the form!'
       
    return render_template('addCriminal.html',msg=msg)

@app.route('/pythonlogin/googlemap', methods=['GET','POST'])
def googlemap():
    msg = ''
    data=[]
    if 'loggedin' in session:
        if request.method == 'POST':
            # Create variables for easy access
            startPoint = request.form['startPoint']
            endPoint = request.form['endPoint']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            driver = webdriver.Chrome()
            driver.get("https://www.google.co.in/maps/@10.8091781,78.2885026,7z") 
            sleep(2) 
            def searchplace():
                Place=driver.find_element_by_class_name("tactile-searchbox-input")
                Place.send_keys(startPoint)
                Submit=driver.find_element_by_xpath("/html/body/div[3]/div[9]/div[3]/div[1]/div[1]/div[1]/div[2]/div[1]/button")
                Submit.click()
                print(startPoint)
            searchplace()
            def directions():
                sleep(10)
                directions=driver.find_element_by_xpath("/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[4]/div[1]/button")
                #directions=driver.find_element_by_xpath("/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[4]/div[1]/button")
                directions.click()
            directions()
            def find():
                sleep(6)
                find=driver.find_element_by_xpath("/html/body/div[3]/div[9]/div[3]/div[1]/div[2]/div/div[3]/div[1]/div[1]/div[2]/div[1]/div/input")
                #find=driver.find_element_by_xpath("/html/body/div[3]/div[9]/div[3]/div[1]/div[2]/div/div[3]/div[1]/div[1]/div[2]/div[1]/div/input")
                find.send_keys(endPoint)
                sleep(2)
                
                #search=driver.find_element_by_xpath("/html/body/div[3]/div[9]/div[3]/div[1]/div[2]/div/div[3]/div[1]/div[1]/div[2]/button[1]")
                search.click()

            find()
            def kilometers():
                sleep(2)
                Totalkilometers=driver.find_element_by_xpath("/html/body/div[3]/div[9]/div[3]/div[1]/div[2]/div/div[2]/div/div/div/div[2]/button/div[1]")
                #/html/body/div[3]/div[9]/div[3]/div[1]/div[2]/div/div[2]/div/div/div/div[2]/button/div[1]")
                #/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[4]/div[1]/div[1]/div[1]/div[1]/div[2]/div")
                print("Total Hours:",Totalkilometers.text)
                data.append(Totalkilometers.text)
                
            kilometers()
        
            
        elif request.method == 'POST':
            # Form is empty... (no POST data)
            msg = 'Please fill out the form!'

    return render_template('googlemap.html',data=data,msg=msg)
    
@app.route('/pythonlogin/plot', methods=['GET','POST'])
def plot():
    if 'loggedin' in session:
            cur =mysql.connection.cursor()
            #cur.execute("select cid,firstname,lastname,address,city,state,country,pincode,ssn_number,countrycode,phone,dob,age,company,occupation,height,weight,bloodtype,fav_color,vehicle,CrimeType FROM criminal_details WHERE cid=%s", (id_data,))
            cur.execute("SELECT CrimeCounts,CrimeType,City FROM criminal")
            data_ = cur.fetchall() 
            x = [] 
            City=[]
            y = [] 
            for i in data_: 
                 x.append(i[0])	#x column contain data(1,2,3,4,5) 
                 y.append(i[1])
                 City.append(i[2])
            # plt.plot(x,y)  x = 'City', y = 'CrimeType' ,color="StateFull",title='cirminal crimeType Details')
            # plt.show() 
            fig = px.bar(data_, x , y ,title='Criminal crimeType Analysis',color=City)
            fig.show()
            return render_template('home.html')
         
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(host = 'localhost', debug = True, port = '5000')
    