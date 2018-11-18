import os
import sys
import json
import time
import pymysql as sql
import geocoder
import subprocess
# from detect_barcode import VideoStream
from math import sin, cos, sqrt, atan2, radians

# Employee login
def login(cursor):#login setup for employee
    print("\n--- Employee Login ---\n")
    eid = input("\nEnter Employee ID :\t")
    while(len(eid)!=4):
        eid = input("Enter Valid Employee ID :\t")
    
    cursor.execute("SELECT eid FROM ttsdb.ula")
    li = []
    db_eid_list = []
    li = cursor.fetchall()
    for i in li:
        db_eid_list.append(i[0])
    if int(eid) in db_eid_list:
        pwd = input("Enter Password :\t")
        sqlquery = "SELECT password FROM ttsdb.ula where eid="+str(eid)
        cursor.execute(sqlquery)
        dbpwd = cursor.fetchone()
        if pwd == dbpwd[0]:
            print("Login Successful\n")
            routesetup(cursor)
    else:
        reg = input("Employee ID has not been registered before. Would you like register now? (y/n)\t")
        if reg.lower() in ['y','yes']:
            register(cursor)
    
# Registration and change of password
def register(cursor):
    print("\n--- Registration ---\n")
    eid = input("Enter Employee ID :\t")
    pwd = input("Enter New Password :\t")
    cpwd = input("Enter Password again :\t")
    if pwd!=cpwd:
        print("Passwords not matching. Try again\n")
        register(eid)
    else:
        sqlquery = "INSERT INTO ttsdb.ula(eid,password) VALUES("+eid+",\""+pwd+"\")"
        cursor.execute(sqlquery)
        sqlquery = "SELECT password FROM ttsdb.ula where eid="+str(eid)
        cursor.execute(sqlquery)
        dbpwd = cursor.fetchone()
        if pwd == dbpwd[0]:
            print("\nRegistration Successful.\n\nYou will be redirected to login now...\n")
            time.sleep(1)
            login(cursor)
        else:
            ch = ("\nRegistration Unsuccessful. Try Again? (y/n)")
            if ch.lower() in ['y','yes']:
                register(cursor)

# Calculating Distance in Kms between 2 Lat,Long Pairs
def distcalc(la1,lo1,la2,lo2):
    R=6373.0
    dlo = radians(lo2) - radians(lo1)
    dla = radians(la2) - radians(la1)
    a = sin(dla / 2)**2 + cos(la1) * cos(la2) * sin(dlo / 2)**2
    b = 2 * atan2(sqrt(a), sqrt(1 - a))
    res = R * b
    return res

# Setting Up Route
def routesetup(cursor):
    print("\n--- Route Setup ---\n")
    routeid = input("Enter Route ID:\t")
    sqlquery = "SELECT routeid FROM ttsdb.routes"
    li = []
    db_routeid_list = []
    cursor.execute(sqlquery)
    li = cursor.fetchall()
    for i in li:
        db_routeid_list.append(i[0])
    print(db_routeid_list)
    if routeid in db_routeid_list:
        print("\nRoute Successfully initialized\n")
        transact(cursor)
    else:
        print("Invalid Route ID")
        routesetup(cursor)

def transact(cursor):
    while True:
        print("\n\n-------- Welcome to Transport Ticketing System! --------\n")
        print("Please scan your BMTC Card by placing it infront of the Camera to continue\n")
        subprocess.check_output("python detect_barcode.py", shell=True).decode()
        
if __name__ == "__main__":
    print("\n\n-------- Welcome to Transport Ticketing System! --------\n")
    g = geocoder.ip('me')
    print(g.lat)

    choice = input("\n1. Login\n2. Registration\n3. Exit\n\n")
    # SQL Parameters
    sqlsrvr = "localhost"
    sqluser = "root"
    sqlpwd = "toor"
    sqldb = "ttsdb"
    
    # Connecting to MySQL DataBase and initializing a cursor to fetch data
    db = sql.connect(sqlsrvr,sqluser,sqlpwd,sqldb)
    cursor = db.cursor()
    if choice=="1":
        login(cursor)
    elif choice=="2":
        register(cursor)
    elif choice=="3":
        exit()
    else:
        print("Enter a Valid Choice\n")
    db.close()