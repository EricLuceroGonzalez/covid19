# Data is obtained from CSSEGISandData
# https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv (deprecated)
# https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv (csv)

# https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv (actual)
# https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv (csv)


import csv
import pandas as pd
import numpy as np
import json
import requests
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import date, timedelta
from matplotlib.font_manager import FontProperties  # Smaller font
import test as covid
import os
import pathlib
thePath = str(pathlib.Path(__file__).parent.absolute())
theCSVPath = thePath + '/csv'

# today = date.today().strftime("%-m/%-d/%y")
today = (date.today() - timedelta(days=1)).strftime("%-m/%-d/%y")
yesterday = (date.today() - timedelta(days=1)).strftime("%-m/%-d/%y")
todayDay = date.today().strftime("%-d")
todayMon = date.today().strftime("%-m")


def getData(update):
    if update:
        url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
        dataFromCSSE = pd.read_csv(url)
        # Save the data:
        os.makedirs(theCSVPath, exist_ok=True)
        dataFromCSSE.to_csv(
            theCSVPath+'/'+todayDay+'-'+todayMon+'-Confirmed.csv')
        loadedData = pd.read_csv(theCSVPath+'/'+todayDay+'-'+todayMon+'-Confirmed.csv')
        return loadedData
    else:
        if not os.path.exists(theCSVPath+'/'+todayDay+'-'+todayMon+'-Confirmed.csv'):
            yesterdays = (date.today() - timedelta(days=1)).strftime("%-d")
            savedData = pd.read_csv(
                theCSVPath+'/'+yesterdays+'-'+todayMon+'-Confirmed.csv')
        else:
            savedData = pd.read_csv(
                theCSVPath+'/'+todayDay+'-'+todayMon+'-Confirmed.csv')
    return savedData


#     # # Bring the data:
data = getData(False)  # True if want to update data to last push

# Some important dates:
firstDate = '1/24/20'  # Start date on data
firstPanama = '3/10/20'  # First case in Panama
# today = '3/22/20'


# Some countries to test
countrie = ['Panama', 'Peru', 'Mexico', 'Spain', 'Italy',
            'El Salvador', 'Iran', 'Costa Rica', 'Colombia']
countrie = ['Panama', 'Peru', 'Mexico', 'Costa Rica', 'Colombia',
            'El Salvador', 'Thailand', 'Sri Lanka', 'Finland', 'Chile', 'Vietnam']

# Countries to plot:
latinAmerica = ['Panama', 'Uruguay', 'Costa Rica', 'Nicaragua', 'El Salvador', 'Guatemala',
           'Mexico', 'Honduras', 'Colombia', 'Chile', 'Argentina', 'Ecuador', 'Peru', 'Venezuela']

# Generate the DataFrame from CSSEGISandData data
dff, places = covid.caseVSday(
    countries=latinAmerica, data=data, startDate=firstDate, finalDate=today, printIt=False)

# country = ['Panama']
# # country = ['Panama']
# firstCaseArray = covid.getSinceFirseCase(countries=country, dataFrame=dff)
# # covid.plotSinceFirstCaseBar(firstCaseArray, True, todayDay, todayMon)

# firstCaseArray = covid.getSinceFirseCase(countries=['Panama', 'Uruguay'], dataFrame=dff)
# covid.plotSinceFirstCase(firstCaseArray, False, todayDay, todayMon)
# print(firstCaseArray)
# print(dff['Panama'])
# ['Panama'])

theArray = covid.getSinceFirseCase(countries=['Panama', 'Uruguay'], dataFrame=dff)
covid.daysWithCases(fromZeroArray=theArray, dataFrame=dff)

