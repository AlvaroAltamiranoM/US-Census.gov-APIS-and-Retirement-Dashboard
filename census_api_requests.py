# -*- coding: utf-8 -*-
"""
Created on Fri Jun 24 09:48:30 2022

@author: unily
"""

import pandas as pd
import requests
from functools import reduce

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
# invert the dictionary
abbrev_to_us_state = dict(map(reversed, us_state_to_abbrev.items()))

def json_to_dataframe(response):
    """
    Convert response to dataframe
    """
    return pd.DataFrame(response.json()[1:], columns=response.json()[0])

'''
#2019
#County level population
# 65+ & 85+
url_c1="https://api.census.gov/data/2019/pep/charagegroups?get=NAME,SEX,POP&AGEGROUP=27,26,0&for=county:*&key="
response_c1 = requests.request("GET", url_c1)
df_c = json_to_dataframe(response_c1)
df_c['fips'] = df_c['state'] + df_c['county']
df_c = df_c[df_c['state']!="72"]

df_c = df_c.pivot(index='NAME', columns='AGEGROUP', values=['POP','fips'])
df_c = df_c.iloc[:, 0:4]
df_c.columns = df_c.columns.droplevel(0)
df_c.columns = ['0', '26', '27', 'fips']

df_c["26"] = df_c["26"].astype(int)
df_c["0"] = df_c["0"].astype(int)
df_c["27"] = df_c["27"].astype(int)
df_c['%65+'] = (df_c['26']/df_c['0'])*100
df_c['%85+'] = (df_c['27']/df_c['0'])*100
df_c['county']  = df_c.index
df_c = df_c.drop(['0'], 1)

df_c.to_csv('pop_county.csv')
'''

'''
#2010
#County level population
# 65+ & 85+
url_c1_2010="https://api.census.gov/data/2000/pep/int_charagegroups?get=GEONAME,POP,DATE_DESC,AGEGROUP&for=state:*&DATE_=12&key=a190abb85e44d5290382038b4c388f9046dd3e32"
response_c1_2010 = requests.request("GET", url_c1_2010)
df_c_2010 = json_to_dataframe(response_c1_2010)
df_c_2010['fips'] = df_c_2010['state'] + df_c_2010['county']
df_c_2010 = df_c_2010[df_c_2010['state']!="72"]
df_c = df_c.pivot(index='NAME', columns='AGEGROUP', values=['POP','fips'])
df_c = df_c.iloc[:, 0:4]
df_c.columns = df_c.columns.droplevel(0)
df_c.columns = ['0', '26', '27', 'fips']
df_c["26"] = df_c["26"].astype(int)
df_c["0"] = df_c["0"].astype(int)
df_c["27"] = df_c["27"].astype(int)
df_c['%65+'] = (df_c['26']/df_c['0'])*100
df_c['%85+'] = (df_c['27']/df_c['0'])*100
df_c['county']  = df_c.index
df_c = df_c.drop(['0'], 1)
df_c.to_csv('pop_county.csv')
'''

#State level population
# 65+ & 85+
url_s1 =   "https://api.census.gov/data/2019/acs/acs1/subject?get=group(S0101)&for=state:*&key=a190abb85e44d5290382038b4c388f9046dd3e32"
response_s1 = requests.request("GET", url_s1)
df_s = json_to_dataframe(response_s1)
df_s = df_s[['NAME','S0101_C01_001E', 'S0101_C01_030E','S0101_C02_030E', 'S0101_C01_019E']]
cols = df_s.columns.drop('NAME')
df_s[cols] = df_s[cols].apply(pd.to_numeric, errors='coerce')

df_s["26"] = df_s["S0101_C01_030E"].astype(int)
df_s["0"] = df_s["S0101_C01_001E"].astype(int)
df_s["27"] = df_s["S0101_C01_019E"].astype(int)
df_s['%65+'] = (df_s['26']/df_s['0'])*100
df_s['%85+'] = (df_s['27']/df_s['0'])*100
df_s['states']  = df_s.NAME
df_s['states']  = df_s.states.replace(us_state_to_abbrev, regex=False)
df_s = df_s.drop(['S0101_C01_001E', 'S0101_C01_030E','S0101_C02_030E', 'S0101_C01_019E'], 1)
df_s = df_s[df_s['states']!="PR"]
cols = df_s.columns.drop(['NAME','states'])
df_s[cols] = df_s[cols].round(1)
df_s.to_csv('pop_states.csv', index=False)

