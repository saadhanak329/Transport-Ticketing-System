import os
import sys
import json
import pymysql as sql # to import sql

try:
    f = open("employeeids.json","r")  #Accessing the emplopyeeids.json file and givimg permision for reading only
    Employee_IDs = json.load(f)  #loading the json file f
    f.close()  #closing the json file
except Exception as e:  #If unable to open the file and throws the exception then print the giiven statement
    print("Unable to Open employeeids.json. Exception: ",e)
print("\n\n-------- Welcome to Transport Ticketing System! --------\n")  #If the file succefully opens then printing this statement

# SQL Parameters
sqlsrvr = "localhost"  #connecting to sql local server
sqluser = "root"  # making the user as the admin 
sqlpwd = "toor"  # admin password is "toor"
sqldb = "ttsdb"  # SQL DataBase name is given as "ttsdb"

db = sql.connect(sqlsrvr,sqluser,sqlpwd,sqldb)  # connecting to the SQL server
cursor = db.cursor()  # cursor enables for any addition or traversal or any other modifications in database
cursor.execute("SELECT * FROM ttsdb.ula")  # To retreive all the data from tts.ula database
data = cursor.fetchall()  # cursor is used to consistently fetch data from the SQL database
print(data[1])  # Retreibing the first row data
db.close()  # closing the database
  # Employee login 
def login(eid, pwd):  # defining a function called login with arguments emplyee id and password
    rvalue = True
    if len(eid)!=4:  # checking if the given employee id is of 4 digits are not
        print("Enter Valid Employee ID : \t")  # if the employee id is not of 4 didgit then printing this message
    else:
        if eid in Employee_IDs:  # If the entered eid is of 4 digits and the eid is present in Employee_IDs(employeeids.json) 
            if Employee_IDs[eid]!=pwd:  # if the entered password is incorrect then the login is failed
                print("Login Failure: Password Incorrect")
                rvalue = "PWD"
            else:
                print("Login Successful")  # if the password is correct then the login is successful
                rvalue = "True"
        else:
            rvalue = "EID"  # to return the employee ID
    return rvalue

def register(eid):  # defining a function called register with employee ID,only for change of password 
    print("--- Registration ---")
    pwd = input("Enter New Password :\t")  # inputing the new password 
    cpwd = input("Enter Password again :\t")
    if pwd!=cpwd:  # checking if the both the entred passowrds are matching 
        print("Passwords not matching. Try again\n")
        register(eid)  # function is called again until the password matches
    else:
        Employee_IDs[eid] = pwd  # assinging the new employee with the new password
        with open('employeeids.json','a+') as e:
            json.dump(Employee_IDs,e)  # updating the employee database with the new password of a particular employee
        print("Password Change Successfull\n")

eid = input("Enter Employee ID : \t")
while(len(eid)!=4):  # checking if the given employee id is of 4 digits are not
    eid = input("Enter Valid Employee ID :\t")  # loop repeates until the correct employee ID is entered
pwd = input("Enter Password : \t")
rvalue = login(eid,pwd)  # login function is called and login process is repeated
if rvalue == "PWD":
    ch = input("\n\n1.Change Password\n2.Exit\n\nEnter your choice :\t")
    if ch=="1":
        register(eid)
elif rvalue == "EID":
    ch = input("\n\n1.Register Employee ID\n2.Exit\n\nEnter your choice :\t")
    if ch=="1":
        register(eid)