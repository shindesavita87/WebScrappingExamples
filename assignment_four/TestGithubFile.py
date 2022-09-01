import inspect
import time
import requests
from IPython.core.display_functions import display
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchWindowException, WebDriverException, NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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

url = "https://github.com/trending"

# Download and install required driver
driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=opt)

# Maximizing the browser window
driver.maximize_window()

# Website URL
driver.get(url)

contributor_list = []
total_ele = driver.find_elements_by_xpath("//span[@class='d-inline-block mr-3']")
print("Total List:" + str(len(total_ele)))
counter = 1
for i in total_ele:
    strMyXPath = "(//span[@class='d-inline-block mr-3'])[{}]//a".format(counter);
    print(strMyXPath)
    all_contributors_for_each = driver.find_elements_by_xpath(strMyXPath)
    temp_list = []
    print("No of contributor in each project: " + str(len(all_contributors_for_each)))
    # iterate through list and get text
    for i in all_contributors_for_each:
        act = ActionChains(driver)
        # For mac
        act.key_down(Keys.COMMAND).click(i).key_up(Keys.COMMAND).perform()
        # For Windows
        # act.key_down(Keys.CONTROL).click(i).key_up(Keys.CONTROL).perform()
        time.sleep(5)
        driver.switch_to.window(driver.window_handles[1])

        # identify element
        ele = driver.find_elements_by_xpath("//h1[@class='vcard-names ']//span[1]")

        # get list size with len
        s = len(ele)
        # check condition, if list size > 0, element exists
        if s > 0:
            name = ele[0].text
            print("Name exist - " + name)
        else:
            print("Element does not exist")
        driver.close()
        time.sleep(5)
        driver.switch_to.window(window_name=driver.window_handles[0])
        temp_list.append(name.strip().replace('\n', ""))
    counter = counter + 1
    print("temp_list: "+str(temp_list))
print("Final list: " + str(contributor_list))

