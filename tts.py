import os
import sys
import json
import pymysql as sql

try:
    f = open("employeeids.json","r")
    Employee_IDs = json.load(f)
    f.close()
except Exception as e:
    print("Unable to Open employeeids.json. Exception: ",e)
print("\n\n-------- Welcome to Transport Ticketing System! --------\n")

# SQL Parameters
sqlsrvr = "localhost"
sqluser = "root"
sqlpwd = "toor"
sqldb = "ttsdb"

db = sql.connect(sqlsrvr,sqluser,sqlpwd,sqldb)
cursor = db.cursor()
cursor.execute("SELECT * FROM ttsdb.ula WHERE ")
data = cursor.fetchall()
print(data[1])
db.close()

def login(eid, pwd):
    rvalue = True
    if len(eid)!=4:
        print("Enter Valid Employee ID : \t")
    else:
        if eid in Employee_IDs:
            if Employee_IDs[eid]!=pwd:
                print("Login Failure: Password Incorrect")
                rvalue = "PWD"
            else:
                print("Login Successful")
                rvalue = "True"
        else:
            rvalue = "EID"
    return rvalue

def register(eid):
    print("--- Registration ---")
    pwd = input("Enter New Password :\t")
    cpwd = input("Enter Password again :\t")
    if pwd!=cpwd:
        print("Passwords not matching. Try again\n")
        register(eid)
    else:
        Employee_IDs[eid] = pwd
        with open('employeeids.json','a+') as e:
            json.dump(Employee_IDs,e)
        print("Password Change Successfull\n")

eid = input("Enter Employee ID : \t")
while(len(eid)!=4):
    eid = input("Enter Valid Employee ID :\t")
pwd = input("Enter Password : \t")
rvalue = login(eid,pwd)
if rvalue == "PWD":
    ch = input("\n\n1.Change Password\n2.Exit\n\nEnter your choice :\t")
    if ch=="1":
        register(eid)
elif rvalue == "EID":
    ch = input("\n\n1.Register Employee ID\n2.Exit\n\nEnter your choice :\t")
    if ch=="1":
        register(eid)