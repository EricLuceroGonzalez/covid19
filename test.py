import csv
import pandas as pd
import numpy as np
import json
import requests
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import date, datetime, time
from matplotlib.font_manager import FontProperties  # Smaller font
import test as covid

import os
import pathlib
thePlotPath = str(pathlib.Path(__file__).parent.absolute()) + '/plots/'

fontP = FontProperties()
fontP.set_size('small')

todayDay = date.today().strftime("%-d")
todayMon = date.today().strftime("%-m")
todayTime = datetime.today().strftime("%H:%M")


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


def getSinceCase(countries, dataFrame):
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


def plotSinceFirstCase(countries, dataFrame, saveIt, todayDay, todayMon, logScale):
    firstCaseArray = getSinceFirstCase(countries, dataFrame)
    for i, item in enumerate(firstCaseArray):
        arry = []
    # Plot
        xCoord = item['Days'].iloc[-1]
        yCoord = item[item.columns[0]].iloc[-1]
        # radii = 10 * np.random.rand(15)
        # colors = plt.cm.plasma(radii / 10.)
        axes = plt.gca()
        sns.lineplot(item['Days'], item[item.columns[0]], marker='o',
                     label=item.columns[0] + ' ('+str(yCoord)+')', alpha=0.8)
        if len(item) < 10:
            plt.text(xCoord-0.35, yCoord + (yCoord/20), yCoord,
                     ha="center", fontsize=9, weight='bold')
        else:
            plt.text(xCoord-0.35, yCoord + (yCoord/40), yCoord,
                     ha="center", fontsize=9, weight='bold')
        plt.title(todayDay+'/'+todayMon+'/'+date.today().strftime("%Y"))
        plt.xlabel('Days since first case')
        plt.ylabel('Numbers of cases')
        # axes.set_xlim([0, 30])
        # axes.set_ylim([0, 1200])
        plt.legend(loc='best', prop=fontP)
    if logScale:
        axes.set(yscale="log")
    if saveIt:
        os.makedirs(thePlotPath, exist_ok=True)
        file_name = thePlotPath+'daysWithVirus-'+todayDay+'-'+todayMon+'.png'
        plt.savefig(file_name, dpi=199, quality=95)
    plt.show()


def plotSinceFirstCaseBar(countries, dataFrame, saveIt, startDate, lastDate):
    firstCaseArray = getSinceFirstCase(countries, dataFrame)
    print('++++++++++++++++++++++++++++++++++    ++++++++++++++++++++++++++++++++++')
    print(startDate)
    for item in firstCaseArray:
        print('\nitem = \n{}'.format(item))
        print('++++++++++++++++++++++++++++++++++    ++++++++++++++++++++++++++++++++++')
        print(item.columns[0])
    # Plot
        xCoord = item['Days']
        yCoord = item[item.columns[0]]
        plt.plot(item['Days'], item['increment'], 'o-', label='Increment')
        plt.bar(xCoord, yCoord,
                label='Cases per day in '+item.columns[0], edgecolor='red', color='red', alpha=0.4)
        plt.xlabel('Days since first case')
        plt.ylabel('Numbers of cases')
        plt.xticks(xCoord)
        for i in range(0, len(xCoord)):
            y_level = item[item.columns[0]].iloc[i]
            yy_level = item[item.columns[3]].iloc[i]
            plt.text(item['Days'].iloc[i]-0.35, y_level + (y_level/70),
                     item[item.columns[0]].iloc[i])
            plt.text(item['Days'].iloc[i]-0.35, yy_level + (yy_level/10),
                     item[item.columns[3]].iloc[i])
        plt.legend(loc='uppert left', prop=fontP)

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


def getSinceFirstCase(countries, dataFrame):
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
        casesPerDay = []
        dflist = dfName[place].tolist()
        for i, j in enumerate(dflist):
            if i == 0:
                casesPerDay.append(dflist[i])
            else:
                casesPerDay.append(dflist[i] - dflist[i-1])
        dfName['increment'] = pd.Series(casesPerDay, index=dfName.index)
        sinceZero.append(dfName)
        print(dfName)
    return sinceZero


centralAmerica = ['Panama', 'El Salvador', 'Nicaragua',
                  'Guatemala', 'Costa Rica', 'Honduras', 'Mexico']
# Suramerica
surAmerica = ['Venezuela', 'Uruguay', 'Colombia',
              'Chile', 'Argentina', 'Ecuador', 'Peru']
