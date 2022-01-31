from datetime import datetime, date, timedelta
import pandas as pd

import pycountry

# REQUIREMENTS:
# GLOBAL:
    # COUNTRY CASES OVER LAST 30 DAYS / COUNTRY POPULATION --> Done
    # COUNTRY INFECTED OVER LAST 30 DAYS AS PERCENTAGE
    # STATE CASES OVER LAST 30 DAYS / STATE POPULATION (US ONLY) --> Done
    # STATE INFECTED OVER LAST 30 DAYS AS PERCENTAGE (US ONLY) --> Done

def get_country_population(country):    
    # https://github.com/datasets/population/blob/master/data/population.csv
    url = "https://raw.githubusercontent.com/datasets/population/master/data/population.csv"
    df = pd.read_csv(url, converters={'Country Code': lambda x: str(x)}, header=0)
    # print(df)
    
    # country_names = ['Arab World', 'Caribbean small states', 'Central Europe and the Baltics', 'Early-demographic dividend', 'East Asia & Pacific', 'East Asia & Pacific (excluding high income)', 'East Asia & Pacific (IDA & IBRD countries)', 'Euro area', 'Europe & Central Asia', 'Europe & Central Asia (excluding high income)', 'Europe & Central Asia (IDA & IBRD countries)', 'European Union', 'Fragile and conflict affected situations', 'Heavily indebted poor countries (HIPC)', 'High income', 'IBRD only', 'IDA & IBRD total', 'IDA blend', 'IDA only', 'IDA total', 'Late-demographic dividend', 'Latin America & Caribbean', 'Latin America & Caribbean (excluding high income)', 'Latin America & the Caribbean (IDA & IBRD countries)', 'Least developed countries: UN classification', 'Low & middle income', 'Low income', 'Lower middle income', 'Middle East & North Africa', 'Middle East & North Africa (excluding high income)', 'Middle East & North Africa (IDA & IBRD countries)', 'Middle income', 'North America', 'OECD members', 'Other small states', 'Pacific island small states', 'Post-demographic dividend', 'Pre-demographic dividend', 'Small states', 'South Asia', 'South Asia (IDA & IBRD)', 'Sub-Saharan Africa', 'Sub-Saharan Africa (excluding high income)', 'Sub-Saharan Africa (IDA & IBRD countries)', 'Upper middle income', 'World', 'Afghanistan', 'Albania', 'Algeria', 'American Samoa', 'Andorra', 'Angola', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Aruba', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas, The', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bermuda', 'Bhutan', 'Bolivia', 'Bosnia and Herzegovina', 'Botswana', 'Brazil', 'British Virgin Islands', 'Brunei Darussalam', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cabo Verde', 'Cambodia', 'Cameroon', 'Canada', 'Cayman Islands', 'Central African Republic', 'Chad', 'Channel Islands', 'Chile', 'China', 'Colombia', 'Comoros', 'Congo, Dem. Rep.', 'Congo, Rep.', 'Costa Rica', "Cote d'Ivoire", 'Croatia', 'Cuba', 'Curacao', 'Cyprus', 'Czech Republic', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'Ecuador', 'Egypt, Arab Rep.', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Eswatini', 'Ethiopia', 'Faroe Islands', 'Fiji', 'Finland', 'France', 'French Polynesia', 'Gabon', 'Gambia, The', 'Georgia', 'Germany', 'Ghana', 'Gibraltar', 'Greece', 'Greenland', 'Grenada', 'Guam', 'Guatemala', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Honduras', 'Hong Kong SAR, China', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran, Islamic Rep.', 'Iraq', 'Ireland', 'Isle of Man', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', 'Korea, Dem. People’s Rep.', 'Korea, Rep.', 'Kosovo', 'Kuwait', 'Kyrgyz Republic', 'Lao PDR', 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macao SAR, China', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Mauritania', 'Mauritius', 'Mexico', 'Micronesia, Fed. Sts.', 'Moldova', 'Monaco', 'Mongolia', 'Montenegro', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'New Caledonia', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'North Macedonia', 'Northern Mariana Islands', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Puerto Rico', 'Qatar', 'Romania', 'Russian Federation', 'Rwanda', 'Samoa', 'San Marino', 'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 'Sint Maarten (Dutch part)', 'Slovak Republic', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'South Sudan', 'Spain', 'Sri Lanka', 'St. Kitts and Nevis', 'St. Lucia', 'St. Martin (French part)', 'St. Vincent and the Grenadines', 'Sudan', 'Suriname', 'Sweden', 'Switzerland', 'Syrian Arab Republic', 'Tajikistan', 'Tanzania', 'Thailand', 'Timor-Leste', 'Togo', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Turks and Caicos Islands', 'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Venezuela, RB', 'Vietnam', 'Virgin Islands (U.S.)', 'West Bank and Gaza', 'Yemen, Rep.', 'Zambia', 'Zimbabwe']
    
    df_country = df[df['Country Name'] == country]
    latest_year = df_country['Year'].max()
    # print("df_country: ", df_country)
    # print(latest_year)
    
    country_population = int(df_country[df_country['Year'] == latest_year]['Value'].values[0])
    
    return country_population

