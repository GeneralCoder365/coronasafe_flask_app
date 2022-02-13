# Getting Chart Studio/Plotly credentials:
import os
from dotenv import load_dotenv
from pathlib import Path
# ! FOR LOCAL TESTING!
dotenv_path = Path('plotly_chart_studio_credentials.env')
load_dotenv(dotenv_path=dotenv_path)
CS_USERNAME = str(os.getenv('CS_USERNAME'))
CS_API_KEY = str(os.getenv('CS_API_KEY'))

# CS_USERNAME = str(os.environ['CS_USERNAME'])
# CS_API_KEY = str(os.environ['CS_API_KEY'])

# print(CS_USERNAME)
# print(CS_API_KEY)

import plotly
import chart_studio.plotly as py
import chart_studio.tools as tls
import plotly.express as px
from plotly.offline import plot
import plotly.io as pio
import pandas as pd
import chart_studio
chart_studio.tools.set_credentials_file(username=CS_USERNAME, api_key=CS_API_KEY)


import ssl
import urllib.request
from urllib.request import urlopen
import json
from datetime import datetime, time

from github import Github, UnknownObjectException

# ! FOR LOCAL TESTING!
# import os
# from dotenv import load_dotenv
# from pathlib import Path
# dotenv_path = Path('github_api_access_token.env')
# load_dotenv(dotenv_path=dotenv_path)
# GITHUB_API_TOKEN = str(os.getenv('GITHUB_API_TOKEN'))
# print(GITHUB_API_TOKEN)

# github_object = Github(GITHUB_API_TOKEN)
# repository = github_object.get_user().get_repo('coronasafe_data_storage')

def github_updater_us_case_map_embed_url(GITHUB_API_TOKEN, html_embed_url):
    github_object = Github(GITHUB_API_TOKEN)
    repository = github_object.get_user().get_repo('coronasafe_data_storage')
    
    # path in the repository
    filename = 'us_case_map_url.txt'
    content = html_embed_url
    # create with commit message
    # file = repository.create_file(filename, "edit_file via PyGithub", content)

    try:
        file = repository.get_contents(filename)
        
        # update file syntax: repository.update_file(path, message, content, sha, branch=NotSet, committer=NotSet, author=NotSet)
        repository.update_file(file.path, "update us case map url", content, file.sha, branch="main")
    # Error raised: github.GithubException.UnknownObjectException: 404 {"message": "Not Found", "documentation_url": "https://docs.github.com/rest/reference/repos#get-repository-content"}
    except UnknownObjectException:
        file = repository.create_file(filename, "create us_case_map_url.txt", content)

# tester code
# print(github_updater_us_case_map_embed_url(make_us_case_map()))

# makes US heat map (auto overwrites any existing one)
def create_us_case_map(GITHUB_API_TOKEN):
    ssl._create_default_https_context = ssl._create_unverified_context
    response = urllib.request.urlopen('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv')
    response1 = urllib.request.urlopen('https://raw.githubusercontent.com/jasonong/List-of-US-States/master/states.csv')

    url = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv"
    df = pd.read_csv(url, converters={'fips': lambda x: str(x)})

    url = "https://raw.githubusercontent.com/jasonong/List-of-US-States/master/states.csv"
    df_abbrev = pd.read_csv(url)

    last_date = df['date'].max()
    df = df[ df['date'] == last_date]
    # print(df['cases'].sum())
    df = df.groupby('state')['cases'].sum().to_frame()
    df = pd.merge(df, df_abbrev, left_on=df.index, right_on='State')

    fig = px.choropleth(df, locations=df['Abbreviation'], color=df['cases'],
                        locationmode="USA-states",
                        # alternate colour scheme -> color_continuous_scale=px.colors.diverging.RdYlGn[::-1],
                        # _r reverses the hot colour scheme
                        color_continuous_scale="hot_r",
                        range_color=(0, 4500000),
                        scope="usa"
                            )

    fig.update_layout(paper_bgcolor="#4E5D6C")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, geo=dict(bgcolor= '#4E5D6C',lakecolor='#4E5D6C'))
    # fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    
    # fig.write_html('maps/us_map.html')
    # ! FOR OFFLINE TESTING
    # ! plot <-- plotly.offline.plot
    # plot(fig, filename = 'templates/us_map.html', auto_open=False)

    plotly_url = py.plot(fig, filename='us_case_map', auto_open=False, sharing='public')

    # html_embed_code = tls.get_embed(plotly_url)
    # print(html_embed_code)
    
    plotly_html_embed_url = plotly_url[:-1] + ".embed"
    
    github_updater_us_case_map_embed_url(GITHUB_API_TOKEN, plotly_html_embed_url)
    
    return plotly_html_embed_url

