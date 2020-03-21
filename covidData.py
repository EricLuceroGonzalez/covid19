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


# Bring the data:
data = getData(False)

# Some important dates:
firstDate = '1/24/20'  # Start date on data
firstPanama = '3/10/20'  # First case in Panama
today = '3/20/20'

df = pd.DataFrame()
# Get dates data (Panama or any has the same)
dates = data.loc[data['Country/Region'] == 'Panama', firstDate: today].columns
df['Dates'] = dates

countrie = ['Panama', 'Peru', 'Mexico', 'Spain', 'Italy',
            'El Salvador', 'Iran', 'Costa Rica', 'Colombia']
countrie = ['Panama', 'Peru']            
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
    print(arrName)
    varName = data.loc[data['Country/Region']
                       == countrie[indx], firstDate: today]
    arrName = varName.to_numpy()[0]
    df.insert(indx, item, arrName)

print('----------------------')
print(df)


# # Find the date of first covid case:
# nonCasesDays = df['Panama'].loc[df['Panama'] == 0]
# yesCasesDays = df['Panama'].loc[df['Panama'] != 0]
# panNZdays = len(nonCasesDays)
# panYZdays = len(yesCasesDays)
# print('{} days with virus cases [Panama]'.format(panYZdays))
# print('{} days without virus in [Panama]'.format(panNZdays))
# # print(yzd)
# # print(nzd)

dataDayZero = pd.DataFrame()
sinceZero = []


def getSinceFirseCase():
    for indx, place in enumerate(countries):
        # print('\n -----------------------------------------------')
        aaa = df.index[df[place] > 0].tolist()
        print('Days with virus in {}: {}'.format(place, len(aaa)))
        dataSince0 = df[place].iloc[aaa]
        dateSince0 = df['Dates'].iloc[aaa]
        # print('dataSince0')
        print(dataSince0)
        # print('dateSince0')
        # print(dateSince0.tolist())
        print('***********************************')
        dfName = place + 'DataFrame'
        # print(dfName)
        dfName = pd.DataFrame()
        # print(indx)
        # print(place)
        dfName.insert(0, place, dataSince0)
        dfName.insert(1, 'Dates', dateSince0)
        sinceZero.append(dfName)
    return sinceZero


aaaa = getSinceFirseCase()
print(aaaa)
print(len(aaaa))
for idx, item in enumerate(aaaa):
    print(item)
    print(item[countries[idx]])
    print(item['Dates'])

# dayZeroSpain = getSinceFirseCase( 'Spain')
# dayZeroColombia = getSinceFirseCase('Colombia')
# dayZeroItaly = getSinceFirseCase( 'Italy')
# print(dayZeroColombia)

# # # # Plot
# # # plt.plot(dayZeroPanama['Dates'], dayZeroPanama['Cases'], 'o-', color='blue')
# # plt.plot(dayZeroSpain['Dates'], dayZeroSpain['Spain'], 'o-', color='magenta')
# # plt.plot(dayZeroItaly['Dates'], dayZeroItaly['Italy'], 'o-', color='red')
# # plt.gcf().autofmt_xdate()
# # plt.show()


# # # plt.plot(dayZeroColombia['Dates'],dayZeroColombia['Cases'], 'o-', color='green')


# Geb_b30 = [11, 10, 12, 14, 16, 19, 17, 14, 18, 17]
# Geb_a30 = [12, 10, 13, 14, 12, 13, 18, 16]

# years = list(range(2008,2018))

# print(years[0:len(Geb_b30)])
# print(years[2:])

# fig, ax = plt.subplots()
# ax.plot(years[0:len(Geb_b30)],Geb_b30, label='Prices 2008-2018',
# color='blue')
# ax.plot(years[2:],Geb_a30, label='Prices 2010-2018', color =
# 'red')
# legend = ax.legend(loc='center right', fontsize='x-large')
# plt.xlabel('years')
# plt.ylabel('prices')
# plt.title('Comparison of the different prices')
# plt.show()
