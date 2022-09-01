import inspect
import time

import pandas as pd
import requests
from IPython.core.display_functions import display
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchWindowException, WebDriverException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 1000)

"""
5. Scrape the details of trending repositories on Github.com. Url = https://github.com/
You have to find the following details:
A) Repository title
B) Repository description C) Contributors count
D) Language used
Note: - From the home page you have to click on the trending option from Explore menu through code.
"""


def add_separator_to_the_list(a_list):
    converted_list = [str(element) for element in a_list]
    joined_string = "||".join(converted_list)
    return joined_string


class GithubTrendingRepoData:
    def __init__(self):
        # Parsing through the webpage
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
        self.driver = None

    def open_browser(self):
        try:
            # Set chrome options
            opt = Options()
            opt.add_argument("--disable-infobars")
            opt.add_argument("--disable-extensions")
            opt.add_argument('--log-level=OFF')
            opt.add_argument("--start-maximized")
            opt.add_experimental_option('excludeSwitches', ['enable-logging'])

            url = "https://github.com/"

            # Download and install required driver
            self.driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=opt)

            # Website URL
            self.driver.get(url)

            # Wait till the page has been loaded
            time.sleep(3)

            # Maximizing the browser window
            self.driver.maximize_window()

            # Getting current URL source code
            expected_title = "GitHub: Where the world builds software · GitHub".strip()
            print("Actual Title: " + self.driver.title)

            # Assert title of the page & Handled assertion error
            try:
                assert expected_title in self.driver.title.strip()
            except AssertionError:
                print("This is main title assertion error " + inspect.stack()[0][3])

            # set implicit wait time
            self.driver.implicitly_wait(60)
        except (NoSuchWindowException, WebDriverException) as err:
            print(err.msg + "Error while calling " + inspect.stack()[0][3])
        except:
            print("Error while calling " + inspect.stack()[0][3])

    def go_to_trending_repo_page(self):
        try:
            actions = ActionChains(self.driver)
            menu = self.driver.find_element_by_xpath("//summary[contains(text(), 'Explore')]")
            actions.send_keys(Keys.TAB * 6).send_keys(Keys.ENTER).pause(10).perform()
            self.driver.find_element_by_link_text('Trending').click()
        except NoSuchElementException as exception:
            print("Element not found for..." + inspect.stack()[0][3] + exception.msg)

    def extract_github_trending_repo_information(self):
        repository_titles = []
        repository_description = []
        contributors_count = []
        language_used = []

        try:
            results = requests.get(self.driver.current_url, headers=self.headers, timeout=10)
            time.sleep(3)
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

        if results.status_code == 200:
            main_div = soup.find('div', {'class': 'position-relative container-lg p-responsive pt-6'})
            all_div = main_div.find_all('article', {'class': 'Box-row'})
            counter = 1
            for i in range(len(all_div)):

                current_div = all_div[i]
                # Get repository title
                try:
                    repo_title = current_div.find('h1', {'class': 'h3 lh-condensed'}).text
                    repository_titles.append(repo_title.strip().replace('\n', ""))
                except AttributeError:
                    print("Unable to get repository titles...")

                # Get repository description
                try:
                    repo_desc = current_div.find('p', {'class': 'col-9 color-fg-muted my-1 pr-4'}).text
                    repository_description.append(repo_desc.strip().replace('\n', ""))
                except AttributeError:
                    print("Unable to get repository description...")

                # Get contributor
                try:
                    # total_ele = self.driver.find_elements_by_xpath("//span[@class='d-inline-block mr-3']")
                    # print("Total List:" + str(len(total_ele)))

                    my_str_xpath = "(//span[@class='d-inline-block mr-3'])[{}]//a".format(counter);
                    print("Executing for element: " + my_str_xpath)
                    all_contributors_for_each = self.driver.find_elements_by_xpath(my_str_xpath)
                    temp_list = []
                    print("No of contributor in each project: " + str(len(all_contributors_for_each)))
                    # iterate through list and get text
                    for i in all_contributors_for_each:
                        act = ActionChains(self.driver)
                        # For mac
                        act.key_down(Keys.COMMAND).click(i).key_up(Keys.COMMAND).perform()
                        # For Windows
                        # act.key_down(Keys.CONTROL).click(i).key_up(Keys.CONTROL).perform()
                        time.sleep(2)
                        self.driver.switch_to.window(self.driver.window_handles[1])

                        # identify element which will return contributor name
                        ele = self.driver.find_elements_by_xpath("//h1[@class='vcard-names ']//span[1]")

                        # get list size with len
                        s = len(ele)
                        # check condition, if list size > 0, element exists
                        if s > 0:
                            name = ele[0].text
                            print("Name exist - " + name)
                        else:
                            print("Element does not exist")
                        self.driver.close()
                        time.sleep(2)
                        self.driver.switch_to.window(window_name=self.driver.window_handles[0])
                        temp_list.append(name.strip().replace('\n', ""))

                        print("temp_list: " + str(temp_list))
                    contributors_count.append(temp_list)
                except AttributeError:
                    print("Unable to find contributors details ...")

                # Get language used
                try:
                    lang = current_div.find('span', {'class': 'd-inline-block ml-0 mr-3'}).text
                    language_used.append(lang.strip().replace('\n', ""))
                except AttributeError:
                    print("Unable to get language used..")

                counter = counter + 1

        github_trending_repo_info = pd.DataFrame({'Repository Title': repository_titles,
                                                  'Repository Description': repository_description,
                                                  'Contributors Count': contributors_count,
                                                  'Language Used': language_used})

        display(github_trending_repo_info)

        print(add_separator_to_the_list(repository_titles), '\n', add_separator_to_the_list(repository_description),
              '\n',
              add_separator_to_the_list(contributors_count), '\n', add_separator_to_the_list(language_used))


if __name__ == "__main__":
    git_data = GithubTrendingRepoData()
    git_data.open_browser()
    git_data.go_to_trending_repo_page()
    git_data.extract_github_trending_repo_information()


"""
Sample Output:

"""
