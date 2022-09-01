"""
  In all the following questions, you have to use BeautifulSoup to scrape different websites and collect data as per the requirement of the question.
    Every answer to the question should be in form of a python function which should take URL as the parameter. Use Jupyter Notebooks to program, upload it on your GitHub and send the link of the Jupyter notebook to your SME.
    1) Write a python program to display all the header tags from wikipedia.org.
"""

from urllib.request import urlopen

from bs4 import BeautifulSoup


def display_all_header_tags(url):
    html = urlopen(url)

    bs = BeautifulSoup(html, "html.parser")

    titles = bs.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])

    print('List all the header tags :', *titles, sep='\n\n')


display_all_header_tags('https://en.wikipedia.org/wiki/Main_Page')