# tester code
# print(make_us_case_map(GITHUB_API_TOKEN))


def get_us_case_map(GITHUB_API_TOKEN):
    github_object = Github(GITHUB_API_TOKEN)
    repository = github_object.get_user().get_repo('coronasafe_data_storage')
    
    # path in the repository
    filename = 'us_case_map_url.txt'

    # create with commit message
    # file = repository.create_file(filename, "edit_file via PyGithub", content)

    try:
        file = repository.get_contents(filename)
        
        # read file
        us_case_map_html_embed_url = file.decoded_content.decode()
    
    # Error raised: github.GithubException.UnknownObjectException: 404 {"message": "Not Found", "documentation_url": "https://docs.github.com/rest/reference/repos#get-repository-content"}
    except UnknownObjectException:
        us_case_map_html_embed_url = create_us_case_map(GITHUB_API_TOKEN)

    
    return us_case_map_html_embed_url

# tester code
# print(get_us_case_map())

def get_us_state_fips_code(state):
    state = state.title()
    us_state_to_fips_code = {
        "Alabama": "01",
        "Alaska": "02",
        "Arizona": "04",
        "Arkansas": "05",
        "California": "06",
        "Colorado": "08",
        "Connecticut": "09",
        "Delaware": "10",
        "District of Columbia": "11",
        "Florida": "12",
        "Georgia": "13",
        "Hawaii": "14",
        "Idaho": "15",
        "Illinois": "17",
        "Indiana": "18",
        "Iowa": "19",
        "Kansas": "20",
        "Kentucky": "21",
        "Louisiana": "22",
        "Maine": "23",
        "Maryland": "24",
        "Massachusetts": "25",
        "Michigan": "26",
        "Minnesota": "27",
        "Mississippi": "28",
        "Missouri": "29",
        "Montana": "30",
        "Nebraska": "31",
        "Nevada": "32",
        "New Hampshire": "33",
        "New Jersey": "34",
        "New Mexico": "35",
        "New York": "36",
        "North Carolina": "37",
        "North Dakota": "38",
        "Ohio": "39",
        "Oklahoma": "40",
        "Oregon": "41",
        "Pennsylvania": "42",
        "Puerto Rico": "72",
        "Rhode Island": "44",
        "South Carolina": "45",
        "South Dakota": "46",
        "Tennessee": "47",
        "Texas": "48",
        "Utah": "49",
        "Vermont": "50",
        "Virginia": "51",
        "U.S. Virgin Islands": "78",
        "Washington": "53",
        "West Virginia": "54",
        "Wisconsin": "55",
        "Wyoming": "56",
        "American Samoa": "60",
        "Guam": "66",
        "Northern Mariana Islands": "69"
    }
    state_fips_code = str(us_state_to_fips_code[state])
    
    return state_fips_code
# print(get_us_state_fips_code('California'))

def generate_custom_state_only_geojson_file(state):
    state = state.title()
    state_fips_code = get_us_state_fips_code(state)
    
    with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
        # counties = json.load(response)
        raw_geojson = json.loads(response.read())["features"]
    
    custom_geojson = {"type": "FeatureCollection", "features": []}
    county_names_in_geojson = []
    
    # print(raw_geojson)
    
    for i in range(len(raw_geojson)):
        raw_geojson_county_data = raw_geojson[i]
        raw_geojson_state_fips_code = raw_geojson_county_data["properties"]["STATE"]
        
        raw_geojson_county_data["properties"]["NAME"] = raw_geojson_county_data["properties"]["NAME"].lower()
        
        if (raw_geojson_state_fips_code == state_fips_code):
            # print(raw_geojson_county_data["properties"]["NAME"])
            if (raw_geojson_county_data["properties"]["NAME"] in county_names_in_geojson):
                # ! TEMPORARY FIX TO HAVING BALTIMORE AND BALTIMORE CITY IN DF, BUT HAVING 2 BALTIMORES IN SAME STATE IN GEOJSON
                raw_geojson_county_data["properties"]["NAME"] = str(raw_geojson_county_data["properties"]["NAME"]) + " city"
            elif (raw_geojson_county_data["properties"]["NAME"] == state.lower()):
                # ! TEMPORARY FIX TO HAVING NEW YORK CITY IN DF, BUT HAVING NEW YORK COUNTY IN NEW YORK STATE IN GEOJSON
                raw_geojson_county_data["properties"]["NAME"] = str(raw_geojson_county_data["properties"]["NAME"]) + " city"
            
            county_names_in_geojson.append(str(raw_geojson_county_data["properties"]["NAME"]))
            # print(county_names_in_geojson)
            custom_geojson["features"].append(raw_geojson_county_data)
            # print(raw_geojson[i]["properties"]["NAME"])
    # print(county_names_in_geojson)
    
    return custom_geojson
