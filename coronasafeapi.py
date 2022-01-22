from flask import Flask, render_template
from flask import request
from flask_restful import Resource, Api, reqparse
# getting the api key
import os
import coronasafe_v3_backend as cs_backend

app = Flask(__name__)
api = Api(app)


@app.route('/getPlaces', methods=["GET"])
def search():
    search_query = request.args.get('query')
    print("search_query: ", search_query)
    str_location = request.args.get('location')
    print("str_location: ", str_location)
    data = cs_backend.places_search(search_query, str_location)
    print(data)
    return {'data':data}, 200

@app.route('/getRisk', methods=["GET"])
def getNumbers():
    raw_address = request.args.get('address')
    data = cs_backend.corona_safe(raw_address)
    return {'data':data}, 200
# (Westfield Montgomery) 7101 Democracy Blvd, Bethesda, MD 20852, United States
# (Empire State Building) 20 W 34th St, New York, NY 10001

@app.route('/getUSCaseMap', methods=["GET"])
def get_us_heat_map():
    return render_template('us_map.html')


app.debug = True

if __name__ == '__main__':
    app.run()