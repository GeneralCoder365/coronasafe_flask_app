from flask import Flask, render_template
from flask import request
from flask_restful import Resource, Api, reqparse
# getting the api key
# import os
import sys
import logging
import gc
import multiprocessing
from memory_profiler import profile

import coronasafe_v3_backend as cs_backend

# def memory_tracker():
#     print('Memory usage         : % 2.2f MB' % round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024.0,1))
# memory_tracker()

def garbage_collect():
    print("boobiesBOI")
    # memory_tracker()
    # gc.set_debug(gc.DEBUG_LEAK)
    gc.collect()

app = Flask(__name__)
api = Api(app)

app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)


@app.route('/getPlaces', methods=["GET"])
@profile
def search():
    search_query = request.args.get('query')
    # print("search_query: ", search_query)
    str_location = request.args.get('location')
    # print("str_location: ", str_location)
    data = cs_backend.places_search(search_query, str_location)
    # print(data)
    return {'data':data}, 200

@app.route('/getRisk', methods=["GET"])
def getNumbers():
    raw_address = request.args.get('address')
    data = cs_backend.corona_safe(raw_address)
    return {'data':data}, 200
# (Westfield Montgomery) 7101 Democracy Blvd, Bethesda, MD 20852, United States
# (Empire State Building) 20 W 34th St, New York, NY 10001


@app.route('/createUSCaseMap', methods=["GET"])
def create_us_case_map():
    us_case_map_html_embed_url = cs_backend.create_us_case_map()
    return {'data':us_case_map_html_embed_url}, 200

@app.route('/getUSCaseMap', methods=["GET"])
def get_us_case_map():
    us_case_map_html_embed_url = cs_backend.get_us_case_map()
    return {'data':us_case_map_html_embed_url}, 200

@app.route('/createUSStateCaseMap', methods=["GET"])
def create_us_state_case_map():
    state = str(request.args.get('state')).title()
    us_state_case_map_html_embed_url = cs_backend.create_us_state_case_map(state)
    return {'data':us_state_case_map_html_embed_url}, 200

@app.route('/getUSStateCaseMap', methods=["GET"])
def get_us_state_case_map():
    state = str(request.args.get('state')).title()
    us_state_case_map_html_embed_url = cs_backend.get_us_state_case_map(state)
    return {'data':us_state_case_map_html_embed_url}, 200

@app.route('/createAllUSStateCaseMaps', methods=["GET"])
def create_all_us_state_case_maps():
    us_state_case_maps_html_embed_urls = cs_backend.create_all_us_state_case_maps()
    return {'data':us_state_case_maps_html_embed_urls}, 200


@app.route('/getCOVIDCaseStats', methods=["GET"])
@profile
def get_covid_case_stats():
    garbage_collect()
    country = str(request.args.get('country')).title()
    state = str(request.args.get('state')).title()
    covid_stats = []
    queue = multiprocessing.Queue()
    process = multiprocessing.Process(target=cs_backend.get_covid_case_stats, args=(country, state, queue))
    process.start()
    process.join() # The join() method, when used with threading or multiprocessing, is not related to str.join() - it's not actually concatenating anything together. Rather, it just means "wait for this [thread/process] to complete"
    print("boob")
    covid_stats = queue.get()
    process.terminate()
    print(process.is_alive())
    queue.close()
    # covid_stats = cs_backend.get_covid_case_stats(country, state)
    return {'data':covid_stats}, 200

@app.before_request 
def before_request_callback():
    garbage_collect()
    # method = request.method 
    # path = request.path 
         
    # if path == "/" and method == "POST": 
    #     myfunction()
 
@app.after_request 
def after_request_callback(response): 
    garbage_collect()
    return response
    # response_value = response.get_data() 
    # print(response_value)
 
    # return response

app.debug = True

if __name__ == '__main__':
    app.run()