# print(generate_custom_state_only_geojson_file('maryland'))

def github_updater_us_state_case_map_embed_url(state, GITHUB_API_TOKEN, html_embed_url):
    state = state.title()
    
    github_object = Github(GITHUB_API_TOKEN)
    repository = github_object.get_user().get_repo('coronasafe_data_storage')
    
    # path in the repository
    filename = 'us_state_case_map_urls.json'
    new_json_file_content = {}
    new_json_file_content[state] = html_embed_url
    # ! converts dict to str of dict
    new_json_file_content = json.dumps(new_json_file_content)
    # print(new_json_file_content)
    # create with commit message
    # file = repository.create_file(filename, "edit_file via PyGithub", content)

    try:
        file = repository.get_contents(filename)
        
        # read file
        file_text = file.decoded_content.decode()
        # print(file_text)
        # converts str form of dict from github file back to dict
        file_dict = json.loads(file_text)
        
        file_dict[state] = html_embed_url
        
        # sorts dictionary of state and embed urls alphabetically by state
        file_dict = {key: value for key, value in sorted(file_dict.items())}
        
        # ! converts dict to str of dict
        updated_file_content = json.dumps(file_dict)
        
        # update file syntax: repository.update_file(path, message, content, sha, branch=NotSet, committer=NotSet, author=NotSet)
        repository.update_file(file.path, "update us_state_case_map_urls.json", updated_file_content, file.sha, branch="main")
        
    # Error raised: github.GithubException.UnknownObjectException: 404 {"message": "Not Found", "documentation_url": "https://docs.github.com/rest/reference/repos#get-repository-content"}
    except UnknownObjectException:
        file = repository.create_file(filename, "create us_state_case_map_urls.json", new_json_file_content)

# tester code
# print(github_updater_us_state_case_map_embed_url(make_us_case_map()))

# makes us state case graph
def create_us_state_case_map(state, GITHUB_API_TOKEN):
    state = state.title()

    geojson = generate_custom_state_only_geojson_file(state)
    
    # response = urllib.request.urlopen('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv')

    url = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv"
    # df = pd.read_csv(url, converters={'fips': lambda x: str(x)})
    # df = pd.read_csv(url, dtype={"county": str})
    df = pd.read_csv(url, converters={'county': lambda x: str(x)})

    #Pick a state
    df_state = df[df['state'] == state]
    # print(df_state)
    # print(df_state[df_state['county'] == 'Allegany'])
    last_date = df['date'].max()
    df = df_state[df_state['date'] == last_date]
    
    # counties_in_state = df['county']
    counties_in_state = []
    # print(df)
    # .lower() to all county names in state df to match with custom_geojson county format
    for i in df.index:
        # print(df[df.index == i])
        # print(df[df.index == i]['county'])
        df_county = str(df.at[i,'county']).lower()
        df.at[i,'county'] = df_county
        counties_in_state.append(df_county)
    
    # print(counties_in_state)
    cases_in_state = df['cases']
    
    max_cases = int(df['cases'].max())
    # print("max_cases: ", max_cases)
    # print(df[df['cases'] == max_cases])

    total_cases = int(df['cases'].sum())
    total_deaths = int(df['deaths'].sum())
    # print("total_cases: ", total_cases)
    # print("total_deaths: ", total_deaths)
    
    # fig = px.choropleth(df, geojson=counties, locations='fips', color='cases',
    # fig = px.choropleth(df, geojson=geojson, locations='county', featureidkey="properties.NAME", color='cases',
    fig = px.choropleth(df, geojson=geojson, locations=counties_in_state, featureidkey="properties.NAME", color=cases_in_state,
                            # color_continuous_scale="Viridis",
                            # range_color=(0, 20000)
                            # ! alternate colour scheme -> color_continuous_scale=px.colors.diverging.RdYlGn[::-1],
                            # ! _r reverses the hot colour scheme
                            color_continuous_scale="hot_r",
                            range_color=(0, max_cases)
                            )

    #Added for zoom and to set rest of map to invisible. 
    fig.update_geos(fitbounds="locations", visible=False)
    
    # title = "COVID-19 Cases From Each County in " + str(state)
    # fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, title_text=title)
    
    fig.update_layout(paper_bgcolor="#4E5D6C")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, geo=dict(bgcolor= '#4E5D6C',lakecolor='#4E5D6C'))
    
    formatted_state_name = state.replace(".", "")
    formatted_state_name = formatted_state_name.replace(" ", "_")
    formatted_state_name = formatted_state_name.lower()
    
    plot_name = state.lower() + "_case_map" 
    
    # ! FOR OFFLINE TESTING
    # ! plot <-- plotly.offline.plot
    # offline_file_name = "templates/" + plot_name + ".html"
    # plot(fig, filename = offline_file_name, auto_open=False)
    # plot(fig, filename = offline_file_name, auto_open=True)
    
    
    plotly_url = py.plot(fig, filename=plot_name, auto_open=False, sharing='public')
    
    plotly_html_embed_url = plotly_url[:-1] + ".embed"
    # print(plotly_html_embed_url)
    
    github_updater_us_state_case_map_embed_url(state, GITHUB_API_TOKEN, plotly_html_embed_url)
    
    return plotly_html_embed_url

