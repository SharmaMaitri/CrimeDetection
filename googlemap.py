from selenium import webdriver 
from time import sleep 

driver = webdriver.Chrome()
driver.get("https://www.google.co.in/maps/@10.8091781,78.2885026,7z") 


sleep(2) 

def searchplace():
            Place=driver.find_element_by_class_name("tactile-searchbox-input")
            Place.send_keys("surat")
            Submit=driver.find_element_by_xpath("/html/body/div[3]/div[9]/div[3]/div[1]/div[1]/div[1]/div[2]/div[1]/button")
            Submit.click()
searchplace()
def directions():
            sleep(10)
            directions=driver.find_element_by_xpath("/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[4]/div[1]/button")
            directions.click()

directions()
def find():
         sleep(6)
         find=driver.find_element_by_xpath("/html/body/div[3]/div[9]/div[3]/div[1]/div[2]/div/div[3]/div[1]/div[1]/div[2]/div[1]/div/input")
         find.send_keys("ahmedabad")
         sleep(2)
         search=driver.find_element_by_xpath("/html/body/div[3]/div[9]/div[3]/div[1]/div[2]/div/div[3]/div[1]/div[1]/div[2]/button[1]")
         search.click()
find()

def kilometers():
               sleep(5)
               Totalkilometers=driver.find_element_by_xpath("/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[4]/div[2]/div[1]/div[1]/div[1]/div[2]/div")
               #"/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[4]/div[1]/div[1]/div[1]/div[1]/div[2]/div")
               print("Total Kilometers:",Totalkilometers.text)
               sleep(5)
               Bus=driver.find_element_by_xpath("/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[4]/div[1]/div[1]/div[1]/div[1]/div[1]/span[1]")
               print("Bus Travel:",Bus.text)
               sleep(7)
               Train=driver.find_element_by_xpath("/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[4]/div[3]/div[1]/div[2]/div[1]/div")
               print("Train Travel:",Train.text)
               sleep(7)

kilometers()
'''

app.config['MYSQL_HOST'] = 'ibm-project.cnr3cxrsxzux.us-east-1.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = 'oyTAry1t9ZWsMf9wbNrk'
app.config['MYSQL_DB'] = 'pythonlogin'''
'''
@app.route('/pythonlogin/googlemap', methods=['GET','POST'])
def googlemap():
    if 'loggedin' in session:
        msg = ''
        data=[]
        if request.method == 'POST':
            # Create variables for easy access
            startPoint = request.form['startPoint']
            endPoint = request.form['endPoint']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            if not re.match(r'[0-9]*[A-Za-z]+[0-9]*', startPoint,endPoint):
                msg = 'enter valid StartPoint,end point!'
            def searchplace():
                Place=driver.find_element_by_class_name("tactile-searchbox-input")
                Place.send_keys(startPoint)
                Submit=driver.find_element_by_xpath("/html/body/div[3]/div[9]/div[3]/div[1]/div[1]/div[1]/div[2]/div[1]/button")
                Submit.click()
            searchplace()
            def directions():
                sleep(5)
                directions=driver.find_element_by_xpath("/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[4]/div[1]/button")
                directions.click()
            directions()
            def find():
                sleep(6)
                find=driver.find_element_by_xpath("/html/body/div[3]/div[9]/div[3]/div[1]/div[2]/div/div[3]/div[1]/div[1]/div[2]/div[1]/div/input")
                find.send_keys(endPoint)
                sleep(2)
                search=driver.find_element_by_xpath("/html/body/div[3]/div[9]/div[3]/div[1]/div[2]/div/div[3]/div[1]/div[1]/div[2]/button[1]")
                search.click()
            find()
            def kilometers():
                sleep(2)
                Totalkilometers=driver.find_element_by_xpath("/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[4]/div[1]/div[1]/div[1]/div[1]/div[2]/div")
                print("Total Kilometers:",Totalkilometers.text)
                data.append(Totalkilometers)
                sleep(2)
                Bus=driver.find_element_by_xpath("/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[4]/div[1]/div[1]/div[1]/div[1]/div[1]/span[1]")
                print("Bus Travel:",Bus.text)
                data.append(Bus)
                sleep(2)
            #    Train=driver.find_element_by_xpath("/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[4]/div[3]/div[1]/div[2]/div[1]/div")
            #    print("Train Travel:",Train.text)
            #    sleep(2)
            kilometers()
            
        elif request.method == 'POST':
            # Form is empty... (no POST data)
            msg = 'Please fill out the form!'

    return render_template('profile.html', msg=msg)
    '''