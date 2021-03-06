import requests
from bs4 import BeautifulSoup
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import test as covid
# from fastnumbers import fast_float
from datetime import date, time, datetime

import os
import pathlib
thePath = str(pathlib.Path(__file__).parent.absolute())
theCSVPath = thePath + '/csv/worldometersData/'
thePlotPath = str(pathlib.Path(__file__).parent.absolute()) + '/plots/'

today = date.today().strftime("%-m/%-d/%y")
todayDay = date.today().strftime("%-d")
todayMon = date.today().strftime("%-m")
todayTime = datetime.today().strftime("%d_%m_%y-%H:%M")


def getWorldometerData(Getit):
    if Getit == True:
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
            if i > 8:
                print('\ni = {}'.format(i))
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
                    if index == 1:
                        if len(data.contents) == 0:
                            NewCases.append(' ')
                        if len(data.contents) != 0:
                            s = data.contents[0]
                            dat = s.replace(',', '')
                            TotalCases.append(float(dat))
                    if index == 2:
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
                            s = data.contents[0]
                            dat = s.replace(',', '')
                            TotCasesPerM.append(float(dat))
                    if index == 9:
                        if len(data.contents) == 0:
                            DeathsPerM.append(' ')
                        if len(data.contents) != 0:
                            s = data.contents[0]
                            dat = s.replace(',', '')
                            DeathsPerM.append(float(dat))
                    if index == 10:
                        if len(data.contents) == 0:
                            TotalTests.append(' ')
                        if len(data.contents) != 0:
                            s = data.contents[0]
                            dat = float(s.replace(',', ''))
                            TotalTests.append(dat)
                    if index == 11:
                        if len(data.contents) == 0:
                            TestsPerM.append(' ')
                        if len(data.contents) != 0:
                            s = data.contents[0]
                            dat = float(s.replace(',', ''))
                            print(type(s))
                            print(type(dat))
                            TestsPerM.append(dat)

        print(Country)
        print(TotalCases)
        print(TotCasesPerM)
        print(len(Country))
        print(len(TotalCases))
        print(len(TotCasesPerM))
        # Create the DataFrame:
        df['Country'] = Country
        df['Total Cases'] = TotalCases
        df['New Cases'] = NewCases
        df['Total Deaths'] = TotalDeaths
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
        return df


# Generate new CSV?
data = getWorldometerData(True)
print(data)
# Open some CSV
csvData = pd.read_csv(
    theCSVPath+'10_04_20-19:06-WorldometersData.csv', sep=",")

print(csvData.loc[[40]])
print('*************')
# print(csvData.loc[[1]])

# data = ['Panama', 'USA', 'Mexico']
dat1 = ['Argentina', 'Ecuador', 'Peru',
        'El Salvador', 'Nicaragua', 'Cuba',
        'Guatemala', 'Costa Rica', 'Honduras',
        'Mexico'        # , 'Venezuela'
        , 'Colombia',
        'Brazil',
        'Haiti',
        'Bolivia',
        'Jamaica',
        'Paraguay',
        'Trinidad and Tobago',
        'Belize', 'Panama', 'Uruguay', 'Chile'
        ]

dat2 = ['Panama', 'Chile', 'Italy', 'Spain', 'Switzerland', 'Netherlands', 'Iran',
        'Germany', 'USA', 'UK', 'France', 'Belgium']
dat3 = [
    'Turkey',
    'Sweden',
    'Russia',
    'Finland',
    'Ireland',
    'New Zealand',
    'Canada',
    'S. Korea',
    'Denmark',
    'Singapore',
    'Portugal',
    'Australia',
    'Slovenia',
    'Qatar',
    'Estonia',
    'Switzerland',
    'Isle of Man',
    'Brunei ',
    'Norway',
    'Liechtenstein',
    'Malta',
    'Bahrain'    # ,'UAE'
    , 'Panama'
]
# 'Luxembourg',
# 'Andorra',
# 'San Marino',
# 'Gibraltar']


dat4 = [
    'USA',
'Spain',
'Italy',
'France',
'Germany',
'UK',
'Iran',
'Turkey',
'Belgium',
'Switzerland',
'Netherlands',
'Canada',
'Brazil',
'Portugal',
'Austria',
'Russia',
'Israel',
'S. Korea',
'Sweden',
'Ireland',
'India',
'Ecuador',
'Chile',
'Peru',
'Norway',
'Poland',
'Australia',
'Japan',
'Denmark',
'Romania',
'Czechia',
'Pakistan',
'Malaysia',
'Philippines',
'Saudi Arabia',
'Mexico',
'Indonesia',
'UAE',
'Serbia',
'Luxembourg',
'Panama'
]


# someDf = covid.scatterPlotCountries(csvData, dat1+dat3+dat2, 'Panama')
# s = covid.perMillionPlots(someDf, 'World')

# someDf = covid.scatterPlotCountries(csvData, dat3, 'Europe')
# s = covid.perMillionPlots(someDf, 'Europe')
# someDf = covid.scatterPlotCountries(csvData, dat1, 'Latinamerica')
# s = covid.perMillionPlots(someDf, 'Latin America')
# print(someDf)
# s = covid.perMillionPlots(someDf, 'Latin America')

someDf = covid.scatterPlotCountries(csvData, dat4, 'Top 40')
s = covid.perMillionPlots(someDf, 'Top 40')
# print(someDf)