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
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import date, timedelta
from matplotlib.font_manager import FontProperties  # Smaller font
import test as covid
import os
import pathlib
thePath = str(pathlib.Path(__file__).parent.absolute())
theCSVPath = thePath + '/csv/'
thePlotPath = thePath + '/plots/'

# today = date.today().strftime("%-m/%-d/%y")
today = (date.today() - timedelta(days=1)).strftime("%-m/%-d/%y")
yesterday = (date.today() - timedelta(days=1)).strftime("%-m/%-d/%y")
todayDay = date.today().strftime("%-d")
todayMon = date.today().strftime("%-m")

panamaData = pd.read_csv('Panama.csv')
allData = pd.read_csv(theCSVPath+'26-3-TestsPerCountry.csv')

date = panamaData['Date']
cases = panamaData['Cases']
totalCases = panamaData['TotalCases']
tests = panamaData['Test']
daysVirus = panamaData['DaysWithVirus']
panamaData['CasesTest'] = round((cases/tests)*100, 1)

print(panamaData)


f, ax = plt.subplots(figsize=(16, 8))
plt.xlabel('Dias desde el primer caso')
plt.ylabel('Casos')
sns.set_style("dark")

# sns.set_style("ticks")
sns.set(style="whitegrid", color_codes=True)

lineTotal = sns.lineplot(x=daysVirus-1, y=totalCases,
                         marker='o', label='Total Cases')
barsTestDay = sns.barplot(x=daysVirus, y=tests,
                          edgecolor='red', color='red', alpha=0.5, label='Tests')
barsCasesDay = sns.barplot(
    x=daysVirus, y=cases, color='royalblue',  label='Positives')

for index, row in panamaData.iterrows():
    barsTestDay.text(row.DaysWithVirus-1, row.Test+(row.Test/40),
                     str(round(row.Test, 2)), color='black', ha="center")
    barsCasesDay.text(row.DaysWithVirus-1, row.Cases + (row.Cases/40),
                      str(round(row.CasesTest, 2))+'%', color='black', ha="center", fontsize=9, weight='bold')
    if index < 10:
        lineTotal.text(row.DaysWithVirus-1, row.TotalCases + (row.TotalCases/2),
                       '+' + str(round(row.Cases, 2)), color='green', ha="right", fontsize=7, weight='bold', alpha=0.8, label='Total Cases')
        lineTotal.text(row.DaysWithVirus-1.1, row.TotalCases + (row.TotalCases/15),
                       str(round(row.TotalCases, 2)), color='firebrick', ha="center", fontsize=8, weight='bold')
    if (index > 9 and index < 12):
        lineTotal.text(row.DaysWithVirus-1, row.TotalCases + (row.TotalCases/4),
                       '+' + str(round(row.Cases, 2)), color='green', ha="right", fontsize=7, weight='bold', alpha=0.8, label='Total Cases')
        lineTotal.text(row.DaysWithVirus-1.1, row.TotalCases + (row.TotalCases/15),
                   str(round(row.TotalCases, 2)), color='firebrick', ha="center", fontsize=8, weight='bold')
    if index < 15 and index > 12:
        lineTotal.text(row.DaysWithVirus-1, (row.TotalCases + (row.TotalCases/8)),
                       '+' + str(round(row.Cases, 2)), color='green', ha="right", fontsize=7, weight='bold', alpha=0.8, label='Total Cases')
        lineTotal.text(row.DaysWithVirus-1.1, row.TotalCases + (row.TotalCases/15),
                   str(round(row.TotalCases, 2)), color='firebrick', ha="center", fontsize=8, weight='bold')
    if index > 15 and index < 18:
        lineTotal.text(row.DaysWithVirus-1, (row.TotalCases + (row.TotalCases/10)),
                       '+' + str(round(row.Cases, 2)), color='green', ha="right", fontsize=7, weight='bold', alpha=0.8, label='Total Cases')
        lineTotal.text(row.DaysWithVirus-1.1, row.TotalCases + (row.TotalCases/15),
                   str(round(row.TotalCases, 2)), color='firebrick', ha="center", fontsize=8, weight='bold')
    if index > 17:
        lineTotal.text(row.DaysWithVirus-1, (row.TotalCases + (row.TotalCases/40)),
                       '+' + str(round(row.Cases, 2)), color='green', ha="right", fontsize=7, weight='bold', alpha=0.8, label='Total Cases')
        lineTotal.text(row.DaysWithVirus-1.1, row.TotalCases + (row.TotalCases/110),
                   str(round(row.TotalCases, 2)), color='firebrick', ha="center", fontsize=8, weight='bold')
plt.legend(loc='best')
plt.title('Increment of cases per day and percentage of positive tests results')
file_name = thePlotPath+'barPanamaDayli-'+todayDay+'-'+todayMon+'.png'
plt.savefig(file_name, dpi=300, quality=95)
plt.show()


# figure = plt.figure()
# tips = sns.load_dataset("tips")
# # ax = sns.scatterplot(x="total_bill", y="tip", data=tips,hue='smoker')
# ax = sns.scatterplot(x='TotalTest', y='Positive', data=allData,hue='PositivePerThousand',size='TotalTest',sizes=(90, 600))
# for index, row in allData.iterrows():
#     ax.text(row.TotalTest, row.Positive,
#                      row.Countries, color='black', ha="center")
# ax.set(xscale="log",yscale='log')
# plt.show()
