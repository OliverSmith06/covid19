# import pandas as pd 
from selenium import webdriver
from bs4 import BeautifulSoup
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint as pp
import datetime
import time
from time import sleep
from sys import platform
from apscheduler.schedulers.blocking import BlockingScheduler
print(platform)

epoch = time.time()
daysEpoch = int(float(epoch)/86400)

covidEpoch = datetime.datetime(2020, 4, 22, 0, 0).timestamp()
covidDaysEpoch = int(float(covidEpoch)/86400)

covidDelta = daysEpoch - covidDaysEpoch

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)
sheet = client.open('Covid-19 Australia Numbers').sheet1
print("Google Sheets (CONNECTED)")

chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument('--headless')
#chrome_options.add_argument('--no-sandbox')
#chrome_options.add_argument('--disable-dev-shm-usage')
print("Google Options Set")
osPath = ""
if platform == "linux" or platform == "linux2":
    osPath = "/home/oliver/covidStats/chromedriverLin"
elif platform == "win32":
    osPath = "D:\Programming\CovidStats\chromedriverWin.exe"
driver = webdriver.Chrome(osPath,chrome_options=chrome_options)
print("Chromedriver initialised")

now = datetime.datetime.now()
today = now.strftime("%d/%m/%Y")
driver.get("https://www.health.gov.au/news/health-alerts/novel-coronavirus-2019-ncov-health-alert/coronavirus-covid-19-current-situation-and-case-numbers")
print("Health.gov.au retrieved")
states = [today]
print("Starting search")
sleep(5)
ACT = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div/main/div/div/div/div[5]/div/div/div/article/div/div/article/div[1]/div/div/div/div[2]/div[1]/div/table/tbody/tr[2]/td[2]/div/div/span').text
states.append(ACT)

NSW = driver.find_element_by_xpath('//*[@id="RHjRJ"]/div/article/div[1]/div/div/div/div[2]/div[1]/div/table/tbody/tr[3]/td[2]/div/div/span').text
states.append(NSW)

NT = driver.find_element_by_xpath('//*[@id="RHjRJ"]/div/article/div[1]/div/div/div/div[2]/div[1]/div/table/tbody/tr[4]/td[2]/div/div/span').text
states.append(NT)

QLD = driver.find_element_by_xpath('//*[@id="RHjRJ"]/div/article/div[1]/div/div/div/div[2]/div[1]/div/table/tbody/tr[5]/td[2]/div/div/span').text
states.append(QLD)

SA = driver.find_element_by_xpath('//*[@id="RHjRJ"]/div/article/div[1]/div/div/div/div[2]/div[1]/div/table/tbody/tr[6]/td[2]/div/div/span').text
states.append(SA)

TAS = driver.find_element_by_xpath('//*[@id="RHjRJ"]/div/article/div[1]/div/div/div/div[2]/div[1]/div/table/tbody/tr[7]/td[2]/div/div/span').text
states.append(TAS)

VIC = driver.find_element_by_xpath('//*[@id="RHjRJ"]/div/article/div[1]/div/div/div/div[2]/div[1]/div/table/tbody/tr[8]/td[2]/div/div/span').text
states.append(VIC)

WA = driver.find_element_by_xpath('//*[@id="RHjRJ"]/div/article/div[1]/div/div/div/div[2]/div[1]/div/table/tbody/tr[9]/td[2]/div/div/span').text
states.append(WA)


print("Search completed, beginning Google Sheets input")

for item in states:
    column = states.index(item)
    column += 1
    sheet.update_cell(41 + covidDelta, column, item)

print("Input completed, Inputted values are as followed:")
print(sheet.row_values(41 +covidDelta))
input("Press Enter to continue...")