#State level population BY SEX
# 65+ & 85+
url_s1_sex =   "https://api.census.gov/data/2019/acs/acs1/subject?get=group(S0101)&for=state:*&key=a190abb85e44d5290382038b4c388f9046dd3e32"
response_s1_sex = requests.request("GET", url_s1_sex)
df_s_sex = json_to_dataframe(response_s1_sex)
    # MEN
df_s_men = df_s_sex[['NAME','S0101_C04_030E', 'S0101_C03_001E','S0101_C03_019E']]
cols = df_s_men.columns.drop('NAME')
df_s_men[cols] = df_s_men[cols].apply(pd.to_numeric, errors='coerce')
df_s_men["0"] = df_s_men["S0101_C03_001E"].astype(int)
df_s_men["27"] = df_s_men["S0101_C03_019E"].astype(int)
df_s_men['%65+'] = df_s_men['S0101_C04_030E']
df_s_men["26"] = ((df_s_men['%65+']/100) * df_s_men["0"]).astype(int)
df_s_men['%85+'] = (df_s_men['27']/df_s_men['0'])*100
df_s_men['states']  = df_s_men.NAME
df_s_men['states']  = df_s_men.states.replace(us_state_to_abbrev, regex=False)
df_s_men = df_s_men.drop(['S0101_C04_030E', 'S0101_C03_001E','S0101_C03_019E'], 1)
df_s_men = df_s_men[df_s_men['states']!=48]
cols = df_s_men.columns.drop(['NAME','states'])
df_s_men[cols] = df_s_men[cols].round(1)
df_s_men.to_csv('pop_states_sex_men.csv', index=False)

    # WOMEN
df_s_women = df_s_sex[['NAME', 'S0101_C06_030E','S0101_C05_001E','S0101_C05_019E']]
cols = df_s_women.columns.drop('NAME')
df_s_women[cols] = df_s_women[cols].apply(pd.to_numeric, errors='coerce')
df_s_women["0"] = df_s_women["S0101_C05_001E"].astype(int)
df_s_women["27"] = df_s_women["S0101_C05_019E"].astype(int)
df_s_women['%65+'] = df_s_women['S0101_C06_030E']
df_s_women["26"] = ((df_s_women['%65+']/100) * df_s_women["0"]).astype(int)
df_s_women['%85+'] = (df_s_women['27']/df_s_women['0'])*100
df_s_women['states']  = df_s_women.NAME
df_s_women['states']  = df_s_women.states.replace(us_state_to_abbrev, regex=False)
df_s_women = df_s_women.drop(['S0101_C06_030E','S0101_C05_001E','S0101_C05_019E'], 1)
df_s_women = df_s_women[df_s_women['states']!=48]
cols = df_s_women.columns.drop(['NAME','states'])
df_s_women[cols] = df_s_women[cols].round(1)
df_s_women.to_csv('pop_states_sex_women.csv', index=False)


#State level population BY RACE
# 65+ & 85+
url_s1_race =   "https://api.census.gov/data/2019/acs/acs1/subject?get=group(S0103)&for=state:*&key=a190abb85e44d5290382038b4c388f9046dd3e32"
response_s1_race = requests.request("GET", url_s1_race)
df_s_race = json_to_dataframe(response_s1_race)
    # MEN
df_s_race = df_s_race[['NAME','S0103_C01_006E','S0103_C01_007E','S0103_C01_009E','S0103_C01_013E']]
df_s_race = df_s_race[df_s_race['NAME']!='Puerto Rico']