# LatinAmerica
latinAmerica = centralAmerica + surAmerica
# BigCountries
bigCountries = ['US', 'Italy', 'Spain', 'Mexico', 'Switzerland',
                'Netherlands',
                'Brazil',
                'United Kingdom',
                'Iran',
                'France', 'Belgium',
                'Germany']
# Europe
europe = ['Italy', 'Spain', 'Switzerland',
          'Netherlands',
          'United Kingdom',
          'France', 'Belgium',
          'Germany']


def dataArrays(region):
    if region == 'latinAmerica':
        return latinAmerica
    if region == 'bigCountries':
        return bigCountries
    if region == 'centralAmerica':
        return centralAmerica
    if region == 'europe':
        return europe
    if (region != 'Europe' or region != 'CentralAmerica' or region != 'BigCountries' or region != 'LatinAmerica'):
        return 'invalid'


def scatterPlotCountries(csvData, arrayCountries, plotTitle):
    df = pd.DataFrame()
    place = []
    dpm = []
    tpm = []
    cpm = []
    tot = []
    toc = []
    tod = []
    data = arrayCountries
    for j, i in enumerate(data):
        countryIndx = csvData.index[csvData['Country'] == i].tolist()
        place.append(csvData.loc[countryIndx]['Country'].tolist()[0])
        dpm.append(csvData.loc[countryIndx]
                   ['DeathsPerM'].tolist()[0].replace(' ', ''))
        tot.append(csvData.loc[countryIndx]['Total Tests'].tolist()[0])
        toc.append(csvData.loc[countryIndx]['Total Cases'].tolist()[0])
        tpm.append(csvData.loc[countryIndx]['TestsPerM'].tolist()[0])
        cpm.append(csvData.loc[countryIndx]['Tot CasesPerM'].tolist()[0])
        tod.append(csvData.loc[countryIndx]['Total Deaths'].tolist()[0])        

    df['Place'] = pd.Series(place)
    df['Case-Per-Million'] = pd.to_numeric(pd.Series(cpm), errors='coerce')
    df['Dead-Per-Million'] = pd.to_numeric(pd.Series(dpm), errors='coerce')
    df['Test-Per-Million'] = pd.to_numeric(pd.Series(tpm), errors='coerce')
    df['TotalTests'] = pd.to_numeric(pd.Series(tot), errors='coerce')
    df['TotalCases'] = pd.to_numeric(pd.Series(toc), errors='coerce')
    df['TotalDeaths'] = pd.to_numeric(pd.Series(tod), errors='coerce')    
    print(df)
    plt.figure(figsize=plt.figaspect(0.33))
    # barsTestDay = sns.barplot(x=df['Place'], y=df['Case-Per-Million'],
    #                           edgecolor='red', color='red', alpha=0.35, label='Tests')
    cmap = sns.cubehelix_palette(dark=.4, light=.9, as_cmap=True)
    bars = sns.scatterplot(x='Test-Per-Million', y='Case-Per-Million',
                           hue='Case-Per-Million', size='Dead-Per-Million',
                           data=df,
                           sizes=(80, 650), palette=cmap)
    for i in df.iterrows():
        if i[1]['Case-Per-Million'] > 100 and i[1]['Place'] == 'Panama':
            bars.text(i[1]['Test-Per-Million'], i[1]['Case-Per-Million'] + (i[1]['Case-Per-Million']/20),
                      i[1]['Place'], color='blue', ha="center", fontsize=10, weight='bold')
        if i[1]['Case-Per-Million'] > 1600:
            bars.text(i[1]['Test-Per-Million'], i[1]['Case-Per-Million'] + (i[1]['Case-Per-Million']/60),
                      i[1]['Place'], color='black', ha="center", fontsize=9, weight='bold')
        if i[1]['Case-Per-Million'] < 1600 and i[1]['Case-Per-Million'] > 1200:
            bars.text(i[1]['Test-Per-Million'], i[1]['Case-Per-Million'] + (i[1]['Case-Per-Million']/40),
                      i[1]['Place'], color='black', ha="center", fontsize=9, weight='bold')
        elif i[1]['Case-Per-Million'] < 1200 and i[1]['Case-Per-Million'] > 900:
            bars.text(i[1]['Test-Per-Million'], i[1]['Case-Per-Million'] + (i[1]['Case-Per-Million']/20),
                      i[1]['Place'], color='black', ha="center", fontsize=9, weight='bold')
        elif i[1]['Case-Per-Million'] > 150 and i[1]['Case-Per-Million'] < 900 and i[1]['Place'] != 'Panama':
            bars.text(i[1]['Test-Per-Million'], i[1]['Case-Per-Million'] + (i[1]['Case-Per-Million']/30),
                      i[1]['Place'], color='black', ha="center", fontsize=9, weight='bold')
        elif i[1]['Case-Per-Million'] < 150 and i[1]['Case-Per-Million'] > 50:
            bars.text(i[1]['Test-Per-Million'], i[1]['Case-Per-Million'] + (i[1]['Case-Per-Million']/9),
                      i[1]['Place'], color='black', ha="center", fontsize=6, weight='bold')
        elif i[1]['Case-Per-Million'] < 50:
            bars.text(i[1]['Test-Per-Million'], i[1]['Case-Per-Million'] + (i[1]['Case-Per-Million']/3),
                      i[1]['Place'], color='black', ha="center", fontsize=6, weight='bold')
    plt.legend(loc='upper left', fontsize=8)
    plt.title(plotTitle + ' - Relation per million at ' +
              todayDay + '/'+todayMon+'/20 - '+todayTime)
    file_name = thePlotPath + plotTitle + ' perMillion-'+todayDay+'-'+todayMon+'.png'
    # bbox_inches removes extra white spaces
    plt.savefig(file_name, dpi=300, quality=95, bbox_inches='tight')
    plt.show()

    return df


