import csv
import pandas as pd
import numpy as np
import json
import requests
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import date
from matplotlib.font_manager import FontProperties  # Smaller font
import test as covid

import os
import pathlib
thePlotPath = str(pathlib.Path(__file__).parent.absolute() ) + '/plots/'

fontP = FontProperties()
fontP.set_size('small')

def shortCountryName(country):
    countries = []
    for item in country:
        space = item.split(' ')  # Find spaces on country name
        originalName = item
        if len(space) > 1:
            originalName = item
            item = space[0]+space[1]  # If not concatenate
        countries.append(item)
    return countries


def caseVSday(countries, data, startDate, finalDate, printIt):
    df = pd.DataFrame()
    # Get dates data (Panama or any has the same)
    dates = data.loc[data['Country/Region']
                     == 'Panama', startDate: finalDate].columns
    df['Dates'] = dates
    shortCountryName(countries)

    for indx, item in enumerate(countries):
        varName = item+'Data'
        arrName = 'data'+item
        varName = data.loc[data['Country/Region']
                           == countries[indx], startDate: finalDate]
        arrName = varName.to_numpy()[0]
        df.insert(indx, item, arrName)
    if printIt:
        print(df)   
    return df, countries


def getSinceFirseCase(countries, dataFrame):
    dataDayZero = pd.DataFrame()
    shortCountryName(countries)
    sinceZero = []
    for indx, place in enumerate(countries):
        daysWithVirus = dataFrame.index[dataFrame[place] > 0].tolist()
        print('Days with virus in {}: {}'.format(place, len(daysWithVirus)))
        dataSince0 = dataFrame[place].iloc[daysWithVirus]
        dateSince0 = dataFrame['Dates'].iloc[daysWithVirus]
        dfName = place + 'DataFrame'
        dfName = pd.DataFrame()
        dfName.insert(0, place, dataSince0)
        dfName.insert(1, 'Dates', dateSince0)
        sinceZero.append(dfName)
    return sinceZero


def plotSinceFirsCase(firstCaseArray, saveIt, todayDay, todayMon):
    for item in firstCaseArray:
        arry = []
        for index in range(0, len(item)):
            arry.append(index+1)
        item.insert(0, 'Days', arry)
    # Plot
        xCoord = item['Days'].iloc[-1]
        yCoord = item[item.columns[1]].iloc[-1]
        plt.plot(item['Days'], item[item.columns[1]], 'o-',
                 label=item.columns[1] + '('+str(yCoord)+')')
        plt.legend(loc='best', prop=fontP)
        plt.text(xCoord, yCoord, yCoord)
        plt.title(todayDay+'/'+todayMon+'/'+date.today().strftime("%Y"))
        plt.xlabel('Days since first case')
        plt.ylabel('Numbers of cases')
    if saveIt:
        os.makedirs(thePlotPath, exist_ok=True)
        file_name = thePlotPath+'daysWithVirus-'+todayDay+'-'+todayMon+'.png'
        plt.savefig(file_name, dpi=199)
    plt.show()