'''
#Poverty, County level
# 65+
url_p_65_c=   "https://api.census.gov/data/2020/acs/acs5/subject?get=NAME,S1701_C01_010E,S1701_C02_010E&for=county:*&key=a190abb85e44d5290382038b4c388f9046dd3e32"
response = requests.request("GET", url_p_65_c)
df_p_65_c = json_to_dataframe(response)
df_p_65_c["POP"] = df_p_65_c["S1701_C01_010E"].astype(int)
df_p_65_c["Below_poverty"] = df_p_65_c["S1701_C02_010E"].astype(int)
df_p_65_c['Percent_Poor'] = (df_p_65_c.Below_poverty/df_p_65_c.POP)*100
df_p_65_c = df_p_65_c[df_p_65_c['state']!="72"]
df_p_65_c['fips'] = df_p_65_c.state + df_p_65_c.county
df_p_65_c = df_p_65_c.drop(['S1701_C01_010E', 'S1701_C02_010E','state','county'], 1)
df_p_65_c.to_csv('poverty_county.csv')
'''
#Poverty, State level
# 65+
url_p_65 =   "https://api.census.gov/data/2019/acs/acs1/subject?get=NAME,S1701_C03_011EA,S1701_C01_010E,S1701_C02_010E&for=state:*&key=a190abb85e44d5290382038b4c388f9046dd3e32"
response = requests.request("GET", url_p_65)
df_p_65_s = json_to_dataframe(response)
df_p_65_s["POP"] = df_p_65_s["S1701_C01_010E"].astype(int)
df_p_65_s["Below_poverty"] = df_p_65_s["S1701_C02_010E"].astype(int)
df_p_65_s['Percent_Poor'] = (df_p_65_s.Below_poverty/df_p_65_s.POP)*100
df_p_65_s['states']  = df_p_65_s.NAME.replace(us_state_to_abbrev, regex=False)
df_p_65_s = df_p_65_s[df_p_65_s['state']!="72"]
df_p_65_s = df_p_65_s.drop(['S1701_C01_010E', 'S1701_C02_010E','state'], 1)

cols = df_p_65_s.columns.drop(['NAME','states'])
df_p_65_s[cols] = df_p_65_s[cols].round(1)

df_p_65_s.to_csv('poverty_state.csv', index=False)

#Poverty, State level BY SEX
# 65+
    # MEN
url_p_65_sex_men =   "https://api.census.gov/data/2019/acs/acs1?get=NAME,B17001_015E,B17001_016E,B17001_044E,B17001_045E&for=state:*&key=a190abb85e44d5290382038b4c388f9046dd3e32"
response_p_sex_men = requests.request("GET", url_p_65_sex_men)
df_p_65_s_sex_men = json_to_dataframe(response_p_sex_men)
 # pop values to numeric
cols = df_p_65_s_sex_men.columns.drop('NAME')
df_p_65_s_sex_men[cols] = df_p_65_s_sex_men[cols].apply(pd.to_numeric, errors='coerce')
df_p_65_s_sex_men["POP"] = df_p_65_s_sex_men.iloc[:,1:5].sum(axis=1) # add pop groups
df_p_65_s_sex_men["Below_poverty"] = df_p_65_s_sex_men["B17001_015E"] + df_p_65_s_sex_men["B17001_016E"]
df_p_65_s_sex_men['Percent_Poor'] = (df_p_65_s_sex_men.Below_poverty/df_p_65_s_sex_men.POP)*100
df_p_65_s_sex_men['states']  = df_p_65_s_sex_men.NAME.replace(us_state_to_abbrev, regex=False)
df_p_65_s_sex_men = df_p_65_s_sex_men[df_p_65_s_sex_men['state']!=72]
df_p_65_s_sex_men = df_p_65_s_sex_men.drop(['B17001_015E','B17001_016E','B17001_044E','B17001_045E','state'], 1)

cols = df_p_65_s_sex_men.columns.drop(['NAME','states'])
df_p_65_s_sex_men[cols] = df_p_65_s_sex_men[cols].round(1)
df_p_65_s_sex_men.to_csv('poverty_state_men.csv', index=False)

    # WOMEN
url_p_65_sex_women =   "https://api.census.gov/data/2019/acs/acs1?get=NAME,B17001_029E,B17001_030E,B17001_058E,B17001_059E&for=state:*&key=a190abb85e44d5290382038b4c388f9046dd3e32"
response_p_sex_women = requests.request("GET", url_p_65_sex_women)
df_p_65_s_sex_women = json_to_dataframe(response_p_sex_women)
 # pop values to numeric
