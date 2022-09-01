"""
2) Write a python program to display IMDB’s Top rated 100 movies’ data (i.e. name, rating, year of release)
and make data frame.
"""
import pandas as pd
import requests
from IPython.core.display_functions import display
from bs4 import BeautifulSoup

pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 100)
pd.set_option('display.width', 100)


def DisplayImdbTopRatedMovies(url):
    results = requests.get(url)

    soup = BeautifulSoup(results.text, "html.parser")
    names = []
    years = []
    imdb_ratings = []

    movie_div = soup.find_all('div', class_='lister-item mode-advanced')

    for container in movie_div:
        name = container.h3.a.text

        names.append(name)

        year = container.h3.find('span', class_='lister-item-year').text

        years.append(year)

        imdb = float(container.strong.text)

        imdb_ratings.append(imdb)

    print(names,years,imdb_ratings)

    movie = pd.DataFrame({'Names of Movie': names,

                          'Release Year': years,

                          'IMDB Rating of Movie': imdb_ratings})
    print(movie)

    display(movie)


DisplayImdbTopRatedMovies('https://www.imdb.com/search/title/?count=100&groups=top_100&sort=user_rating')
