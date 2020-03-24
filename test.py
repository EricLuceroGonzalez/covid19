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
thePlotPath = str(pathlib.Path(__file__).parent.absolute()) + '/plots/'

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
    dfList = list(data.columns.values)
    if dfList[-1] != finalDate:
        finalDate = dfList[-1]
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
    covid.shortCountryName(countries)
    sinceZero = []
    for indx, place in enumerate(countries):
        daysTranscurred = []
        daysWithVirus = dataFrame.index[dataFrame[place] > 0].tolist()
        for i in range(0, len(daysWithVirus)):
            daysTranscurred.append(i+1)
        print('Days with virus in {}: {}'.format(place, len(daysWithVirus)))
        dataDayZero = pd.DataFrame(daysTranscurred)
        dataSince0 = dataFrame[place].iloc[daysWithVirus]
        dateSince0 = dataFrame['Dates'].iloc[daysWithVirus]
        dfName = place + 'DataFrame'
        dfName = pd.DataFrame()
        dfName.insert(0, place, dataSince0)
        dfName.insert(1, 'Dates', dateSince0)
        dfName['Days'] = pd.Series(daysTranscurred, index=dfName.index)
        sinceZero.append(dfName)
    return sinceZero


def plotSinceFirstCase(firstCaseArray, saveIt, todayDay, todayMon):
    print(firstCaseArray)
    for item in firstCaseArray:
        arry = []
    # Plot
        xCoord = item['Days'].iloc[-1]
        yCoord = item[item.columns[0]].iloc[-1]
        # radii = 10 * np.random.rand(15)
        # colors = plt.cm.plasma(radii / 10.)
        axes = plt.gca()
        plt.plot(item['Days'], item[item.columns[0]], 'o-',
                 label=item.columns[0] + ' ('+str(yCoord)+')', alpha=0.8)
        plt.legend(loc='best', prop=fontP)
        plt.text(xCoord, yCoord, yCoord)
        plt.title(todayDay+'/'+todayMon+'/'+date.today().strftime("%Y"))
        plt.xlabel('Days since first case')
        plt.ylabel('Numbers of cases')
        axes.set_xlim([0, 25])
        axes.set_ylim([0, 1000])
    if saveIt:
        os.makedirs(thePlotPath, exist_ok=True)
        file_name = thePlotPath+'daysWithVirus-'+todayDay+'-'+todayMon+'.png'
        plt.savefig(file_name, dpi=199)
    plt.show()


def plotSinceFirstCaseBar(firstCaseArray, saveIt, startDate, lastDate):
    print('++++++++++++++++++++++++++++++++++    ++++++++++++++++++++++++++++++++++')
    print(startDate)
    for item in firstCaseArray:
        print('\nitem = \n{}'.format(item))
        print('++++++++++++++++++++++++++++++++++    ++++++++++++++++++++++++++++++++++')
        print(item.columns[0])
    # Plot
        xCoord = item['Days']
        yCoord = item[item.columns[0]]
        plt.bar(xCoord, yCoord,
                label='Cases per day in '+item.columns[0], edgecolor='red', color='red', alpha=0.4)
        plt.xlabel('Days since first case')
        plt.ylabel('Numbers of cases')
        plt.xticks(xCoord)
        for i in range(0, len(xCoord)):
            plt.text(item['Days'].iloc[i]-0.25, item[item.columns[0]
                                                     ].iloc[i], item[item.columns[0]].iloc[i])
        plt.legend(loc='best', prop=fontP)

        plt.title(startDate+'/'+lastDate+'/'+date.today().strftime("%Y"))
        if saveIt:
            os.makedirs(thePlotPath, exist_ok=True)
            file_name = thePlotPath+'Bar-daysWithVirus-'+startDate+'-'+lastDate+'.png'
            plt.savefig(file_name, dpi=199)
    plt.show()

def daysWithCases(fromZeroArray, dataFrame):
    # , dataFrame, place, startDate, finalDate):
    print('\n# Get dates data (Panama or any has the same)')
    zeroPanDays, zeroPan = getTheZeroDay(dataFrame, place='Panama')
    print(zeroPanDays)
    print(zeroPan)
    print(fromZeroArray)
    theDF = pd.DataFrame()
    theDF['Panama'] = zeroPan


def getTheZeroDay(dataFrame, place):
    theList = dataFrame[place].tolist()
    daysFromZero = []
    for i in theList:
        if i != 0:
            daysFromZero.append(i)
    lenDays = len(daysFromZero)
    return lenDays, daysFromZero
