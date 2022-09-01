"""
4) Write a python program to scrape product name, price and discounts from https://meesho.com/bags-
ladies/pl/p7vbp .
"""

import re
import pandas as pd
import requests
from IPython.core.display_functions import display
from bs4 import BeautifulSoup


def display_product_name_price_discount(url):
    results = requests.get(url)

    soup = BeautifulSoup(results.text, "html.parser")

    product_names = []

    product_price = []

    discounts = []

    bags_div = soup.find_all('div', class_='sc-dkPtRN ProductList__GridCol-sc-8lnc8o-0 FjWWx jMkQHN')

    for container in bags_div:
        product_name = container.div.p.text

        product_names.append(product_name)

        price = container.div.h5.text

        # price = re.sub("\D", "", price)

        product_price.append(price)

        discount = container.div.span.text

        # Extract digit string

        discount = re.sub("\D", "", discount)

        discounts.append(discount + '%')

    # print(product_names,product_price,discounts)    

    products = pd.DataFrame({'Product Name': product_names,

                             'Product Price': product_price,

                             'Product Discount': discounts})

    display(products)


display_product_name_price_discount('https://meesho.com/bags-ladies/pl/p7vbp')
