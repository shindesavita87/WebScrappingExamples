import inspect
import time
import requests
from IPython.core.display_functions import display
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchWindowException, WebDriverException, NoSuchElementException
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

"""
Scrape the details of State-wise GDP of India from statisticstime.com. Url = http://statisticstimes.com/
You have to find following details:
A) Rank
B) State
C) GSDP
D) GSDP
E) Share
F) GDP($ billion)
Note: - From statistics times home page you have to reach to economy page through code.
"""


class StateWiseGDP:
    def __init__(self):
        self.driver = None

    def open_browser(self):
        try:
            # Set chrome options
            opt = Options()
            opt.add_argument("--disable-infobars")
            opt.add_argument("--disable-extensions")
            opt.add_argument('--log-level=OFF')
            opt.add_experimental_option('excludeSwitches', ['enable-logging'])

            url = "https://www.statisticstimes.com/"

            # Download and install required driver
            self.driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=opt)

            # Maximizing the browser window
            self.driver.maximize_window()

            # Website URL
            self.driver.get(url)

            # Wait till the page has been loaded
            time.sleep(5)
        except (NoSuchWindowException, WebDriverException) as err:
            print(err.msg + "Error while calling " + inspect.stack()[0][3])
        except:
            print("Error while calling " + inspect.stack()[0][3])

    def go_to_gdp_of_indian_state_page(self):

        # Getting current URL source code
        expected_title = "StatisticsTimes.com | Collection of Statistics and charts"
        print("Actual Title: " + self.driver.title)

        # Assert title of the page & Handled assertion error
        try:
            assert expected_title in self.driver.title
        except AssertionError:
            print("This is assertion error " + inspect.stack()[0][3])

        try:
            # identify element which will return contributor name
            ele = self.driver.find_elements(By.XPATH, "//a[@class='cc-btn cc-dismiss' and text()='Got it!']")

            # check condition, if list size > 0, element exists
            if len(ele) > 0:
                ele[0].click()
                time.sleep(2)
            else:
                print("Accept cookies doen not exist..")

            self.driver.find_element(By.XPATH, "//button[contains(text(), 'Economy')]").click()
            self.driver.find_element(By.LINK_TEXT, 'India').click()
            if "#google_vignette" in self.driver.current_url:
                self.driver.refresh()
                time.sleep(2)
                self.driver.find_element(By.XPATH, "//button[contains(text(), 'Economy')]").click()
                self.driver.find_element(By.LINK_TEXT, 'India').click()

            self.driver.find_element(By.PARTIAL_LINK_TEXT, '» GDP of Indian states').click()
            time.sleep(5)
        except NoSuchElementException as exception:
            print("Element not found for..." + inspect.stack()[0][3])

    def extract_indian_state_gdp_data(self):
        table_headers = []
        ranks = []
        state_name = []
        gsdp_one = []
        gsdp_two = []
        shares = []
        gdp_data = []

        # Parsing through the webpage
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}

        try:
            results = requests.get(self.driver.current_url, headers=headers, timeout=3)
            # Raise error in case of failure
            results.raise_for_status()
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        except requests.exceptions.HTTPError as httpErr:
            print("Http Error:", httpErr)
        except requests.exceptions.ConnectionError as connErr:
            print("Error Connecting:", connErr)
        except requests.exceptions.Timeout as timeOutErr:
            print("Timeout Error:", timeOutErr)
        except requests.exceptions.RequestException as reqErr:
            print("Something Else:", reqErr)

            # Get product brand from product details page
            if results.status_code == 200:
                print("Hello...")
                main_div = soup.find('table', {'id': 'table_id'})
                print(main_div)
                th_div = main_div.find('thead').find_all('tr')[0].find_all('th')
                tr_div = main_div.find('tbody').find_all('tr')

                for j in range(len(th_div)):
                    header_row = th_div[j].text
                    table_headers.append(header_row)

                for i in range(len(tr_div)):
                    item = tr_div[i]

                    # Get ranks
                    try:
                        rank = item.find_all('td')[0].text
                        ranks.append(rank)
                    except AttributeError:
                        print("Unable to get ranks..")

                    # Get state name
                    try:
                        state = item.find_all('td')[1].text
                        state_name.append(state)
                    except AttributeError:
                        print("Unable to state name..")

                    # Get gsdp one
                    try:
                        gsdp1 = item.find_all('td')[2].text
                        gsdp_one.append(gsdp1)
                    except AttributeError:
                        print("Unable to gsdp one..")

                    # Get gsdp two
                    try:
                        gsdp2 = item.find_all('td')[3].text
                        gsdp_two.append(gsdp2)
                    except AttributeError:
                        print("Unable to get gsdp two..")

                    # Get shares
                    try:
                        share = item.find_all('td')[4].text
                        shares.append(share)
                    except AttributeError:
                        print("Unable to get shares..")

                    # Get gdp
                    try:
                        gdp = item.find_all('td')[5].text
                        gdp_data.append(gdp)
                    except AttributeError:
                        print("Unable to get gdp_data..")

            gdp_data = pd.DataFrame({table_headers[0]: ranks,
                                     table_headers[1]: state_name,
                                     table_headers[2]: gsdp_one,
                                     table_headers[3]: gsdp_two,
                                     table_headers[4]: shares,
                                     table_headers[5]: gdp_data})

            display(gdp_data)
            self.driver.close()


if __name__ == "__main__":
    state_gdp = StateWiseGDP()
    state_gdp.open_browser()
    state_gdp.go_to_gdp_of_indian_state_page()
    state_gdp.extract_indian_state_gdp_data()