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
sns.set_style("dark")
axes = plt.gca()

# sns.set_style("ticks")
sns.set(style="whitegrid", color_codes=True)

barsTestDay = sns.barplot(x=daysVirus, y=tests,
                          edgecolor='red', color='red', alpha=0.35, label='Tests')
barsCasesDay = sns.barplot(
    x=daysVirus, y=cases, color='royalblue',  label='Positives')
ax2 = ax.twinx()
lineTotal = sns.lineplot(x=daysVirus-1, y=totalCases,
                         marker='o', label='Total Cases', ax=ax2)
ax2.set_ylim([0, 3450])
for index, row in panamaData.iterrows():
    if index < 10:
        barsTestDay.text(row.DaysWithVirus-1, row.Test+(row.Test/40),
                         str(round(row.Test, 2)), color='black', ha="center", fontsize=7, weight='bold')
        barsCasesDay.text(row.DaysWithVirus-1, row.Cases + (row.Cases/60),
                      str(round(row.CasesTest, 1))+'%', color='black', ha="center", fontsize=7, weight='bold')
        lineTotal.text(row.DaysWithVirus-1, row.TotalCases + (row.TotalCases/2),
                   '+' + str(round(row.Cases, 2)), color='green', ha="right", fontsize=12, weight='bold', alpha=0.8, label='Total Cases')
        lineTotal.text(row.DaysWithVirus-1.1, row.TotalCases + (row.TotalCases/15),
                   str(round(row.TotalCases, 2)), color='firebrick', ha="center", fontsize=9, weight='bold')
    if (index > 9 and index < 12):
        barsTestDay.text(row.DaysWithVirus-1, row.Test+(row.Test/40),
                         str(round(row.Test, 2)), color='black', ha="center", fontsize=7, weight='bold')
        barsCasesDay.text(row.DaysWithVirus-1, row.Cases + (row.Cases/60),
                      str(round(row.CasesTest, 1))+'%', color='black', ha="center", fontsize=7, weight='bold')
        lineTotal.text(row.DaysWithVirus-1, row.TotalCases + (row.TotalCases/4),
                       '+' + str(round(row.Cases, 2)), color='green', ha="right", fontsize=12, weight='bold', alpha=0.8, label='Total Cases')
        lineTotal.text(row.DaysWithVirus-1.1, row.TotalCases + (row.TotalCases/15),
                       str(round(row.TotalCases, 2)), color='firebrick', ha="center", fontsize=9, weight='bold')
    if index < 15 and index > 12:
        barsTestDay.text(row.DaysWithVirus-1, row.Test+(row.Test/40),
                         str(round(row.Test, 2)), color='black', ha="center", fontsize=7, weight='bold')
        barsCasesDay.text(row.DaysWithVirus-1, row.Cases + (row.Cases/60),
                      str(round(row.CasesTest, 1))+'%', color='black', ha="center", fontsize=7, weight='bold')
        lineTotal.text(row.DaysWithVirus-1, (row.TotalCases + (row.TotalCases/8)),
                       '+' + str(round(row.Cases, 2)), color='green', ha="right", fontsize=12, weight='bold', alpha=0.8, label='Total Cases')
        lineTotal.text(row.DaysWithVirus-1.1, row.TotalCases + (row.TotalCases/15),
                       str(round(row.TotalCases, 2)), color='firebrick', ha="center", fontsize=9, weight='bold')
    if index > 15 and index < 18:
        barsTestDay.text(row.DaysWithVirus-1, row.Test+(row.Test/40),
                         str(round(row.Test, 2)), color='black', ha="center", fontsize=7, weight='bold')
        barsCasesDay.text(row.DaysWithVirus-1, row.Cases + (row.Cases/70),
                      str(round(row.CasesTest, 1))+'%', color='black', ha="center", fontsize=7, weight='bold')
        lineTotal.text(row.DaysWithVirus-1, (row.TotalCases + (row.TotalCases/6)),
                       '+' + str(round(row.Cases, 2)), color='green', ha="right", fontsize=12, weight='bold', alpha=0.8, label='Total Cases')
        lineTotal.text(row.DaysWithVirus-1.1, row.TotalCases + (row.TotalCases/15),
                       str(round(row.TotalCases, 2)), color='firebrick', ha="center", fontsize=9, weight='bold')
    if index > 18 and index < 30:
        barsTestDay.text(row.DaysWithVirus-1, row.Test+(row.Test/40),
                         str(round(row.Test, 2)), color='black', ha="center", fontsize=7, weight='bold')
        barsCasesDay.text(row.DaysWithVirus-1, row.Cases + (row.Cases/90),
                      str(round(row.CasesTest, 1))+'%', color='black', ha="center", fontsize=7, weight='bold')
        lineTotal.text(row.DaysWithVirus-1, (row.TotalCases + (row.TotalCases/30)),
                       '+' + str(round(row.Cases, 2)), color='green', ha="right", fontsize=12, weight='bold', alpha=0.8, label='Total Cases')
        lineTotal.text(row.DaysWithVirus-1.1, row.TotalCases + (row.TotalCases/110),
                       str(round(row.TotalCases, 2)), color='firebrick', ha="center", fontsize=9, weight='bold')
    if index > 29:
        barsCasesDay.text(row.DaysWithVirus-1, row.Cases + (row.Cases/100),
                      str(round(row.CasesTest, 1))+'%', color='black', ha="center", fontsize=7, weight='bold')
        barsTestDay.text(row.DaysWithVirus-1, row.Test+(row.Test/80),
                         str(round(row.Test, 2)), color='black', ha="center", fontsize=7, weight='bold')
        lineTotal.text(row.DaysWithVirus-1.1, (row.TotalCases + (row.TotalCases/35)),
                       '+' + str(round(row.Cases, 2)), color='green', ha="right", fontsize=12, weight='bold', alpha=0.8, label='Total Cases')
        lineTotal.text(row.DaysWithVirus-1.1, row.TotalCases + (row.TotalCases/110),
                       str(round(row.TotalCases, 2)), color='firebrick', ha="center", fontsize=9, weight='bold')
ax.legend(loc='upper left')
ax2.legend(loc='upper center')
ax2.set_ylabel('Acumulated number of cases')
ax.set_ylabel('Number of tests per day')
plt.title('Increment of cases per day and percentage of positive tests results')
file_name = thePlotPath+'barPanamaDayli-'+todayDay+'-'+todayMon+'.png'
plt.savefig(file_name, dpi=300, quality=95, bbox_inches='tight')
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
