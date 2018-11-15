import os
import sys
import json
import time
import pymysql as sql

# Employee login
def login(cursor):
    rvalue = True
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
    else:
        reg = input("Employee ID has not been registered before. Would you like register now? (y/n)\t")
        if reg.lower() in ['y','yes']:
            register(cursor)
    return rvalue

# Registration
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