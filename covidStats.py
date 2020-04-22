# import pandas as pd 
from selenium import webdriver
from bs4 import BeautifulSoup
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint as pp
import datetime
import time
from sys import platform
print(platform)

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
print("Google Sheets (CONNECTED)")

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
print("Google Options Set")
osPath = ""
if platform == "linux" or platform == "linux2":
    osPath = "/home/oliver/covidStats/chromedriverLin"
elif platform == "win32":
    osPath = "D:\Programming\CovidStats\chromedriverWin.exe"
driver = webdriver.Chrome(osPath,chrome_options=chrome_options)
print("Chromedriver initialised")

driver.get("https://www.health.gov.au/news/health-alerts/novel-coronavirus-2019-ncov-health-alert/coronavirus-covid-19-current-situation-and-case-numbers")
print("Health.gov.au retrieved")
states = [today]
content = driver.page_source
soup = BeautifulSoup(content, features="html.parser")

print("Starting search")
for td in soup.findAll("td", {"class": "numeric"}):
    x = td.text
    x = x.replace(',', '')
    x = x.replace('\n', '')
    x = x.replace(' ', '')
    states.append(x)
print("Search completed, beginning Google Sheets input")

for item in states:
    column = states.index(item)
    column += 1
    sheet.update_cell(41 + covidDelta, column, item)

print("Input completed, Inputted values are as followed:")
print(sheet.row_values(41 +covidDelta))