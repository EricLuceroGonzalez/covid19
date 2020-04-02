import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from datetime import date

import os
import pathlib
thePath = str(pathlib.Path(__file__).parent.absolute())
theCSVPath = thePath + '/csv/'


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
# Extrac by html class
my_table = soup.find('table', {'class': 'wikitable'})  # Get the table
allTd = my_table.findAll('tr')  # Get all <a> links (lists of countries)
# print(allTd)
for i, aTD in enumerate(allTd):
    for i, th in enumerate(aTD.findAll('th')):
        # if isinstance(th.get('data-sort-value'), str) == True:
        #     aa = th.get('data-sort-value').split(',')
        #     regions.append(aa[0])
        #     countryRegion.append(aa[1])
        #     for a in th.find_next('a'):
        #         # print(a)
        #         # print(a.find_next('a'))
        #         allTds = aTD.findAll('td')
        #         for i, region in enumerate(allTds):
        #             if i == 0:
        #                 print(
        #                     '&&&&&&   &&&&&&   &&&&&&   &&&&&&   &&&&&&  &&&&&&  &&&&&&   &&&&&&')
        #                 print(region.contents)
        #                 s = region.contents[0].replace("'", '')
        #                 s = ''.join(c for c in s if c.isnumeric())
        #                 s = int(s)
        #                 TotalTestRegion.append(s)
                    # elif i == 1:
                    #     print(region.contents[0])
                    #     s = region.contents[0].replace("\n", "")
                    #     s = ''.join(c for c in s if c.isnumeric())
                    #     s = int(s)
                    #     PositiveRegion.append(s)
                    # elif i == 2:
                    #     # s = region.find('span').contents[0]
                    #     UpdateDateRegion.append(s)
                    # elif i == 3:
                    #     s = region.contents[0].replace("\n", "")
                    #     s = ''.join(c for c in s if c.isnumeric())
                    #     int(s)
                    #     TestPerMillionRegion.append(s)
                    # elif i == 4:
                    #     s = region.contents[0].replace("\n", "")
                    #     s = ''.join(c for c in s if c.isnumeric())
                    #     PositivePerThousandRegion.append(s)
                    # print('-------------')

        if isinstance(th.get('data-sort-value'), str) == False:
            for a in th.select('span > img'):
                Countries.append(a.find_next('a').contents[0])
                allTd = aTD.findAll('td')
                for i, vaina in enumerate(allTd):
                    if i == 0:
                        print('conte = {}'.format(vaina.contents[0]))
                        s = vaina.contents[0].replace("'", '')
                        s = ''.join(c for c in s if c.isnumeric())
                        s = int(s)
                        TotalTest.append(s)
                        print(TotalTest)
                    elif i == 1:
                        print('conte = {}'.format(vaina.contents[0]))
                        s = vaina.contents[0].replace("'", '')
                        s = ''.join(c for c in s if c.isnumeric())
                        print('*****************************')
                        if s != '':
                            s = int(s)
                        Positive.append(s)
                        print(Positive)
                    elif i == 2:
                        # s = vaina.contents[0].replace("'", '')
                        # s = ''.join(c for c in s if c.isnumeric())
                        # s = int(s)
                        UpdateDate.append(s)
                    elif i == 3:
                        s = vaina.contents[0].replace("'", '')
                        s = ''.join(c for c in s if c.isnumeric())
                        if s != '':
                            s = int(s)
                        TestPerMillion.append(s)
                    elif i == 4:
                        s = vaina.contents[0].replace("'", '')
                        s = ''.join(c for c in s if c.isnumeric())
                        if s != '':
                            s = int(s)
                        PositivePerThousand.append(s)
df['Countries'] = Countries
df['TotalTest'] = TotalTest
df['Positive'] = Positive
df['UpdateDate'] = UpdateDate
df['TestPerMillion'] = TestPerMillion
df['PositivePerThousand'] = PositivePerThousand
# print(df)


# dfRegion['Region'] = countryRegion
# dfRegion['TotalTest'] = TotalTestRegion
# dfRegion['Positive'] = PositiveRegion
# dfRegion['UpdateDate'] = UpdateDateRegion
# dfRegion['TestPerMillion'] = TestPerMillionRegion
# dfRegion['PositivePerThousand'] = PositivePerThousandRegion
# # dfRegion['PositivePerTest'] = (dfRegion['Positive'] + dfRegion['PositivePerThousand'])
# # dfRegion.Positive = dfRegion.Positive.astype(np.int64)
# # dfRegion.TotalTest = dfRegion.TotalTest.astype(np.int64)

# # dfRegion = dfRegion.assign(PositivePerThousand =lambda x: (x['TotalTest'] + x['Positive'] ) )

# # print(dfRegion)

# df.to_csv(theCSVPath + '/'+todayDay+'-'+todayMon+'-TestsPerCountry.csv',float_format='%.f')
# # dfRegion.to_csv(theCSVPath + '/'+todayDay+'-'+todayMon+'-TestsPerRegion.csv',float_format='%.f')

print(theCSVPath +'tests.csv')
savedData = pd.read_csv(theCSVPath +'tests.csv')
print(savedData)

print(savedData['Countries'] == 'Armenia')
# a = pd.Series(dfRegion['TotalTest'])
# pd.to_numeric(a, errors='ignore')
# print(a)
# for i in a:
#     print(int(i)+'2')

# print('\n ***********  ***********  ***********  ***********  ***********  ')
# # for i, j in enumerate(dfRegion['Positive'].tolist()):
# #     # dfRegion['PositivePerTest'] = dfRegion['TotalTest'].astype(float)


# # print(dfRegion)

# # print(savedData['Countries']=='Panama')

# # axes = plt.gca()
# # plt.bar(savedData['Countries']=='Panama', item[item.columns[0]], 'o-',
# #          label=item.columns[0] + ' ('+str(yCoord)+')', alpha=0.8)
# # plt.legend(loc='best', prop=fontP)
# # plt.text(xCoord-0.35, yCoord + (yCoord/20), yCoord)
# # plt.title(todayDay+'/'+todayMon+'/'+date.today().strftime("%Y"))
# # plt.xlabel('Days since first case')
# # plt.ylabel('Numbers of cases')
