#!/usr/bin/python

from cProfile import label
import cgi
import cgitb
from xml.etree.ElementTree import tostring
cgitb.enable()
import json

print("Content-Type: text/html\n")

filename = "database.json"
json_data = {}

def Form2Dict():
    D = {}
    F = cgi.FieldStorage()
    for k in F.keys():
        try:
            v = int( F.getvalue(k) )
        except:
            try:
                v = float( F.getvalue(k) )
            except:
                v = str( F.getvalue(k) )
        D[k] = v
    return D
    
D = Form2Dict()

D['status'] = True
print(json.dumps(D))

def get():
    json_data = {}
    id = D['id']
    with open(filename, 'r') as json_file:
        json_data = json.load(json_file)

    for rider in json_data['riders']:
        if rider['id'] == id:
            print(True)
            rider['date'] = ''


    with open(filename, "w") as json_file:
        json_data = json.dumps(json_data)
        json_file.write(json_data)
        json_file.close()
    

trips = {}

def add():
    json_data = {}
    # Open file, read into local dict variable, edit.
    with open(filename, 'r') as json_file:
        json_data = json.load(json_file)
    
    #D['_latlng'] is in the form: LatLng(30.351819, -97.700206)
    latlng = D['_latlng'].replace('LatLng' , '').replace('(','').replace(')','').replace(' ','').split(',')
    #resulted form ["30.351819", "-97.700206"]

    # Add riders to the database
    user = {"id": D["id"], "name": D["name"], "surname": D["surname"], "birthdate": D["birthdate"], "location":latlng, "date" : D['date'], "picked" : D['picked'], 'waiver': D['waiver']}
    temp_rider = False
    for rider in json_data["riders"]:
        if rider['id'] == user['id']:
            if rider['name'] == user['name'] and rider['surname'] == user['surname'] and rider['birthdate'] == rider['birthdate']:
                temp_rider = True
                rider['date'] = user['date']
                rider['location'] = user['location']
            else:
                return 'False'
    if temp_rider == False:
        json_data["riders"].append(
            user
    )

    # Update trips list in the database
    temp = False
    for trip in json_data['trips']:
        if D['date'] in trip.keys():
            for t in trip[D['date']]:
                if t[0] == D['id']:
                    temp = True
            if temp == False:
                trip[D['date']].append([D['id'] , latlng])
        else:
            trip[D['date']] = [[D['id'] , latlng]]
    
    # Write local dict (edited) back to json file.
    with open(filename, "w") as json_file:
        json_data = json.dumps(json_data)
        json_file.write(json_data)
        json_file.close()



if(D["function"] == "add"):
    add()
else:
    get()