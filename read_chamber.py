#!/usr/bin/env python
#When this program is executed, it receives the values of the 
# temperature and humidity from the chamber and save it in to the database

import serial

import sqlite3

import os
import time
import glob


#Global Variables

ser = 0
serialString = " test string"
temperature = ""
humidity = ""

# chamber temperature stored in the database
dbname='/var/www/new_test.db'

#Function to Initialize the Serial Port
def init_serial():
   
    global ser          #Must be declared in Each Function
    ser = serial.Serial()
    ser.baudrate = 9600
    ser.parity = serial.PARITY_NONE
    ser.stopbits = serial.STOPBITS_ONE
    ser.bytesize = serial.EIGHTBITS
    
    
    #assign to the folder of the opening port
    ser.port = '/dev/ttyUSB1' 

    #Specify theTimeOut in seconds, so that SerialPort
    #Doesn't hangs
    ser.timeout = 0.1 
    ser.open()          #Opens SerialPort

 
#Call the Serial Initilization Function, Main Program Starts from here
init_serial()

def spliter(a):
   
    if(a[2] == "A"):
	x = a.split(' ')
	temperature = a[3:10]
	humidity = a[18:23]
	print "temperature = " + temperature, "humidity = " + humidity	

	chamber_log_temperature(temperature, humidity)



def chamber_log_temperature(mytemp, humid):

    conn=sqlite3.connect(dbname)
    curs=conn.cursor()

    curs.execute("INSERT INTO mytemps values(datetime('now'), (?), (?))", (mytemp,humid))

    # commit the changes
    conn.commit()

    conn.close()

def display_rpi_data():

    conn=sqlite3.connect(dbname)
    curs=conn.cursor()

    for row in curs.execute("SELECT * FROM mytemps"):
        print str(row[0])+" "+ str(row[1]) + " " + str(row[2])
   
    conn.close()

while True:
		bytes = ser.readline()			
		serialString = bytes.decode("utf-8")
		#print serialString		
		#print bytes		
		#display_rpi_data()
		spliter(bytes)
	
		