def perMillionPlots(theDataFrame, thePlotTitle):
    
    colA = 'Case-Per-Million'
    colB = 'Test-Per-Million'
    colC = 'TotalTests'
    colD = 'TotalCases'
    colE = 'TotalDeaths'
    colF = 'Dead-Per-Million'
    # sorted data
    a = theDataFrame.sort_values(by=[colA], ascending=False)
    b = theDataFrame.sort_values(by=[colB], ascending=False)
    c = theDataFrame.sort_values(by=[colC], ascending=False)
    d = theDataFrame.sort_values(by=[colD], ascending=False)
    e = theDataFrame.sort_values(by=[colE], ascending=False)
    f = theDataFrame.sort_values(by=[colF], ascending=False)         

    pal = sns.color_palette("coolwarm", len(a))

    # plt.figure(figsize=plt.figaspect(1.))
    plt.subplot(121)
    rank = a[colA].argsort().argsort()
    sns.barplot(x=colA, y='Place', data=a,
                palette=np.array(pal[::-1])[rank])
    
    plt.subplot(122)
    rank = b[colB].argsort().argsort()
    sns.barplot(x=colB, y='Place', data=b,
                palette=np.array(pal[::-1])[rank])
    # Save it
    # plt.title('Panama&'+thePlotTitle +'-perMillion')
    file_name = thePlotPath + 'Panama&'+thePlotTitle +'-perMillion-'+todayDay+'-'+todayMon+'.png'
    plt.savefig(file_name, dpi=300, quality=95, bbox_inches='tight')
    plt.show()

    # plt.figure(figsize=plt.figaspect(1.))
    plt.subplot(121)
    rank = c[colC].argsort().argsort()
    sns.barplot(x=colC, y='Place', data=c,
                palette=np.array(pal[::-1])[rank])
    
    plt.subplot(122)
    rank = d[colD].argsort().argsort()
    sns.barplot(x=colD, y='Place', data=d,
                palette=np.array(pal[::-1])[rank])
    # plt.title('Panama&'+thePlotTitle +'-Totals')
    file_name = thePlotPath + 'Panama&'+thePlotTitle +'-Totals-'+todayDay+'-'+todayMon+'.png'                
    plt.savefig(file_name, dpi=300, quality=95, bbox_inches='tight')
    plt.show()

    # plt.figure(figsize=plt.figaspect(1.))
    plt.subplot(121)
    rank = e[colE].argsort().argsort()
    sns.barplot(x=colE, y='Place', data=e,
                palette=np.array(pal[::-1])[rank])
    
    plt.subplot(122)
    rank = f[colF].argsort().argsort()
    sns.barplot(x=colF, y='Place', data=f,
                palette=np.array(pal[::-1])[rank])
    # Save it
    # plt.title('Panama&'+thePlotTitle +'-perMillion')
    file_name = thePlotPath + 'Panama&'+thePlotTitle +'-Deaths-'+todayDay+'-'+todayMon+'.png'
    plt.savefig(file_name, dpi=300, quality=95, bbox_inches='tight')
    plt.show()

print(2974 - 3234)
print(13648 - 14588)