# tester code -> I think the format for the state is: Ex. "Maryland"
# print(create_us_state_case_map("florida", GITHUB_API_TOKEN))

def get_us_state_case_map(state, GITHUB_API_TOKEN):
    state = state.title()
    
    github_object = Github(GITHUB_API_TOKEN)
    repository = github_object.get_user().get_repo('coronasafe_data_storage')
    
    # path in the repository
    filename = 'us_state_case_map_urls.json'

    # create with commit message
    # file = repository.create_file(filename, "edit_file via PyGithub", content)

    try:
        file = repository.get_contents(filename)
        
        # read file, convert to dict, get the embed url for given state
        us_state_case_map_html_embed_url = json.loads(file.decoded_content.decode())[state]
    
    # Error raised: github.GithubException.UnknownObjectException: 404 {"message": "Not Found", "documentation_url": "https://docs.github.com/rest/reference/repos#get-repository-content"}
    # Error raised: KeyError: 'Maryland'
    except (UnknownObjectException, KeyError):
        us_state_case_map_html_embed_url = create_us_state_case_map(state, GITHUB_API_TOKEN)

    
    return us_state_case_map_html_embed_url

# tester code
# print(get_us_state_case_map("maryland", GITHUB_API_TOKEN))

def create_all_us_state_case_maps(GITHUB_API_TOKEN):
    us_states = ['Alabama','Alaska','Arizona','Arkansas','California','Colorado',
                 'Connecticut','Delaware','Florida','Georgia','Hawaii','Idaho',
                 'Illinois','Indiana','Iowa','Kansas','Kentucky','Louisiana',
                 'Maine','Maryland','Massachusetts','Michigan','Minnesota',
                 'Mississippi','Missouri','Montana','Nebraska','Nevada',
                 'New Hampshire','New Jersey','New Mexico','New York',
                 'North Carolina','North Dakota','Ohio','Oklahoma','Oregon',
                 'Pennsylvania','Rhode Island','South Carolina','South Dakota',
                 'Tennessee','Texas','Utah','Vermont','Virginia','Washington',
                 'West Virginia','Wisconsin','Wyoming']
    html_embed_urls = {}
    
    for i in range(len(us_states)):
        html_embed_urls[us_states[i]] = create_us_state_case_map(us_states[i], GITHUB_API_TOKEN)
    # passes html_embed_urls in str format of dict
    # html_embed_urls = json.dumps(html_embed_urls)
    # print(html_embed_urls)
    
    return html_embed_urls

# tester code
# print(create_all_us_state_case_maps(GITHUB_API_TOKEN))

# current_time = datetime.now().time()
# current_time = current_time.strftime("%H:%M:%S")
# print(current_time)
# print(str(time.min))

# if (current_time == "12:26:30"):
#     make_us_heat_map()