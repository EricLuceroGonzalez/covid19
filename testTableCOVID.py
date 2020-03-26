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

# # Extrac by html class
my_table = soup.find('table', {'class': 'wikitable'})  # Get the table
allTd = my_table.findAll('tr')  # Get all <a> links (lists of countries)
# print(allTd)
for i, aTD in enumerate(allTd):
    for i, th in enumerate(aTD.findAll('th')):
        print('\n\n-------------')
        # print(th)

        if isinstance(th.get('data-sort-value'), str) == False:
            for a in th.select('span > img'):
                Countries.append(a.find_next('a').contents[0])
                allTd = aTD.findAll('td')
                # print(allTd)
                for i, vaina in enumerate(allTd):
                    print('****************************** i = {}'.format(i))
                    if i == 0:
                        s = vaina.contents[0].replace("\n", "")
                        TotalTest.append(s)
                    elif i == 1:
                        s = vaina.contents[0].replace("\n", "")
                        Positive.append(s)
                    elif i == 2:
                        print('******************************')
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


df.to_csv(theCSVPath + '/'+todayDay+'-'+todayMon+'-TestsPerCountry.csv')