cols = df_p_65_s_sex_women.columns.drop('NAME')
df_p_65_s_sex_women[cols] = df_p_65_s_sex_women[cols].apply(pd.to_numeric, errors='coerce')
df_p_65_s_sex_women["POP"] = df_p_65_s_sex_women.iloc[:,1:5].sum(axis=1) # add pop groups
df_p_65_s_sex_women["Below_poverty"] = df_p_65_s_sex_women["B17001_029E"] + df_p_65_s_sex_women["B17001_030E"]
df_p_65_s_sex_women['Percent_Poor'] = (df_p_65_s_sex_women.Below_poverty/df_p_65_s_sex_women.POP)*100
df_p_65_s_sex_women['states']  = df_p_65_s_sex_women.NAME.replace(us_state_to_abbrev, regex=False)
df_p_65_s_sex_women = df_p_65_s_sex_women[df_p_65_s_sex_women['state']!=72]
df_p_65_s_sex_women = df_p_65_s_sex_women.drop(['B17001_029E','B17001_030E','B17001_058E','B17001_059E','state'], 1)

cols = df_p_65_s_sex_women.columns.drop(['NAME','states'])
df_p_65_s_sex_women[cols] = df_p_65_s_sex_women[cols].round(1)
df_p_65_s_sex_women.to_csv('poverty_state_women.csv', index=False)

#Employment/Population ratio, State level
# 65 to 74 years
url_emp_65_74_75 = "https://api.census.gov/data/2019/acs/acs1/subject?get=NAME,S2301_C03_010E,S2301_C03_011E&for=state:*&key=a190abb85e44d5290382038b4c388f9046dd3e32"
response = requests.request("GET", url_emp_65_74_75)
df_emp_65_s = json_to_dataframe(response)
df_emp_65_s["Employed_65_74"] = df_emp_65_s["S2301_C03_010E"].astype(float)
df_emp_65_s["Employed_75+"] = df_emp_65_s["S2301_C03_011E"].astype(float)
df_emp_65_s['states']  = df_emp_65_s.NAME.replace(us_state_to_abbrev, regex=False)
df_emp_65_s = df_emp_65_s.drop(['S2301_C03_010E', 'S2301_C03_011E','state'], 1)
df_emp_65_s = df_emp_65_s[df_emp_65_s['states']!="PR"]

cols = df_emp_65_s.columns.drop(['NAME','states'])
df_emp_65_s[cols] = df_emp_65_s[cols].round(1)
df_emp_65_s.to_csv('emp_state.csv', index=False)

#Employment/Population ratio, State level BY SEX
# 65 to 74 years
    # MEN
url_emp_65_74_75_sex_men =   "https://api.census.gov/data/2019/acs/acs1?get=NAME,B23001_073E,B23001_075E,B23001_078E,B23001_080E,B23001_083E,B23001_085E&for=state:*&key=a190abb85e44d5290382038b4c388f9046dd3e32"
response_emp_65_74_75_sex_men = requests.request("GET", url_emp_65_74_75_sex_men)
df_emp_65_74_75_sex_men = json_to_dataframe(response_emp_65_74_75_sex_men)
 # pop values to numeric
cols = df_emp_65_74_75_sex_men.columns.drop('NAME')
df_emp_65_74_75_sex_men[cols] = df_emp_65_74_75_sex_men[cols].apply(pd.to_numeric, errors='coerce')
df_emp_65_74_75_sex_men["Employed_65_74"] = ((df_emp_65_74_75_sex_men["B23001_075E"] + df_emp_65_74_75_sex_men["B23001_080E"] ) / (df_emp_65_74_75_sex_men["B23001_073E"] + df_emp_65_74_75_sex_men["B23001_078E"] ))*100
df_emp_65_74_75_sex_men["Employed_75+"] = (df_emp_65_74_75_sex_men["B23001_085E"] / df_emp_65_74_75_sex_men["B23001_083E"])*100
df_emp_65_74_75_sex_men['states']  = df_emp_65_74_75_sex_men.NAME.replace(us_state_to_abbrev, regex=False)
df_emp_65_74_75_sex_men = df_emp_65_74_75_sex_men.drop(['B23001_073E', 'B23001_075E', 'B23001_078E', 'B23001_080E',
       'B23001_083E', 'B23001_085E','state'], 1)
