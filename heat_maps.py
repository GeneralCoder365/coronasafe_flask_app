# Getting Chart Studio/Plotly credentials:
import os
from dotenv import load_dotenv
from pathlib import Path
dotenv_path = Path('chart_studio_credentials.env')

load_dotenv(dotenv_path=dotenv_path)
CS_USERNAME = str(os.getenv('CS_USERNAME'))
CS_API_KEY = str(os.getenv('CS_API_KEY'))
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
dotenv_path = Path('github_api_token.env')
load_dotenv(dotenv_path=dotenv_path)
GITHUB_API_TOKEN = str(os.getenv('GITHUB_API_TOKEN'))
# print(GITHUB_API_TOKEN)

github_object = Github(GITHUB_API_TOKEN)
repository = github_object.get_user().get_repo('coronasafe_plotly_map_urls')

def github_updater_us_case_map_embed_url(html_embed_url):
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
def make_us_case_map():
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
    # ! plot <-- plotly.offline.plot
    # plot(fig, filename = 'templates/us_map.html', auto_open=False)

    plotly_url = py.plot(fig, filename='us_case_map', auto_open=False, sharing='public')

    # html_embed_code = tls.get_embed(plotly_url)
    # print(html_embed_code)
    
    plotly_html_embed_url = plotly_url[:-1] + ".embed"
    
    github_updater_us_case_map_embed_url(plotly_html_embed_url)
    
    return plotly_html_embed_url

# # tester code
# print(make_us_case_map())


def get_us_case_map():
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
        us_case_map_html_embed_url = make_us_case_map()

    
    return us_case_map_html_embed_url

# tester code
# print(get_us_case_map())




# makes state case graph
def make_state_case_graph(state_input):
    ssl._create_default_https_context = ssl._create_unverified_context
    response1 = urllib.request.urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json')

    with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
        counties = json.load(response)

    counties["features"][0]

    response = urllib.request.urlopen('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv')

    url = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv"
    df = pd.read_csv(url, converters={'fips': lambda x: str(x)})

    #Pick a state
    df_Maryland = df[ df['state'] == state_input]
    last_date = df['date'].max()
    df = df_Maryland[ df_Maryland['date'] == last_date]

    print(df['cases'].sum())
    print(df['deaths'].sum())


    fig = px.choropleth(df, geojson=counties, locations='fips', color='cases',
                            color_continuous_scale="Viridis",
                            range_color=(0, 20000)
                            )

    #Added for zoom and to set rest of map to invisible. 
    fig.update_geos(fitbounds="locations", visible=False)

    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, title_text='COVID-19 Cases From Each County in Maryland')
    plot(fig)

# tester code -> I think the format for the state is: Ex. "MD"
# make_state_case_graph("MD")



# current_time = datetime.now().time()
# current_time = current_time.strftime("%H:%M:%S")
# print(current_time)
# print(str(time.min))

# if (current_time == "12:26:30"):
#     make_us_heat_map()