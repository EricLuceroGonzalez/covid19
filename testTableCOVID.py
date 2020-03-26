import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import date

import os
import pathlib
thePath = str(pathlib.Path(__file__).parent.absolute())
theCSVPath = thePath + '/csv'


today = date.today().strftime("%-m/%-d/%y")
todayDay = date.today().strftime("%-d")
todayMon = date.today().strftime("%-m")


website_url = requests.get(
    'https://en.wikipedia.org/wiki/Template:COVID-19_testing').text
soup = BeautifulSoup(website_url, 'html.parser')
# print(soup.prettify())
Countries = []
TotalTest = []
Positive = []
UpdateDate = []
TestPerMillion = []
PositivePerThousand = []

df = pd.DataFrame()
dfRegion = pd.DataFrame()

CountriesRegion = []
TotalTestRegion = []
PositiveRegion = []
UpdateDateRegion = []
TestPerMillionRegion = []
PositivePerThousandRegion = []

regions = []
countryRegion = []
# # Extrac by html class
my_table = soup.find('table', {'class': 'wikitable'})  # Get the table
allTd = my_table.findAll('tr')  # Get all <a> links (lists of countries)
# print(allTd)
for i, aTD in enumerate(allTd):
    for i, th in enumerate(aTD.findAll('th')):
        if isinstance(th.get('data-sort-value'), str) == True:
            aa = th.get('data-sort-value').split(',')
            regions.append(aa[0])
            countryRegion.append(aa[1])
            for a in th.find_next('a'):
                print(a)
                # print(a.find_next('a'))
                # culo.append(a.find_next('a').contents[0])
                allTds = aTD.findAll('td')
                # print(culo)
                for i, region in enumerate(allTds):
                    if i == 0:
                        s = region.contents[0].replace("\n", "")
                        TotalTestRegion.append(s)
                    elif i == 1:
                        s = region.contents[0].replace("\n", "")
                        PositiveRegion.append(s)
                    elif i == 2:
                        s = region.find('span').contents[0]
                        UpdateDateRegion.append(s)
                    elif i == 3:
                        s = region.contents[0].replace("\n", "")
                        TestPerMillionRegion.append(s)
                    elif i == 4:
                        s = region.contents[0].replace("\n", "")
                        PositivePerThousandRegion.append(s)
                    print('-------------')

        if isinstance(th.get('data-sort-value'), str) == False:
            for a in th.select('span > img'):
                Countries.append(a.find_next('a').contents[0])
                allTd = aTD.findAll('td')
                for i, vaina in enumerate(allTd):
                    if i == 0:
                        s = vaina.contents[0].replace("\n", "")
                        TotalTest.append(s)
                    elif i == 1:
                        s = vaina.contents[0].replace("\n", "")
                        Positive.append(s)
                    elif i == 2:
                        s = vaina.find('span').contents[0]
                        UpdateDate.append(s)
                    elif i == 3:
                        s = vaina.contents[0].replace("\n", "")
                        TestPerMillion.append(s)
                    elif i == 4:
                        s = vaina.contents[0].replace("\n", "")
                        PositivePerThousand.append(s)

df['Countries'] = Countries
df['TotalTest'] = TotalTest
df['Positive'] = Positive
df['UpdateDate'] = UpdateDate
df['TestPerMillion'] = TestPerMillion
df['PositivePerThousand'] = PositivePerThousand

print(df)


dfRegion['Region'] = countryRegion
dfRegion['TotalTest'] = TotalTestRegion
dfRegion['Positive'] = PositiveRegion
dfRegion['UpdateDate'] = UpdateDateRegion
dfRegion['TestPerMillion'] = TestPerMillionRegion
dfRegion['PositivePerThousand'] = PositivePerThousandRegion

print(dfRegion)

df.to_csv(theCSVPath + '/'+todayDay+'-'+todayMon+'-TestsPerCountry.csv')
dfRegion.to_csv(theCSVPath + '/'+todayDay+'-'+todayMon+'-TestsPerRegion.csv')
