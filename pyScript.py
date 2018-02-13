#!/usr/bin/env python

# Author: Daniel-Florin Dosaru dosarudaniel@gmail.com

import getpass, sys, telnetlib

apc_addr = ["192.168.254.201", "192.168.254.202", "192.168.254.203"]
# user = raw_input("UserName: ")
# password = getpass.getpass()
user = "apc"
password = "apc"


# This function applies an action to a specific Outlet of a specific APC
# apc_no tells which APC to configure
# outlet_no tells wich outlet to control
# Possible actions:
# 1- Immediate On              
# 2- Immediate Off             
# 3- Immediate Reboot          
# 4- Delayed On                
# 5- Delayed Off               
# 6- Delayed Reboot 
# 7- Cancel
def applyActionToOutlet(outlet_no, action, apc_no):
	if outlet_no > 8 or outlet_no < 1:
		print 'Invalid Outlet number, try an integer: [1-8]'
		return
	if action > 7 or action < 1:
		print 'Invalid action, try an integer: [1-7]'
		return
	if apc_no > 2 or apc_no < 0:
		print 'Invalid apc_no, try an integer: [0-2]'
		return

	tn = telnetlib.Telnet(apc_addr[apc_no])
	tn.read_until("User Name : ")
	tn.write(user + "\r")
	if password:
		tn.read_until("Password  : ")
		tn.write(password + "\n")
	tn.write("\r")
	tn.write("1\r3\r"+str(outlet_no)+"\r1\r" + str(action) + "\rYES\r\n\r") 
	tn.write("\033\r\033\r\033\r\033\r4\r") # close telnet connection
	tn.read_until(".")
# Example: applyActionToPort(3, 1, 1) # Turn Immediate ON the 3rd Outlet of apc[1]



# This function applies an action to all outlets of a specific apc_no
# apc_no tells which APC to configure
# Possible actions:
# 1- Immediate On              
# 2- Immediate Off             
# 3- Immediate Reboot          
# 4- Delayed On                
# 5- Delayed Off               
# 6- Delayed Reboot 
# 7- Cancel
def applyActionToAllOutlets(action, apc_no):
	if action > 7 or action < 1:
		print 'Invalid action, try an integer: [1-7]'
		return
	if apc_no > 2 or apc_no < 0:
		print 'Invalid apc_no, try an integer: [0-2]'
		return

	tn = telnetlib.Telnet(apc_addr[apc_no])
	tn.read_until("User Name : ")
	tn.write(user + "\r")
	if password:
		tn.read_until("Password  : ")
		tn.write(password + "\n")
	tn.write("\r")
	tn.write("1\r3\r9\r1\r" + action + "\rYES\r\n\r") 
	tn.write("\033\r\033\r\033\r\033\r4\r") # close telnet connection
	tn.read_until(".")
# Example applyActionToAllOutlets(2, 1) # Turn Immediate OFF all Outlets of apc[1]



# This function returns an array that represent the state of the outlets
# status[i] == 0 => Outlet nr i is OFF
# status[i] == 1 => Outlet nr i is ON
# apc_no tells which APC to configure
def checkStatus(apc_no):
	if apc_no > 2 or apc_no < 0:
		print 'Invalid apc_no, try an integer: [0-2]'
		return
	status = [0,0,0,0,0,0,0,0]
	tn = telnetlib.Telnet(apc_addr[apc_no])
	tn.read_until("User Name : ")
	tn.write(user + "\r")
	if password:
		tn.read_until("Password  : ")
		tn.write(password + "\n")
	tn.write("\r")
	tn.write("1\r3\r")
	tn.write("\033\r\033\r4\r") # close telnet connection
	s = tn.read_until("Master ")
	s = s[1193:1497]
	a = s.split('\n')
	
	for i in range(0, 8):
		if a[i][34] == 'N':
			status[i] = 1
	return status
# Example: 
# status = []
# status = checkStatus(1) #from apc[1]
# print status

# applyActionToOutlet(int(sys.argv[1]), int(sys.argv[2]), 1)