import csv
import pandas as pd
import numpy as np
import json
import requests
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from datetime import date

today = date.today().strftime("%-m/%-d/%y")
todayDay = date.today().strftime("%-d")
todayMon = date.today().strftime("%-m")

# Data is obtained from CSSEGISandData
# https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv

def getData(update):
    if update:
        url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv'
        dataFromCSSE = pd.read_csv(url)
        # Save the data:
        dataCSV = dataFromCSSE.to_csv(
            '/home/ericlucero/Dropbox/Python_things/math/covidData/covidData-'+todayDay+'-'+todayMon+'.csv')
        data = pd.read_csv('/home/ericlucero/Dropbox/Python_things/math/covidData/covidData-' +
                           todayDay+'-'+todayMon+'.csv')
        return data
    else:
        data = pd.read_csv('/home/ericlucero/Dropbox/Python_things/math/covidData/covidData-' +
                           todayDay+'-'+todayMon+'.csv')
        return data

# # Bring the data:
data = getData(False) # True if want to update data to last push 

# Some important dates:
firstDate = '1/24/20'  # Start date on data
firstPanama = '3/10/20'  # First case in Panama
today = '3/20/20'

df = pd.DataFrame()
# Get dates data (Panama or any has the same)
dates = data.loc[data['Country/Region'] == 'Panama', firstDate: today].columns
df['Dates'] = dates

# Some countries to test
countrie = ['Panama', 'Peru', 'Mexico', 'Spain', 'Italy',
            'El Salvador', 'Iran', 'Costa Rica', 'Colombia']
countrie = ['Panama', 'Peru', 'Mexico', 'Costa Rica', 'Colombia',
            'El Salvador', 'Thailand', 'Sri Lanka', 'Finland', 'Chile', 'Vietnam']

# Countries to plot:
countrie = ['Panama', 'Costa Rica', 'Nicaragua', 'El Salvador', 'Guatemala',
            'Mexico', 'Honduras', 'Colombia', 'Chile', 'Argentina', 'Ecuador', 'Peru', 'Uruguay']

countries = []

for i, item in enumerate(countrie):
    space = item.split(' ')  # Find spaces on country name
    originalName = item
    if len(space) > 1:
        originalName = item
        item = space[0]+space[1]  # If not concatenate
    countries.append(item)


for indx, item in enumerate(countries):
    varName = item+'Data'
    arrName = 'data'+item
    varName = data.loc[data['Country/Region']
                       == countrie[indx], firstDate: today]
    arrName = varName.to_numpy()[0]
    df.insert(indx, item, arrName)

print('----------------------')
print(df)

dataDayZero = pd.DataFrame()
sinceZero = []

def getSinceFirseCase():
    for indx, place in enumerate(countries):
        aaa = df.index[df[place] > 0].tolist()
        print('Days with virus in {}: {}'.format(place, len(aaa)))
        dataSince0 = df[place].iloc[aaa]
        dateSince0 = df['Dates'].iloc[aaa]
        dfName = place + 'DataFrame'
        dfName = pd.DataFrame()
        dfName.insert(0, place, dataSince0)
        dfName.insert(1, 'Dates', dateSince0)
        sinceZero.append(dfName)
    return sinceZero


firstCaseArray = getSinceFirseCase()
for idx, item in enumerate(firstCaseArray):
    idx = 0
    arry = []
    for index in range(0, len(item)):
        arry.append(index+1)
    item.insert(0, 'Days', arry)
# Plot
    xCoord = item['Days'].iloc[-1]
    yCoord = item[item.columns[1]].iloc[-1]
    plt.plot(item['Days'], item[item.columns[1]], 'o-', label=item.columns[1]+ '('+str(yCoord)+')')
    plt.legend(loc='best')
    plt.text(xCoord, yCoord, yCoord)
    plt.xlabel('Days since first case')
    plt.ylabel('Numbers of cases')


plt.savefig('daysWithVirus.png', dpi=199)
plt.show()
