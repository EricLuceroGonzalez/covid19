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
        loadedData = pd.read_csv(
            theCSVPath+'/'+todayDay+'-'+todayMon+'-Confirmed.csv')
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

# Countries to plot:
CentralAmerica = ['Panama', 'El Salvador', 'Nicaragua',
                  'Guatemala', 'Costa Rica', 'Honduras', 'Mexico']
#
# CentralAmerica = ['Panama']                  
suramerica = ['Venezuela', 'Uruguay', 'Colombia',
              'Chile', 'Argentina', 'Ecuador', 'Peru', 'Brazil']
latinAmerica = []
latinAmerica = CentralAmerica + suramerica

# Generate the DataFrame from CSSEGISandData data (1):


def runTodayPlots(listCountries, condition, savePlot):
    dff, places = covid.caseVSday(
        countries=listCountries, data=data, startDate=firstDate, finalDate=today, printIt=False)
    if condition:
        covid.plotSinceFirstCase(countries=listCountries, dataFrame=dff,
                                 saveIt=savePlot, todayDay=todayDay, todayMon=todayMon)
        covid.plotSinceFirstCaseBar(['Panama'], dff, True, todayDay, todayMon)
    return dff


datframe = runTodayPlots(listCountries=latinAmerica, condition=True, savePlot=False)

# covid.getSome(countries=CentralAmerica, dataFrame=datframe)
