#!/usr/bin/env python3

# Authors: Andrei Raduta, Dosaru Daniel-Florin
# E-mail: andrei.raduta11@gmail.com ; dosarudaniel@gmail.com
# Script usage: python3 webserver.py [port-number] (default port = 5000)

from flask import Flask, render_template, request
import pandas, numpy, sys, telnetlib

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
		print('Invalid Outlet number, try an integer: [1-8]')
		return
	if action > 7 or action < 1:
		print ('Invalid action, try an integer: [1-7]')
		return
	if apc_no > 2 or apc_no < 0:
		print ('Invalid apc_no, try an integer: [0-2]')
		return

	tn = telnetlib.Telnet(apc_addr[apc_no])
	tn.read_until(("User Name : ").encode('ascii'))
	tn.write((user + '\r').encode('ascii'))
	if password:
		tn.read_until(("Password  : ").encode('ascii'))
		tn.write((password + "\n").encode('ascii'))
	tn.write(("\r").encode('ascii'))
	tn.write(("1\r3\r"+str(outlet_no)+"\r1\r" + str(action) + "\rYES\r\n\r").encode('ascii')) 
	tn.write(("\033\r\033\r\033\r\033\r4\r").encode('ascii')) # close telnet connection
	tn.read_until((".").encode('ascii'))
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
		print('Invalid action, try an integer: [1-7]')
		return
	if apc_no > 2 or apc_no < 0:
		print('Invalid apc_no, try an integer: [0-2]')
		return

	tn = telnetlib.Telnet(apc_addr[apc_no])
	tn.read_until(("User Name : ").encode('ascii'))
	tn.write((user + "\r").encode('ascii'))
	if password:
		tn.read_until(("Password  : ").encode('ascii'))
		tn.write((password + "\n").encode('ascii'))
	tn.write(("\r").encode('ascii'))
	tn.write(("1\r3\r9\r1\r" + str(action) + "\rYES\r\n\r").encode('ascii')) 
	tn.write(("\033\r\033\r\033\r\033\r4\r").encode('ascii')) # close telnet connection
	tn.read_until((".").encode('ascii'))
# Example applyActionToAllOutlets(2, 1) # Turn Immediate OFF all Outlets of apc[1]



# This function returns an array that represent the state of the outlets
# status[i] == 0 => Outlet nr i is OFF
# status[i] == 1 => Outlet nr i is ON
# apc_no tells which APC to configure
def checkStatus(apc_no):
	if apc_no > 2 or apc_no < 0:
		print('Invalid apc_no, try an integer: [0-2]')
		return
	status = [0,0,0,0,0,0,0,0]
	tn = telnetlib.Telnet(apc_addr[apc_no])
	tn.read_until(("User Name : ").encode('ascii'))
	tn.write((user + "\r").encode('ascii'))
	if password:
		tn.read_until(("Password  : ").encode('ascii'))
		tn.write((password + "\n").encode('ascii'))
	tn.write(("\r").encode('ascii'))
	tn.write(("1\r3\r").encode('ascii'))
	tn.write(("\033\r\033\r4\r").encode('ascii')) # close telnet connection
	s = tn.read_until(("Master ").encode('ascii'))
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

#applyActionToOutlet(int(sys.argv[1]), int(sys.argv[2]), 1)



app = Flask(__name__)

# List with the devices from pods (for table is all of this)
devicesList = [
	{'POD': '1', 'Type': 'Router', 'Index': '1', 'Power status': False},
	{'POD': '1', 'Type': 'Router', 'Index': '2', 'Power status': False},
	{'POD': '1', 'Type': 'Router', 'Index': '3', 'Power status': False},
	{'POD': '1', 'Type': 'Router', 'Index': '4', 'Power status': False},
	{'POD': '1', 'Type': 'Router', 'Index': '5', 'Power status': False},
	{'POD': '1', 'Type': 'Router', 'Index': '6', 'Power status': False},
	{'POD': '1', 'Type': 'Router', 'Index': '7', 'Power status': False},
	{'POD': '1', 'Type': 'Router', 'Index': '8', 'Power status': False},
	{'POD': '1', 'Type': 'Switch', 'Index': '1', 'Power status': False},
	{'POD': '1', 'Type': 'Switch', 'Index': '2', 'Power status': False},
	{'POD': '1', 'Type': 'Switch', 'Index': '3', 'Power status': False},
	{'POD': '1', 'Type': 'Switch', 'Index': '4', 'Power status': False},
	{'POD': '2', 'Type': 'Router', 'Index': '1', 'Power status': False},
	{'POD': '2', 'Type': 'Router', 'Index': '2', 'Power status': False},
	{'POD': '2', 'Type': 'Router', 'Index': '3', 'Power status': False},
	{'POD': '2', 'Type': 'Router', 'Index': '4', 'Power status': False},
	{'POD': '2', 'Type': 'Router', 'Index': '5', 'Power status': False},
	{'POD': '2', 'Type': 'Router', 'Index': '6', 'Power status': False},
	{'POD': '2', 'Type': 'Router', 'Index': '7', 'Power status': False},
	{'POD': '2', 'Type': 'Router', 'Index': '8', 'Power status': False},
	{'POD': '2', 'Type': 'Switch', 'Index': '1', 'Power status': False},
	{'POD': '2', 'Type': 'Switch', 'Index': '2', 'Power status': False},
	{'POD': '2', 'Type': 'Switch', 'Index': '3', 'Power status': False},
	{'POD': '2', 'Type': 'Switch', 'Index': '4', 'Power status': False},
]

# Compute the table with the status of every device in a new file
def computeTable():
	pivotTable = pandas.pivot_table(
		pandas.DataFrame(devicesList),
		values = ['Power status'],
		index = ['POD', 'Index'],
		columns = ['Type'],
		fill_value = ''
	).to_html('templates/result.html')

@app.route('/', methods = ['POST', 'GET'])
def state():
	if ( request.method == 'POST' ):
		# Get data from the request, a dictionary with keys: pod, type, index
		data = request.form.to_dict()
		indexFromRequest = 0
		listIndex = 0
		validEntry = True

		# With the pod, type and index is calculated the index of the
		# requested device from list (order in that list is important)
		# Verify if data is valid and computing index
		if ( 'pod' in data.keys() ):
			pod = int(data["pod"])

			if ( pod == 2 ):
				listIndex = 12
		else:
			validEntry = False

		if ( data["index"] != '' ):
			indexFromRequest = int(data["index"])
			listIndex += indexFromRequest - 1
		else:
			validEntry = False

		if ( 'type' in data.keys() ):
			if ( data["type"] == "switch" ):
				# Only 4 switches per pod
				if ( indexFromRequest <= 4 ):
					listIndex += 8
				else:
					validEntry = False

		if ( validEntry == True ):
			status = devicesList[listIndex]["Power status"]

			if ( status == True ):
				devicesList[listIndex]["Power status"] = False
			else:
				devicesList[listIndex]["Power status"] = True

		# Update the page with the devices status
		computeTable()
		return render_template('pods.html')

	else:
		# Show the updated page with the devices status
		computeTable()
		return render_template('pods.html')

@app.route('/result.html')
def result():
	return render_template('result.html')

if __name__ == '__main__':
	applyActionToAllOutlets(2, 1)  # Turn Immediate OFF all Outlets of apc[1]; default state is OFF
	app.run(debug = True) # Might be a partial solution for #3 issue app.run(debug = True, port=int(sys.argv[1]))
