from flask import Flask
from flask import request
from flask import render_template
import json

app = Flask(__name__, static_url_path='', static_folder='static')

@app.route('/')
def index():
    #load a current view of the data
    f = open("data/scores.json", "r")
    data = json.load(f) #object format 
    f.close()

    #render the template with the apporpriate data
    return render_template('index.html', pets = data.keys())


@app.route('/all_scores')
def all_scores():
    #load a current view of the data
    f = open("data/scores.json", "r")
    data = json.load(f)
    f.close()

    #check to see if year is in the query string portion of the URL
    requested_year = request.args.get('year')
    if requested_year == None:
        requested_year = "2020" #just in case

    #Filter and reformat data for ease of access in the template
    pets = list(data.keys())
    requested_data = {}
    for pet in pets:
        requested_data[pet] = data[pet][requested_year]
    all_years = sorted(list(data[pets[0]].keys()))

    return render_template('all_scores.html', year=requested_year, all_years=all_years, data=requested_data)


@app.route('/scores/<pet_type>')
def specific_scores(pet_type):
    #load a current view of the data
    f = open("data/scores.json", "r")
    data = json.load(f)
    f.close()

    #Check to see if year is passed via the query string portion of the URL
    requested_pet = pet_type
    if requested_pet not in data:
        requested_pet = "tigers"

    #Filter and reformat data for ease of access in the template
    requested_data = data[requested_pet]
    years = sorted(list(requested_data.keys()))
    line_endpoints =[]
    for i in range(len(years)-1): # make it easy to dynamically generate a line graph
        start_x = years[i] #generate endpoints for each line segment
        stop_x = years[i+1]
        line_endpoints.append([requested_data[start_x],requested_data[stop_x]] )

    return render_template('individual_scores.html', pet=requested_pet, years = years, endpoints = line_endpoints)

app.run(debug=True)
