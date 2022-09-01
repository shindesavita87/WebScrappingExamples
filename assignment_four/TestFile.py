import inspect
import time
import requests
from IPython.core.display_functions import display
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchWindowException, WebDriverException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import re

match_titles = []
series_names = []
place_name = []
dates_played = []
times_played = []
opt = Options()
opt.add_argument("--disable-infobars")
opt.add_argument("--disable-extensions")
opt.add_argument('--log-level=OFF')
opt.add_experimental_option('excludeSwitches', ['enable-logging'])

url = "https://www.bcci.tv/"

# Download and install required driver
driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=opt)

# Maximizing the browser window
driver.maximize_window()

# Website URL
driver.get(url)
driver.find_element_by_xpath('//button[@class="cookie__accept btn btn-primary"]').click()

# Wait till the page has been loaded
time.sleep(5)
driver.find_element_by_link_text("INTERNATIONAL").click()

# Wait till the page has been loaded
time.sleep(5)

# Parsing through the webpage
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}

results = requests.get(driver.current_url, headers=headers, timeout=3)
soup = BeautifulSoup(driver.page_source, 'html.parser')

main_div = soup.find_all('div', {'class': 'tab-inner-content'})[0]

series_div = main_div.find_all('div', {'class': 'fixture-card-mid d-flex align-items-center justify-content-between'})

final_str = series_div[0].find_all('h5')[0].text + ' vs ' + series_div[0].find_all('h5')[1].text

print("series: " + final_str)

title_div = main_div.find_all('div', {'class': 'fixture-card-top'})

print("title : " + title_div[0].find_all('h5')[1].text)

date_time_div = main_div.find_all('div', {'class': 'match-top-info d-flex align-items-center justify-content-between'})

print("date: "+ date_time_div[0].find_all('div')[0].text)

time = date_time_div[0].find_all('h5')[1].text
print("time: "+ time.replace('Women’s U-19',''))

location_div = main_div.find_all('div', {'class': 'fix-place ng-binding ng-scope'})

print("location: "+location_div[0].text)




# s1 = card_div[0].text.strip()
# pattern = 'vs'
# print(s1)
# print("Output "+str(s1.find("vs")))
# print(re.search(pattern, s1).span())
#
#
#
# s2 = card_div[1].text.strip()
# print(s2)
# print("Output "+str(s2.find("vs")))
# print(re.search(pattern, s2).span())

#
# s3 = card_div[2].text.strip()
# print(s3)
# print("Output "+str(s3.find("vs")))
# print(re.search(pattern, s3).span())