df_emp_65_74_75_sex_men = df_emp_65_74_75_sex_men[df_emp_65_74_75_sex_men['states']!="PR"]

cols = df_emp_65_74_75_sex_men.columns.drop(['NAME','states'])
df_emp_65_74_75_sex_men[cols] = df_emp_65_74_75_sex_men[cols].round(1)

df_emp_65_74_75_sex_men.to_csv('emp_state_men.csv', index=False)

    # WOMEN
url_emp_65_74_75_sex_women =   "https://api.census.gov/data/2019/acs/acs1?get=NAME,B23001_159E,B23001_161E,B23001_164E,B23001_166E,B23001_169E,B23001_171E&for=state:*&key=a190abb85e44d5290382038b4c388f9046dd3e32"
response_emp_65_74_75_sex_women = requests.request("GET", url_emp_65_74_75_sex_women)
df_emp_65_74_75_sex_women = json_to_dataframe(response_emp_65_74_75_sex_women)
 # pop values to numeric
cols = df_emp_65_74_75_sex_women.columns.drop('NAME')
df_emp_65_74_75_sex_women[cols] = df_emp_65_74_75_sex_women[cols].apply(pd.to_numeric, errors='coerce')
df_emp_65_74_75_sex_women["Employed_65_74"] = ((df_emp_65_74_75_sex_women["B23001_161E"] + df_emp_65_74_75_sex_women["B23001_166E"] ) / (df_emp_65_74_75_sex_women["B23001_159E"] + df_emp_65_74_75_sex_women["B23001_164E"] ))*100
df_emp_65_74_75_sex_women["Employed_75+"] = (df_emp_65_74_75_sex_women["B23001_171E"] / df_emp_65_74_75_sex_women["B23001_169E"])*100
df_emp_65_74_75_sex_women['states']  = df_emp_65_74_75_sex_women.NAME.replace(us_state_to_abbrev, regex=False)
df_emp_65_74_75_sex_women = df_emp_65_74_75_sex_women.drop(['B23001_159E', 'B23001_161E', 'B23001_164E', 'B23001_166E',
       'B23001_169E', 'B23001_171E','state'], 1)
df_emp_65_74_75_sex_women = df_emp_65_74_75_sex_women[df_emp_65_74_75_sex_women['states']!="PR"]

cols = df_emp_65_74_75_sex_women.columns.drop(['NAME','states'])
df_emp_65_74_75_sex_women[cols] = df_emp_65_74_75_sex_women[cols].round(1)

df_emp_65_74_75_sex_women.to_csv('emp_state_women.csv', index=False)

'''
# 65 to 74 years
url_emp_65_74_75_c =   "https://api.census.gov/data/2020/acs/acs5/subject?get=NAME,S2301_C03_010E,S2301_C03_011E&for=county:*&key=a190abb85e44d5290382038b4c388f9046dd3e32"
response = requests.request("GET", url_emp_65_74_75_c)
df_emp_65_c = json_to_dataframe(response)
df_emp_65_c["Employed_65_74"] = df_emp_65_c["S2301_C03_010E"].astype(float)
df_emp_65_c["Employed_75+"] = df_emp_65_c["S2301_C03_011E"].astype(float)
df_emp_65_c = df_emp_65_c[df_emp_65_c['state']!="72"]
df_emp_65_c['fips'] = df_emp_65_c.state + df_emp_65_c.county
df_emp_65_c = df_emp_65_c.drop(['S2301_C03_010E', 'S2301_C03_011E','state','county'], 1)
df_emp_65_c.to_csv('emp_county.csv')
'''
#Households with retirement income, State level
# 60+
url_ret =   "https://api.census.gov/data/2019/acs/acs1/subject?get=NAME,S0102_C02_083E,S0102_C02_077E&for=state:*&key=a190abb85e44d5290382038b4c388f9046dd3e32"
response = requests.request("GET", url_ret)
df_ret_s = json_to_dataframe(response)
df_ret_s["Retirement_income"] = df_ret_s["S0102_C02_083E"].astype(float)
df_ret_s["Social_security"] = df_ret_s["S0102_C02_077E"].astype(float)
df_ret_s['states']  = df_ret_s.NAME.replace(us_state_to_abbrev, regex=False)
df_ret_s = df_ret_s.drop(['S0102_C02_083E', 'S0102_C02_077E','state'], 1)
df_ret_s = df_ret_s[df_ret_s['states']!="PR"]

