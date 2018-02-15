#!/usr/bin/env python3

# Author: Andrei Raduta
# E-mail: andrei.raduta11@gmail.com
# Script usage: python3 webserver.py [port-number] (default port = 5000)

from flask import Flask, render_template, request
import pandas, numpy

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
   app.run(debug = True)
