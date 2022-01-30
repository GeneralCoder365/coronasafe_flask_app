import pandas as pd

# REQUIREMENTS:
# GLOBAL:
    # COUNTRY CASES OVER LAST 30 DAYS/COUNTRY POPULATION
    # COUNTRY INFECTED OVER LAST 30 DAYS AS PERCENTAGE
    # STATE CASES OVER LAST 30 DAYS/STATE POPULATION
    # STATE INFECTED OVER LAST 30 DAYS AS PERCENTAGE



def get_us_state_population(state):
    state = state.capitalize()
    us_state_to_abbrev = {
        "Alabama": "AL",
        "Alaska": "AK",
        "Arizona": "AZ",
        "Arkansas": "AR",
        "California": "CA",
        "Colorado": "CO",
        "Connecticut": "CT",
        "Delaware": "DE",
        "Florida": "FL",
        "Georgia": "GA",
        "Hawaii": "HI",
        "Idaho": "ID",
        "Illinois": "IL",
        "Indiana": "IN",
        "Iowa": "IA",
        "Kansas": "KS",
        "Kentucky": "KY",
        "Louisiana": "LA",
        "Maine": "ME",
        "Maryland": "MD",
        "Massachusetts": "MA",
        "Michigan": "MI",
        "Minnesota": "MN",
        "Mississippi": "MS",
        "Missouri": "MO",
        "Montana": "MT",
        "Nebraska": "NE",
        "Nevada": "NV",
        "New Hampshire": "NH",
        "New Jersey": "NJ",
        "New Mexico": "NM",
        "New York": "NY",
        "North Carolina": "NC",
        "North Dakota": "ND",
        "Ohio": "OH",
        "Oklahoma": "OK",
        "Oregon": "OR",
        "Pennsylvania": "PA",
        "Rhode Island": "RI",
        "South Carolina": "SC",
        "South Dakota": "SD",
        "Tennessee": "TN",
        "Texas": "TX",
        "Utah": "UT",
        "Vermont": "VT",
        "Virginia": "VA",
        "Washington": "WA",
        "West Virginia": "WV",
        "Wisconsin": "WI",
        "Wyoming": "WY",
        "District of Columbia": "DC",
        "American Samoa": "AS",
        "Guam": "GU",
        "Northern Mariana Islands": "MP",
        "Puerto Rico": "PR",
        "United States Minor Outlying Islands": "UM",
        "U.S. Virgin Islands": "VI",
    }
    state = us_state_to_abbrev[state]
    # print(state)
    
    # https://github.com/JoshData/historical-state-population-csv/blob/primary/historical_state_population_by_year.csv
    url = "https://raw.githubusercontent.com/JoshData/historical-state-population-csv/primary/historical_state_population_by_year.csv"
    df = pd.read_csv(url, converters={'fips': lambda x: str(x)}, header=None)
    # ! type(df) = <class 'pandas.core.frame.DataFrame'>
    
    # Columns: 0 (State Abbreviation), 1 (Year), 2 (Population)
    
    # print(df)
    
    df_state = df[df[0] == state]
    most_recent_year = df_state[1].max()
    state_population = int(df_state[df_state[1] == most_recent_year][2].values[0])
    
    # print(df_state)
    # print(most_recent_year)
    # print(state_population)

    return state_population
# print(get_us_state_population('California'))

