from flask import Flask
from flask import request
from flask_restful import Resource, Api, reqparse
# getting the api key
import os
import coronasafe_v2_backend as cs_backend

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

@app.route('/getNumbers', methods=["GET"])
def getNumbers():
    raw_address = request.args.get('address')
    data = cs_backend.master_risk_calculator(raw_address)
    return {'data':data}, 200

app.debug = True

if __name__ == '__main__':
    app.run()