# print(get_country_population("United States"))


def get_us_state_population(state):
    state = state.title()
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
    # ! header=None since there are no column labels in this csv file
    
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


def get_location_key(country, state):
    country_code = str(pycountry.countries.get(name=country).alpha_2)
    # print(country_code)
    
    country_subdivisions_list = list(pycountry.subdivisions.get(country_code=country_code))
    
    for i in range(len(country_subdivisions_list)):
        if (country_subdivisions_list[i].name == state):
            state_code = country_subdivisions_list[i].parent_code
            if (state_code == None):
                state_code = country_subdivisions_list[i].code
            state_code = state_code.replace('-', '_')
            # print(state_code)
            break
    
    # print(list(pycountry.subdivisions.get(country_code=country_code))[0].name)
    # print(list(pycountry.subdivisions.get(country_code=country_code)))
    
    return [country_code, state_code]

# print(get_location_key("Spain", "Madrid"))
# print(get_location_key("United States", "California"))

def get_state_and_country_covid_cases(country, state):
    location_key = get_location_key(country, state)
    country_key = location_key[0]
    state_key = location_key[1]
    # print(country_key)
    # print(state_key)
    
    date_range = 30
    date_range_timedelta = timedelta(days=(-date_range))
    
    # # Load CSV data directly from the URL with pandas, the options are needed to prevent
    # reading of records with key "NA" (Namibia) as NaN
    df = pd.read_csv('https://storage.googleapis.com/covid19-open-data/v3/epidemiology.csv', keep_default_na=False, na_values=[""])
    # print(df[df['key'] == 'US'])
    # print(df[df.location_key == 'US_CA'])
    # print(type(df.date.max()))
    
    df_country = df[df.location_key == country_key]
    country_last_date = df_country.date.max()
    country_last_date_date = (datetime.strptime(country_last_date, '%Y-%m-%d')).date()
    country_cases_start_date = country_last_date_date + date_range_timedelta
    
    current_country_cases_date = country_cases_start_date
    country_cases = 0.
    
    # print(df_country)
    # print("country_last_date", country_last_date)
    
    for i in range(date_range):
        # print("current_country_cases_date: ", current_country_cases_date)
        str_date = datetime.strftime(current_country_cases_date, '%Y-%m-%d')
        covid_cases = int(round(float(df_country[df_country.date == str_date]["new_confirmed"].values[0])))
        # print("covid_cases: ", covid_cases)
        country_cases += covid_cases
        current_country_cases_date += timedelta(days=1)
    
    country_cases = round(country_cases)
    # print(country_cases)
    
    # print(int(round(float(df_country[df_country.date == country_last_date]["new_confirmed"].values[0]))))
    
    
    df_state = df[df.location_key == state_key]
    state_last_date = df_state.date.max()
    state_last_date_date = (datetime.strptime(state_last_date, '%Y-%m-%d')).date()
    state_cases_start_date = state_last_date_date + date_range_timedelta
    
    current_state_cases_date = state_cases_start_date
    state_cases = 0.
    
    # print(df_state)
    # print("state_last_date", state_last_date)
    
    for i in range(date_range):
        # print("current_state_cases_date: ", current_state_cases_date)
        str_date = datetime.strftime(current_state_cases_date, '%Y-%m-%d')
        covid_cases = int(round(float(df_state[df_state.date == str_date]["new_confirmed"].values[0])))
        # print("covid_cases: ", covid_cases)
        state_cases += covid_cases
        current_state_cases_date += timedelta(days=1)
    
    state_cases = round(state_cases)
    # print(state_cases)
    
    return [country_cases, state_cases]

# print(get_state_and_country_covid_cases("United States", "California"))

def get_covid_case_stats(country, state):
    country_population = get_country_population(country)
    print("country_population: ", country_population)
    
    if (country == "United States"):
        state_population = get_us_state_population(state)
        print("state_population: ", state_population)
    
    covid_case_data = get_state_and_country_covid_cases(country, state)
    print("covid_case_data: ", covid_case_data)
    country_covid_cases = covid_case_data[0]
    state_covid_cases = covid_case_data[1]
    
    # from 0 to 100
    country_infected_percentage = round((country_covid_cases/country_population) * 100)
    
    if (country == "United States"):
        # from 0 to 100
        state_infected_percentage = round((state_covid_cases/state_population) * 100)
        
        return [country_covid_cases, country_population, country_infected_percentage, state_covid_cases, state_population, state_infected_percentage]
    else:
        return [country_covid_cases, country_population, country_infected_percentage, state_covid_cases]
    

# print(get_covid_case_stats("United States", "New York"))

# High: 7%+
# Medium: 4%+
# Low: 0%+