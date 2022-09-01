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

pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 1000)

"""
Scrape the details of selenium exception from guru99.com. Url = https://www.guru99.com/
You need to find following details:
A) Name
B) Description
Note: - From guru99 home page you have to reach to selenium exception handling page through code.

"""


class ScrapGuru99ExceptionData:
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

            url = "https://www.guru99.com/"

            # Download and install required driver
            self.driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=opt)

            # Maximizing the browser window
            self.driver.maximize_window()

            # Website URL
            self.driver.get(url)

            # Wait till the page has been loaded
            time.sleep(5)
        except (NoSuchWindowException,WebDriverException) as err:
            print(err.msg + "Error while calling " + inspect.stack()[0][3])
        except:
            print("Error while calling " + inspect.stack()[0][3])

    def go_to_exception_handing_page(self):

        # Getting current URL source code
        expected_title = "Meet Guru99 – Free Training Tutorials & Video for IT Courses"
        print("expected_title: " + self.driver.title)

        # Assert title of the page
        # Handled assertion error
        try:
            assert expected_title in self.driver.title
        except AssertionError:
            print("This is assertion error " + inspect.stack()[0][3])

        try:
            self.driver.find_element_by_link_text("➤ Selenium").click()
            self.driver.find_element_by_xpath("//a[@title='Selenium Exception Handling (Common Exceptions List)']").click()
        except NoSuchElementException as exception:
            print("Element not found for..."+ inspect.stack()[0][3])

        # Wait till the page has been loaded
        time.sleep(5)

    def extract_exception_information(self):
        exception_names = []
        exception_descriptions = []

        # Parsing through the webpage
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}

        try:
            results = requests.get(self.driver.current_url, headers=headers, timeout=3)
            # Raise error in case of failure
            results.raise_for_status()
            soup = BeautifulSoup(results.text, 'html.parser')
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
            exception_div = soup.find('div', {'class': 'entry-content single-content'})
            all_tr = exception_div.find('table', {'class': 'table table-striped'}).find_all('tr')
            for i in range(1, len(all_tr)):
                item = all_tr[i]
                # Get exception name
                try:
                    exception_name = item.find_all('td')[0].text
                    exception_names.append(exception_name)
                except AttributeError:
                    print("Error occurred while reading exception name...")

                # Get exception description
                try:
                    exception_description = item.find_all('td')[1].text
                    exception_descriptions.append(exception_description)
                except AttributeError:
                    print("Error occurred while reading exception description...")

            exception_info = pd.DataFrame({'Exception Name': exception_names,
                                           'Exception Description': exception_descriptions})

            display(exception_info)
            self.driver.close()


if __name__ == "__main__":
    guru_data = ScrapGuru99ExceptionData()
    guru_data.open_browser()
    guru_data.go_to_exception_handing_page()
    guru_data.extract_exception_information()


"""
Sample Output:
Exception Name	Exception Description
0	ElementNotVisibleException	This type of Selenium exception occurs when an...
1	ElementNotSelectableException	This Selenium exception occurs when an element...
2	NoSuchElementException	This Exception occurs if an element could not ...
3	NoSuchFrameException	This Exception occurs if the frame target to b...
4	NoAlertPresentException	This Exception occurs when you switch to no pr...
5	NoSuchWindowException	This Exception occurs if the window target to ...
6	StaleElementReferenceException	This Selenium exception occurs happens when th...
7	SessionNotFoundException	The WebDriver is acting after you quit the bro...
8	TimeoutException	Thrown when there is not enough time for a com...
9	WebDriverException	This Exception takes place when the WebDriver ...
10	ConnectionClosedException	This type of Exception takes place when there ...
11	ElementClickInterceptedException	The command may not be completed as the elemen...
12	ElementNotInteractableException	This Selenium exception is thrown when any ele...
13	ErrorInResponseException	This happens while interacting with the Firefo...
14	ErrorHandler.UnknownServerException	Exception is used as a placeholder in case if ...
15	ImeActivationFailedException	This expectation will occur when IME engine ac...
16	ImeNotAvailableException	It takes place when IME support is unavailable.
17	InsecureCertificateException	Navigation made the user agent to hit a certif...
18	InvalidArgumentException	It occurs when an argument does not belong to ...
19	InvalidCookieDomainException	This happens when you try to add a cookie unde...
20	InvalidCoordinatesException	This type of Exception matches an interacting ...
21	InvalidElementStateExceptio	It occurs when command can’t be finished when ...
22	InvalidSessionIdException	This Exception took place when the given sessi...
23	InvalidSwitchToTargetException	This occurs when the frame or window target to...
24	JavascriptException	This issue occurs while executing JavaScript g...
25	JsonException	It occurs when you afford to get the session w...
26	NoSuchAttributeException	This kind of Exception occurs when the attribu...
27	MoveTargetOutOfBoundsException	It takes place if the target provided to the A...
28	NoSuchContextException	ContextAware does mobile device testing.
29	NoSuchCookieException	This Exception occurs when no cookie matching ...
30	NotFoundException	This Exception is a subclass of WebDriverExcep...
31	RemoteDriverServerException	This Selenium exception is thrown when the ser...
32	ScreenshotException	It is not possible to capture a screen.
33	SessionNotCreatedException	It happens when a new session could not be suc...
34	UnableToSetCookieException	This occurs if a driver is unable to set a coo...
35	UnexpectedTagNameException	Happens if a support class did not get a web e...
36	UnhandledAlertException	This expectation occurs when there is an alert...
37	UnexpectedAlertPresentException	It occurs when there is the appearance of an u...
38	UnknownMethodException	This Exception happens when the requested comm...
39	UnreachableBrowserException	This Exception occurs only when the browser is...
40	UnsupportedCommandException	This occurs when remote WebDriver does n’t sen...
"""