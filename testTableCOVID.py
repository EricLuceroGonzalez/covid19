import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from datetime import date, time, datetime

import os
import pathlib
thePath = str(pathlib.Path(__file__).parent.absolute())
theCSVPath = thePath + '/csv/'

today = date.today().strftime("%-m/%-d/%y")
todayDay = date.today().strftime("%-d")
todayMon = date.today().strftime("%-m")
todayTime = datetime.today().strftime("%d_%m_%y-%H:%M")

website_url = requests.get(
    'https://en.wikipedia.org/wiki/Template:COVID-19_testing').text
url = requests.get('https://www.worldometers.info/coronavirus/').text
soup = BeautifulSoup(url, 'html.parser')
# print(soup.prettify())

df = pd.DataFrame()

Country = []
TotalCases = []
NewCases = []
TotalDeaths = []
NewDeaths = []
TotalRecovered = []
ActiveCases = []
Critical = []
TotCasesPerM = []
DeathsPerM = []
TotalTests = []
TestsPerM = []

# Extrac by html class
my_table = soup.find(
    'table', {'id': 'main_table_countries_today'})  # Get the table
allTd = my_table.findAll('tr')
# print(allTd)
for i, aTD in enumerate(allTd):
    # print('\ni = {}'.format(i))
    if i == 0:
        a = aTD.find_next('td')
        print(a.contents[0])
        Country.append(a.contents[0])
    for j in aTD.findAll('strong'):
        print(j.contents[0])
        Country.append(j.contents[0])
    for j in aTD.findAll('span'):
        print(j.contents[0])
        Country.append(j.contents[0])
    for j in aTD.findAll('a'):
        Country.append(j.contents[0])
    for index, data in enumerate(aTD.findAll('td')):
        print('index = {}'.format(index))
        if index == 1 and len(data.contents) != 0:
            TotalCases.append(data.contents[0])
        if index == 2:  # and len(data.contents) != 0:
            if len(data.contents) == 0:
                NewCases.append(' ')
            if len(data.contents) != 0:
                NewCases.append(data.contents[0])
        if index == 3:
            if len(data.contents) == 0:
                TotalDeaths.append(' ')
            if len(data.contents) != 0:
                TotalDeaths.append(data.contents[0])
        if index == 4:
            if len(data.contents) == 0:
                NewDeaths.append(' ')
            if len(data.contents) != 0:
                NewDeaths.append(data.contents[0])
        if index == 5:
            if len(data.contents) == 0:
                TotalRecovered.append(' ')
            if len(data.contents) != 0:
                TotalRecovered.append(data.contents[0])
        if index == 6:
            if len(data.contents) == 0:
                ActiveCases.append(' ')
            if len(data.contents) != 0:
                ActiveCases.append(data.contents[0])
        if index == 7:
            if len(data.contents) == 0:
                Critical.append(' ')
            if len(data.contents) != 0:
                Critical.append(data.contents[0])
        if index == 8:
            if len(data.contents) == 0:
                TotCasesPerM.append(' ')
            if len(data.contents) != 0:
                TotCasesPerM.append(data.contents[0])
        if index == 9:
            if len(data.contents) == 0:
                DeathsPerM.append(' ')
            if len(data.contents) != 0:
                DeathsPerM.append(data.contents[0])
        if index == 10:
            if len(data.contents) == 0:
                TotalTests.append(' ')
            if len(data.contents) != 0:
                TotalTests.append(data.contents[0])
        if index == 11:
            if len(data.contents) == 0:
                TestsPerM.append(' ')
            if len(data.contents) != 0:
                TestsPerM.append(data.contents[0])

# Create the DataFrame:
df['Country'] = Country
df['Total Cases'] = TotalCases
df['New Cases'] = NewCases
df['Total Deaths'] = TotalCases
df['New Deaths'] = NewDeaths
df['Total Recovered'] = TotalRecovered
df['Active Cases'] = ActiveCases
df['Critical'] = Critical
df['Tot CasesPerM'] = TotCasesPerM
df['DeathsPerM'] = DeathsPerM
df['Total Tests'] = TotalTests
df['TestsPerM'] = TestsPerM
print(df)

# Save to CSV
data = df.to_csv(theCSVPath+todayTime+'-WorldometersData.csv')