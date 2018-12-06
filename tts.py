import os
import sys
import json
import time
import pymysql as sql
import geocoder
import subprocess
# from detect_barcode import VideoStream
from math import sin, cos, sqrt, atan2, radians, floor

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
            time.sleep(1)
            print("\n>> Login Successful\n")
            routesetup(cursor)
        else:
            time.sleep(1)
            print("\n>> Password Incorrect\n")
            login(cursor)
    else:
        time.sleep(1)
        reg = input("\n>> Employee ID has not been registered before. Would you like register now? (y/n)\t")
        if reg.lower() in ['y','yes']:
            register(cursor)
    
# Registration and change of password
def register(cursor):
    print("\n--- Registration ---\n")
    eid = input("Enter Employee ID :\t")
    pwd = input("Enter New Password :\t")
    cpwd = input("Enter Password again :\t")
    if pwd!=cpwd:
        print(">> Passwords not matching. Try again\n")
        time.sleep(1)
        register(eid)
    else:
        sqlquery = "INSERT INTO ttsdb.ula(eid,password) VALUES("+eid+",\""+pwd+"\")"
        cursor.execute(sqlquery)
        sqlquery = "SELECT password FROM ttsdb.ula where eid="+str(eid)
        cursor.execute(sqlquery)
        dbpwd = cursor.fetchone()
        if pwd == dbpwd[0]:
            time.sleep(1)
            print("\n>> Registration Successful.\n\n>> You will be redirected to login now...\n")
            login(cursor)
        else:
            time.sleep(1)
            ch = ("\n>> Registration Unsuccessful. Try Again? (y/n)")
            if ch.lower() in ['y','yes']:
                register(cursor)

# Calculating Distance in Kms between 2 Lat,Long Pairs
def distcalc(la1,lo1,la2,lo2):
    R=6.371
    la1 = 12.9249 #Banashankari Coords
    lo1 = 12.9260
    la2 = 77.5662
    lo2 = 77.6762 #Bellandur Coords
    dlon = radians(lo2-lo1)
    dlat = radians(la2-la1)
    a = sin(dlat/2)*sin(dlat/2) + cos(radians(la1))*cos(radians(la2))*sin(dlon/2)*sin(dlon/2)
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    res = floor(R * c)
    print("\nDistance Travelled:\t",res,"\n")
    return res

def ratecalc(dist):
    if dist<2:
        return 10
    elif dist<10:
        return dist*4
    else:
        return dist*3

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
    if routeid in db_routeid_list:
        time.sleep(1)
        print("\n>> Route Successfully initialized\n")
        transact(cursor)
    else:
        print("Invalid Route ID")
        routesetup(cursor)

def transact(cursor):
    while True:
        print("\n\n\n-------- Welcome to Transport Ticketing System! --------\n")
        print("Please scan your BMTC Card by placing it infront of the Camera to continue\n")
        # accountno = subprocess.check_output("python detect_barcode.py --video video/coupon.mov", shell=True).decode()
        # print(accountno)
        accountno = input("Enter Account Number Manually:\t")
        sqlquery = "SELECT * FROM ttsdb.customer WHERE accountno="+accountno
        li = []
        cust_details = []
        flag = 0
        cursor.execute(sqlquery)
        li = cursor.fetchall()
        if li: 
            for i in li[0]:
                cust_details.append(i)
            if cust_details[2]==0:
                sqlquery = "UPDATE ttsdb.customer SET flag=1 WHERE accountno="+str(cust_details[0])
                cursor.execute(sqlquery)
                g = geocoder.ip('me')
                sqlquery = "UPDATE ttsdb.customer SET latitude="+str(g.lat)+",longitude="+str(g.lat)+" WHERE accountno="+str(cust_details[0])
                try:
                    cursor.execute(sqlquery)
                except Exception:
                    pass
                print("\n>> Scan Successful. Happy Journey!\n")
                print("\n\n------ Travelling ----\n\n")
                time.sleep(2)
                transact(cursor)
            elif cust_details[2]==1:
                g = geocoder.ip('me')
                distance_travelled = distcalc(cust_details[4],cust_details[5],float(12.9249),float(77.5662))
                cost = ratecalc(distance_travelled)
                if float(cost)<=float(cust_details[3]):
                    sqlquery = "UPDATE ttsdb.customer SET amount="+str(float(cust_details[3])-float(cost))+" WHERE accountno="+str(cust_details[0])
                    time.sleep(2)
                    print(">> Amount of "+str(cost)+" has been deducted. Thank You for travelling with us!")
                else:
                    sqlquery = "UPDATE ttsdb.customer SET amount="+str(cust_details[3])+" WHERE accountno="+str(cust_details[0])
                    time.sleep(2)
                    print(">> Your Account has insufficient funds. Rs."+cust_details[3]+" has been deducted. Please pay the remaining amount to the conductor. Thank You for travelling with us.")
    return 0
        
if __name__ == "__main__":
    print("\n\n-------- Welcome to Transport Ticketing System! --------\n")

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