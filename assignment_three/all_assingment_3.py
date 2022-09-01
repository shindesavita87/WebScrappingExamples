import requests
"""
WEB SCRAPING-ASSIGNMENT3
 Instructions:
 • All questions are compulsory.
• In each of the questions you have to automate the process. You do not have to click on any button, click
any clickable element, enter keywords in search boxes manually. Each process has to be performed via
coding.
• Q1 and Q2 are connected questions i.e. after attempting Q1 proceed to Q2. Do not write whole code
from beginning for Q2.
• You may use any web scraping library and tools.
• The question can be attempted in various ways; the correctness of question depends on the output.
• If you encounter any Null values during scraping, you may replace it by hyphen.
Exercise:
1. Write a python program which searches all the product under a particular product from www.amazon.in. The product to be searched will be taken as input from user. For e.g. If user input is ‘guitar’. Then search for guitars.
2. In the above question, now scrape the following details of each product listed in first 3 pages of your search results and save it in a data frame and csv. In case if any product has less than 3 pages in search results then scrape all the products available under that product name. Details to be scraped are: "Brand Name", "Name of the Product", "Price", "Return/Exchange", "Expected Delivery", "Availability" and “Product URL”. In case, if any of the details are missing for any of the product then replace it by “-“.
3. Write a python program to access the search bar and search button on images.google.com and scrape 10 images each for keywords ‘fruits’, ‘cars’ and ‘Machine Learning’, ‘Guitar’, ‘Cakes’.
4. Write a python program to search for a smartphone(e.g.: Oneplus Nord, pixel 4A, etc.) on www.flipkart.com and scrape following details for all the search results displayed on 1st page. Details to be scraped: “Brand Name”, “Smartphone name”, “Colour”, “RAM”, “Storage(ROM)”, “Primary Camera”, “Secondary Camera”, “Display Size”, “Battery Capacity”, “Price”, “Product URL”. Incase if any of the details is missing then replace it by “- “. Save your results in a dataframe and CSV.
5. Write a program to scrap geospatial coordinates (latitude, longitude) of a city searched on google maps.
6. Write a program to scrap details of all the funding deals for second quarter (i.e Jan 21 – March 21) from trak.in.
7. Write a program to scrap all the available details of best gaming laptops from digit.in.
8. Write a python program to scrape the details for all billionaires from www.forbes.com. Details to be
scrapped: “Rank”, “Name”, “Net worth”, “Age”, “Citizenship”, “Source”, “Industry”.
9. Write a program to extract at least 500 Comments, Comment upvote and time when comment was posted
from any YouTube Video.
10. Write a python program to scrape a data for all available Hostels from https://www.hostelworld.com/ in
“London” location. You have to scrape hostel name, distance from city centre, ratings, total reviews, overall reviews, privates from price, dorms from price, facilities and property description
"""


