import csv
import os
import subprocess
import sys
import time
from datetime import date
import pandas as pd
import requests
from IPython.core.display_functions import display
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 100)

"""
    Step1: Open the Chrome browser and set the opetions
    Step2: Search for user given product 
    Step3: Extract the html content of all the products from that page
    Step4: Scrape details are: "Brand Name", "Name of the Product", "Price", "Return/Exchange", "Expected Delivery", "Availability" and “Product URL”. 
    Step5: In case, if any of the details are missing for any of the product then replace it by “-“.
    Step6: First 3 pages of your search results and save it in a data frame and csv
    Step7: In case if any product has less than 3 pages in search results then scrape all the products available under that product name
    Step8: Close the browser
"""


class ScrapAmazonData:
    def __init__(self):
        self.driver = None
        self.search_product_name = None
        self.removed_space_prod_name = None

    def open_browser(self):

        # Set chrome options
        opt = Options()
        opt.add_argument("--disable-infobars")
        opt.add_argument("--disable-extensions")
        opt.add_argument('--log-level=OFF')
        opt.add_experimental_option('excludeSwitches', ['enable-logging'])

        url = "https://www.amazon.in/"

        # Download and install required driver
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=opt)

        # Maximizing the browser window
        self.driver.maximize_window()

        # Website URL
        self.driver.get(url)

        # Wait till the page has been loaded
        time.sleep(2)

    def form_search_product_url(self):

        # Take product to search input from user
        self.search_product_name = input("\n>> Enter the product/category to be searched: ")

        # Remove the speaces if user entered in search word
        self.removed_space_prod_name = self.search_product_name.replace(" ", "+")

        # This is the product url format for all products
        category_url = "https://www.amazon.in/s?k={}&ref=nb_sb_noss"

        # Form url with search product name
        category_url = category_url.format(self.removed_space_prod_name)

        # Print formed url
        print("=>> Category URL: ", category_url)

        # Go to the product webpage
        self.driver.get(category_url)

        # Getting current URL source code
        actual_title = self.driver.title
        expected_title = "Amazon.in : " + self.search_product_name
        print("expected_title: " + expected_title)

        # Assert title of the page
        assert expected_title in self.driver.title

        # To be used later while navigating to different pages
        return category_url

    def extract_webpage_information(self):
        # Parsing through the webpage
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        # List of all the html information related to the product
        page_results = soup.find_all('div', {'data-component-type': 's-search-result'})

        return page_results

    @staticmethod
    def extract_product_information(page_results):
        temp_record = []
        for i in range(len(page_results)):
            item = page_results[i]

            # Find the a tag of the item
            a_tag_item = item.h2.a

            # Name of the item
            product_name = a_tag_item.text.strip()

            # Get the url of the item
            product_details_url = "https://www.amazon.in/" + a_tag_item.get('href')

            # Get product expected delivery date
            try:
                expected_delivery = item.find('span', text='Get it by ').next_sibling.text
            except AttributeError:
                expected_delivery = "-"

            # Get the price of the product
            try:
                product_price_location = item.find('span', 'a-price')
                product_price = product_price_location.find('span', 'a-offscreen').text
            except AttributeError:
                product_price = "-"

            # Goto category url in new tab to fetch the information
            # Parsing through the webpage
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
            try:
                results1 = requests.get(product_details_url, headers=headers, timeout=3)
                results1.raise_for_status()  # Raise error in case of failure
            except requests.exceptions.HTTPError as httpErr:
                print("Http Error:", httpErr)
            except requests.exceptions.ConnectionError as connErr:
                print("Error Connecting:", connErr)
            except requests.exceptions.Timeout as timeOutErr:
                print("Timeout Error:", timeOutErr)
            except requests.exceptions.RequestException as reqErr:
                print("Something Else:", reqErr)

                time.sleep(1)
                soup1 = BeautifulSoup(results1.text, 'html.parser')

            # Get product brand from product details page
            if results1.status_code == 200:
                try:
                    brand_div = soup1.find('div', {'id': 'centerCol'})
                    tr_brand = brand_div.find('tr', {'class': 'a-spacing-small po-brand'})
                    brand_name = tr_brand.find_all('td')[1].text
                except AttributeError:
                    brand_name = "-"

                try:
                    return_policy = soup1.find('div', {'data-name': 'RETURNS_POLICY'}).find_all('div')[1].get(
                        'alt').strip()
                except AttributeError:
                    return_policy = "-"

                try:
                    delivery_details_div = soup1.find('div', {'id': 'rightCol'})
                    in_stock = delivery_details_div.find('div', {'id': 'availability'}).span.text
                except AttributeError:
                    in_stock = "-"

            # Store the product information in a tuple
            product_information = (
                brand_name, product_name, product_price[1:], return_policy, expected_delivery, in_stock,
                product_details_url)

            # Store the information in a temporary record
            temp_record.append(product_information)

        return temp_record

    def navigate_to_other_pages(self, category_url):
        # Contains the list of all the product's information
        records = []

        print("\n>> Page 1 - webpage information extracted")

        try:
            max_number_of_pages = "//span[@class='s-pagination-item s-pagination-disabled']"
            number_of_pages = self.driver.find_element_by_xpath(max_number_of_pages)
            print("Maximum Pages: ", number_of_pages.text)

        except NoSuchElementException:
            max_number_of_pages = "//li[@class='a-normal'][last()]"
            number_of_pages = self.driver.find_element_by_xpath(max_number_of_pages)

        for i in range(2, 4):
            # Goes to next page
            next_page_url = category_url + "&page=" + str(i)
            self.driver.get(next_page_url)

            # Webpage information is stored in page_results
            page_results = self.extract_webpage_information()
            temp_record = self.extract_product_information(page_results)

            extraction_information = "=>> Page {} - webpage information extracted"
            print(extraction_information.format(i))

            for j in temp_record:
                records.append(j)

        self.driver.close()

        print("\n=>> Creating an excel sheet and entering the details...")

        # prod_info = pd.DataFrame(records, columns=['Brand Name', 'Name of the Product', 'Price', 'Return Exchange',
        #                                            'Expected Delivery', 'Availability', 'Product URL'])
        # display(prod_info)

        return records

    def product_information_spreadsheet(self, records):

        today = date.today().strftime("%d-%m-%Y")

        for _ in records:
            file_name = "{}_{}.csv".format(self.search_product_name, today)
            f = open(file_name, "w", newline='', encoding='utf-8')
            writer = csv.writer(f)
            writer.writerow(
                ['Brand Name', 'Product Name', 'Price', 'Return Policy', 'Expected Delivery', 'Product Availability',
                 'Product URL'])
            writer.writerows(records)
            f.close()

        message = "=>> Information about the product '{}' is stored in {}\n".format(self.search_product_name, file_name)

        # os.startfile(file_name)
        if sys.platform == "win32":
            os.startfile(file_name)
        else:
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, file_name])


if __name__ == "__main__":
    my_amazon_bot = ScrapAmazonData()

    my_amazon_bot.open_browser()

    category_details = my_amazon_bot.form_search_product_url()

    my_amazon_bot.extract_product_information(my_amazon_bot.extract_webpage_information())

    navigation = my_amazon_bot.navigate_to_other_pages(category_details)

    my_amazon_bot.product_information_spreadsheet(navigation)
