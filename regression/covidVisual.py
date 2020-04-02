import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import seaborn as sns
import pandas as pd
import random
import math
import time
from sklearn.linear_model import LinearRegression, BayesianRidge
from sklearn.model_selection import RandomizedSearchCV, train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, mean_absolute_error
from datetime import date, timedelta
import datetime
import operator
import os
import pathlib
plt.style.use('fivethirtyeight')


thePath = str(pathlib.Path(__file__).parent.absolute())
theCSVPath = thePath + '/csv'

# Dates:
today = (date.today()).strftime("%-m/%-d/%y")
yesterday = (date.today() - timedelta(days=1)).strftime("%-m/%-d/%y")
todayDay = date.today().strftime("%-d")
todayMon = date.today().strftime("%-m")

confirmed_df = pd.read_csv(
    'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
deaths_df = pd.read_csv(
    'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
recoveries_df = pd.read_csv(
    'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')
latest_data = pd.read_csv(
    'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/04-01-2020.csv')

latest_data.head()
confirmed_df.head()
cols = confirmed_df.keys()

confirmed = confirmed_df.loc[:, cols[4]:cols[-1]]
deaths = deaths_df.loc[:, cols[4]:cols[-1]]
recoveries = recoveries_df.loc[:, cols[4]:cols[-1]]

dates = confirmed.keys()
world_cases = []
total_deaths = []
mortality_rate = []
recovery_rate = []
total_recovered = []
total_active = []
china_cases = []
italy_cases = []
us_cases = []
spain_cases = []
france_cases = []
panama_cases = []

for i in dates:
    confirmed_sum = confirmed[i].sum()
    death_sum = deaths[i].sum()
    recovered_sum = recoveries[i].sum()

    # confirmed, deaths, recovered, and active
    world_cases.append(confirmed_sum)
    total_deaths.append(death_sum)
    total_recovered.append(recovered_sum)
    total_active.append(confirmed_sum-death_sum-recovered_sum)

    # calculate rates
    mortality_rate.append(death_sum/confirmed_sum)
    recovery_rate.append(recovered_sum/confirmed_sum)

    # case studies
    china_cases.append(
        confirmed_df[confirmed_df['Country/Region'] == 'China'][i].sum())
    italy_cases.append(
        confirmed_df[confirmed_df['Country/Region'] == 'Italy'][i].sum())
    us_cases.append(
        confirmed_df[confirmed_df['Country/Region'] == 'US'][i].sum())
    spain_cases.append(
        confirmed_df[confirmed_df['Country/Region'] == 'Spain'][i].sum())
    france_cases.append(
        confirmed_df[confirmed_df['Country/Region'] == 'France'][i].sum())
    panama_cases.append(
        confirmed_df[confirmed_df['Country/Region'] == 'Panama'][i].sum())


def daily_increase(data):
    print('inside daily_increase')
    d = []
    for i in range(len(data)):
        if i == 0:
            d.append(data[0])
        else:
            d.append(data[i]-data[i-1])
    return d


world_daily_increase = daily_increase(world_cases)
china_daily_increase = daily_increase(china_cases)
italy_daily_increase = daily_increase(italy_cases)
us_daily_increase = daily_increase(us_cases)
spain_daily_increase = daily_increase(spain_cases)
france_daily_increase = daily_increase(france_cases)
panama_daily_increase = daily_increase(panama_cases)

days_since_1_22 = np.array([i for i in range(len(dates))]).reshape(-1, 1)
world_cases = np.array(world_cases).reshape(-1, 1)
total_deaths = np.array(total_deaths).reshape(-1, 1)
total_recovered = np.array(total_recovered).reshape(-1, 1)

days_in_future = 10
future_forcast = np.array(
    [i for i in range(len(dates)+days_in_future)]).reshape(-1, 1)

adjusted_dates = future_forcast[:-10]

start = '1/22/2020'
start_date = datetime.datetime.strptime(start, '%m/%d/%Y')
future_forcast_dates = []
for i in range(len(future_forcast)):
    future_forcast_dates.append(
        (start_date + datetime.timedelta(days=i)).strftime('%m/%d/%Y'))


X_train_confirmed, X_test_confirmed, y_train_confirmed, y_test_confirmed = train_test_split(
    days_since_1_22, world_cases, test_size=0.05, shuffle=False)

days = np.array([i for i in range(len(dates))])
print(len(days_since_1_22))
print(len(world_daily_increase))
print(len(days))
print(days)
print('------------\n')

plt.figure(figsize=(16, 9))
plt.bar(days, world_daily_increase)
plt.title('World Daily Increases in Confirmed Cases', size=30)
plt.xlabel('Days Since 1/22/2020', size=30)
plt.ylabel('# of Cases', size=30)
plt.xticks(size=20)
plt.yticks(size=20)
# plt.show()

plt.figure(figsize=(16, 9))
# plt.bar(days, panama_daily_increase)
plt.title('Panama Daily Increases in Confirmed Cases', size=30)
plt.xlabel('Days Since 1/22/2020', size=30)
plt.ylabel('# of Cases', size=30)
plt.xticks(size=20)
plt.yticks(size=20)
barsTestDay = sns.barplot(x=days, y=us_daily_increase,
                          edgecolor='red', color='red', alpha=0.5, label='Tests')
barsCasesDay = sns.barplot(
    x=days, y=panama_daily_increase, color='royalblue',  label='Positives')

plt.show()
