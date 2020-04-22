import pandas as pd 
from selenium import webdriver
from bs4 import BeautifulSoup
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint as pp
import datetime
import time


epoch = time.time()
daysEpoch = int(float(epoch)/86400)

covidEpoch = datetime.datetime(2020, 4, 22, 0, 0).timestamp()
covidDaysEpoch = int(float(covidEpoch)/86400)

covidDelta = daysEpoch - covidDaysEpoch

now = datetime.datetime.now()
today = now.strftime("%d/%m/%Y")

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)
sheet = client.open('Covid-19 Australia Numbers').sheet1
result = sheet.row_values(2)

driver = webdriver.Chrome("D:\Programming\chromedriver.exe")
driver.get("https://www.health.gov.au/news/health-alerts/novel-coronavirus-2019-ncov-health-alert/coronavirus-covid-19-current-situation-and-case-numbers")
states = [today]
content = driver.page_source
soup = BeautifulSoup(content, features="html.parser")

for td in soup.findAll("td", {"class": "numeric"}):
    x = td.text
    x = x.replace(',', '')
    x = x.replace('\n', '')
    x = x.replace(' ', '')
    states.append(x)

for item in states:
    column = states.index(item)
    column += 1
    sheet.update_cell(41 + covidDelta, column, item)