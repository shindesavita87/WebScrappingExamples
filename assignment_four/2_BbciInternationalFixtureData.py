import inspect
import time
import requests
from IPython.core.display_functions import display
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchWindowException, WebDriverException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

"""
Scrape the details team India’s international fixtures from bcci.tv. Url = https://www.bcci.tv/.
You need to find following details:
A) Match title (I.e. 1st ODI)
B) Series
C) Place
D) Date
E) Time
Note: - From bcci.tv home page you have reach to the international fixture page through code.
"""


class BbciInternationalFixtureData:
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

            url = "https://www.bcci.tv/"

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

    def go_to_international_fixture_page(self):

        # Getting current URL source code
        expected_title = "The Board of Control for Cricket in India".strip()
        print("Actual Title: " + self.driver.title)

        # Assert title of the page & Handled assertion error
        try:
            assert expected_title in self.driver.title.strip()
        except AssertionError:
            print("This is assertion error " + inspect.stack()[0][3])

        try:
            self.driver.find_element_by_link_text("INTERNATIONAL").click()
        except NoSuchElementException as exception:
            print("Element not found for..." + inspect.stack()[0][3])

        # Wait till the page has been loaded
        time.sleep(5)

    def extract_international_fixture_information(self):
        match_titles = []
        series_names = []
        place_name = []
        date_played = []
        time_played = []

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
            main_div = soup.find_all('div', {'class': 'tab-inner-content'})[0]
            all_div = main_div.find_all('div', {'class': 'fixture-card-main col-lg-3 col-md-6 col-sm-12 ng-scope'})

            for i in range(len(all_div)):

                series_div = all_div[i].find('div', {
                    'class': 'fixture-card-mid d-flex align-items-center justify-content-between'})
                title_div = all_div[i].find('div',
                                            {'class': 'fixture-card-top'})
                date_time_div = all_div[i].find('div', {
                    'class': 'match-top-info d-flex align-items-center justify-content-between'})
                location_div = all_div[i].find('div', {'class': 'fixture-card-bottom'})

                # Get match title
                try:
                    match = title_div.find_all('h5')[1].text
                    match_titles.append(match)
                except AttributeError:
                    print("Unable to get match title..")

                # Get series name
                try:
                    series = series_div.find_all('h5')[0].text + ' vs ' + series_div.find_all('h5')[1].text
                    series_names.append(series)
                except AttributeError:
                    print("Unable to get series..")

                # Get place name
                try:
                    place = location_div.text
                    place_name.append(place)
                except AttributeError:
                    print("Unable to get place..")

                # Get date
                try:
                    date = date_time_div.find_all('div')[0].text
                    date_played.append(date)
                except AttributeError:
                    print("Unable to get date..")

                # Get time
                try:
                    time_before = date_time_div.find_all('h5')[1].text
                    time_after = time_before.replace('Women’s U-19', '')
                    time_played.append(time_after)
                except AttributeError:
                    print("Unable to get time..")

            bbci_fixture_info = pd.DataFrame({'Match Title': match_titles,
                                              'Name of Series': series_names,
                                              'Location Played': place_name,
                                              'Date': date_played,
                                              'Time': time_played})

            display(bbci_fixture_info)

            print(match_titles, series_names, place_name, date_played, time_played)
            self.driver.close()


if __name__ == "__main__":
    bbci_data = BbciInternationalFixtureData()
    bbci_data.open_browser()
    bbci_data.go_to_international_fixture_page()
    bbci_data.extract_international_fixture_information()


"""
Sample Output:
Match Title	Name of Series	Location Played	Date	Time
0	ICC WOMENS WORLD CUP 2022	India Women vs South Africa Women	Hagley Oval, Christchurch Match Centre	27 MAR 2022 Monday	6:30 am IST
1	SOUTH AFRICA TOUR OF INDIA T20 SERIES 2022	India vs South Africa	1st T20I - MA Chidambaram Stadium, ChennaiMatc...	9 JUN 2022 Monday	7:30 pm IST
2	SOUTH AFRICA TOUR OF INDIA T20 SERIES 2022	India vs South Africa	2nd T20I - M Chinnaswamy Stadium, BengaluruMa...	12 JUN 2022 Monday	7:30 pm IST
3	SOUTH AFRICA TOUR OF INDIA T20 SERIES 2022	India vs South Africa	3rd T20I - Vidarbha Cricket Association Stadi...	14 JUN 2022 Monday	7:30 pm IST
4	SOUTH AFRICA TOUR OF INDIA T20 SERIES 2022	India vs South Africa	4th T20I - Saurashtra Cricket Association Sta...	17 JUN 2022 Monday	7:30 pm IST
5	SOUTH AFRICA TOUR OF INDIA T20 SERIES 2022	India vs South Africa	5th T20I - Arun Jaitley Stadium, DelhiMatch C...	19 JUN 2022 Monday	7:30 pm IST
['ICC WOMENS WORLD CUP 2022', 'SOUTH AFRICA TOUR OF INDIA T20 SERIES 2022', 'SOUTH AFRICA TOUR OF INDIA T20 SERIES 2022', 'SOUTH AFRICA TOUR OF INDIA T20 SERIES 2022', 'SOUTH AFRICA TOUR OF INDIA T20 SERIES 2022', 'SOUTH AFRICA TOUR OF INDIA T20 SERIES 2022'] ['India Women vs South Africa Women', 'India vs South Africa', 'India vs South Africa', 'India vs South Africa', 'India vs South Africa', 'India vs South Africa'] ['Hagley Oval, Christchurch Match Centre', '1st T20I - MA Chidambaram Stadium, ChennaiMatch Centre', '2nd  T20I - M Chinnaswamy Stadium, BengaluruMatch Centre', '3rd  T20I - Vidarbha Cricket Association Stadium, NagpurMatch Centre', '4th  T20I - Saurashtra Cricket Association Stadium, RajkotMatch Centre', '5th  T20I - Arun Jaitley Stadium, DelhiMatch Centre'] ['27 MAR 2022 Monday', '9 JUN 2022 Monday', '12 JUN 2022 Monday', '14 JUN 2022 Monday', '17 JUN 2022 Monday', '19 JUN 2022 Monday'] ['6:30 am IST ', '7:30 pm IST ', '7:30 pm IST ', '7:30 pm IST ', '7:30 pm IST ', '7:30 pm IST ']
"""