cols = df_ret_s.columns.drop(['NAME','states'])
df_ret_s[cols] = df_ret_s[cols].round(1)

df_ret_s.to_csv('retir_state.csv', index=False)

'''
#Households with retirement income, County level
# 60+
url_ret_c =   "https://api.census.gov/data/2020/acs/acs5/subject?get=NAME,S0102_C02_083E,S0102_C02_077E&for=county:*&key=a190abb85e44d5290382038b4c388f9046dd3e32"
response = requests.request("GET", url_ret_c)
df_ret_c = json_to_dataframe(response)
df_ret_c["Retirement_income"] = df_ret_c["S0102_C02_083E"].astype(float)
df_ret_c["Social_security"] = df_ret_c["S0102_C02_077E"].astype(float)
df_ret_c = df_ret_c[df_ret_c['state']!="72"]
df_ret_c['fips'] = df_ret_c.state + df_ret_c.county
df_ret_c = df_ret_c.drop(['S0102_C02_083E', 'S0102_C02_077E','state'], 1)
df_ret_c.to_csv('retir_county.csv')

#Agregating county level indicators
data_frames_c = [df_c, df_emp_65_c, df_p_65_c, df_ret_c]
df_merged_c = reduce(lambda  left,right: pd.merge(left,right,on=['fips'],                                            how='outer'), data_frames_c)
df_table_c = df_merged_c[['NAME','26','27','%65+','%85+','Below_poverty','Percent_Poor',
                          'Employed_65_74','Employed_75+','Retirement_income','Social_security']]
df_table_c.columns = ['County', 'Population 65+', 'Population 85+', 'Share of population 65+ (%)',
                      'Share of population 85+ (%)','People 65+ living below poverty',
                      'People 65+ living below poverty (%)', 'Employment at 65-74 (%)',
                      'Employment at 75+ (%)','People 60+ with retirement income (%)',
                      'People 60+ with social security income (%)']
df_table_c.to_csv('table_county.csv')
'''

#Agregating state level indicators
data_frames_s = [df_s, df_emp_65_s, df_p_65_s, df_ret_s]
df_merged_s = reduce(lambda  left,right: pd.merge(left,right,on=['states'],
                                            how='outer'), data_frames_s)

df_table_s = df_merged_s[['NAME_y','26','27','%65+','%85+','Below_poverty','Percent_Poor',
                          'Employed_65_74','Employed_75+','Retirement_income','Social_security']]

df_table_s = df_table_s.drop[['NAME_y']]
df_table_s = df_table_s.iloc[:, 1:]


df_table_s.columns = ['Name_y', 'Population 65+', 'Population 85+', 'Share of population 65+ (%)',
                      'Share of population 85+ (%)','People 65+ living below poverty',
                      'People 65+ living below poverty (%)', 'Employment at 65-74 (%)',
                      'Employment at 75+ (%)','People 60+ with retirement income (%)',
                      'People 60+ with social security income (%)']


precision = 1
df_table_s['Share of population 65+ (%)'] = df_table_s['Share of population 65+ (%)'].round(decimals = precision)
df_table_s['Share of population 85+ (%)'] = df_table_s['Share of population 85+ (%)'].round(decimals = precision)
df_table_s['People 65+ living below poverty (%)'] = df_table_s['People 65+ living below poverty (%)'].round(decimals = precision)
df_table_s.to_csv('table_state.csv', index=False)
