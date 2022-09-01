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
9. Scrape the details most watched tv series of all time from imdb.com. Url = https://www.imdb.com/list/ls095964455/
You have to find the following details: A) Name
B) Year span
C) Genre
D) Run time E) Ratings F) Votes
"""


def add_separator_to_the_list(a_list):
    converted_list = [str(element) for element in a_list]
    joined_string = "||".join(converted_list)
    return joined_string


def extract_imdb_movie_information():
    movie_names = []
    movie_year_spans = []
    movie_genres = []
    movie_run_times = []
    movie_ratings = []
    movie_votes = []

    results = requests.get('https://www.imdb.com/list/ls095964455/', timeout=30)

    # Get product brand from product details page
    soup = BeautifulSoup(results.text, 'html.parser')
    if results.status_code == 200:
        main_div = soup.find('div', {'class': 'lister list detail sub-list'})
        all_div = main_div.find_all('div', {'class': 'lister-item mode-detail'})
        for i in range(len(all_div)):
            item = all_div[i]

            # Get movie name
            try:
                name = item.find('h3').find('a').text
                movie_names.append(name)
            except AttributeError:
                print("Error occurred while reading movie name...")

            # Get movie year spans
            try:
                year_spans = item.find('span', {'class': 'lister-item-year text-muted unbold'}).text
                movie_year_spans.append(year_spans)
            except AttributeError:
                print("Error occurred while reading movie year spans...")

            # Get movie genres
            try:
                genres = item.find('span', {'class': 'genre'}).text
                movie_genres.append(genres.strip().replace('\n', ""))
            except AttributeError:
                print("Error occurred while reading movie genres...")

            # Get movie run times
            try:
                run_times = item.find('span', {'class': 'runtime'}).text
                movie_run_times.append(run_times)
            except AttributeError:
                print("Error occurred while reading movie run times...")

            # Get movie ratings
            try:
                ratings = item.find('span', {'class': 'ipl-rating-star__rating'}).text
                movie_ratings.append(ratings)
            except AttributeError:
                print("Error occurred while reading movie ratings...")

            # Get movie votes
            try:
                votes = item.find('span', {'name': 'nv'}).text
                movie_votes.append(votes)
            except AttributeError:
                print("Error occurred while reading movie votes...")

    # print(add_separator_to_the_list(movie_names), '\n',
    #       add_separator_to_the_list(movie_year_spans),'\n',
    #       add_separator_to_the_list(movie_genres), '\n',
    #       add_separator_to_the_list(movie_run_times),'\n',
    #       add_separator_to_the_list(movie_ratings), '\n',
    #       add_separator_to_the_list(movie_votes), '\n')

    imdb_movie_info = pd.DataFrame({'Movie Name': movie_names,
                                    'Movie Year Span': movie_year_spans,
                                    'Movie Genres': movie_genres,
                                    'Movie Run Times': movie_run_times,
                                    'Movie Ratings': movie_ratings,
                                    'Movie Votes': movie_votes})

    display(imdb_movie_info)
    #print(imdb_movie_info)


extract_imdb_movie_information()


"""
Sample Output:
Movie Name	Movie Year Span	Movie Genres	Movie Run Times	Movie Ratings	Movie Votes
0	Game of Thrones	(2011–2019)	Action, Adventure, Drama	57 min	9.3	1,967,161
1	Stranger Things	(2016– )	Drama, Fantasy, Horror	51 min	8.7	974,369
2	The Walking Dead	(2010–2022)	Drama, Horror, Thriller	44 min	8.3	937,230
3	13 Reasons Why	(2017–2020)	Drama, Mystery, Thriller	60 min	7.6	280,304
4	The 100	(2014–2020)	Drama, Mystery, Sci-Fi	43 min	7.7	240,388
5	Orange Is the New Black	(2013–2019)	Comedy, Crime, Drama	59 min	8.1	293,990
6	Riverdale	(2017– )	Crime, Drama, Mystery	45 min	6.8	137,905
7	Grey's Anatomy	(2005– )	Drama, Romance	41 min	7.8	290,274
8	The Flash	(2014– )	Action, Adventure, Drama	43 min	7.7	334,419
9	Arrow	(2012–2020)	Action, Adventure, Crime	42 min	7.7	424,346
10	La casa de papel	(2017–2021)	Action, Crime, Drama	70 min	8.3	450,985
11	The Big Bang Theory	(2007–2019)	Comedy, Romance	22 min	8.2	777,107
12	Black Mirror	(2011–2019)	Drama, Mystery, Sci-Fi	60 min	8.8	509,672
13	Sherlock	(2010–2017)	Crime, Drama, Mystery	88 min	9.1	884,734
14	Vikings	(2013–2020)	Action, Adventure, Drama	44 min	8.6	501,165
15	Pretty Little Liars	(2010–2017)	Drama, Mystery, Romance	44 min	7.6	162,141
16	The Vampire Diaries	(2009–2017)	Drama, Fantasy, Horror	43 min	7.9	308,679
17	American Horror Story	(2011– )	Drama, Horror, Sci-Fi	60 min	8.1	305,822
18	Breaking Bad	(2008–2013)	Crime, Drama, Thriller	49 min	9.5	1,691,816
19	Lucifer	(2016–2021)	Crime, Drama, Fantasy	42 min	8.2	305,987
20	Supernatural	(2005–2020)	Drama, Fantasy, Horror	44 min	8.6	425,292
21	Prison Break	(2005–2017)	Action, Crime, Drama	44 min	8.4	514,112
22	How to Get Away with Murder	(2014–2020)	Crime, Drama, Mystery	43 min	8.2	145,462
23	Teen Wolf	(2011–2017)	Action, Drama, Fantasy	41 min	7.9	141,491
24	The Simpsons	(1989– )	Animation, Comedy	22 min	8.7	392,228
25	Once Upon a Time	(2011–2018)	Adventure, Fantasy, Romance	60 min	7.9	219,337
26	Narcos	(2015–2017)	Biography, Crime, Drama	49 min	8.8	401,001
27	Daredevil	(2015–2018)	Action, Crime, Drama	54 min	8.7	413,970
28	Friends	(1994–2004)	Comedy, Romance	22 min	9	942,140
29	How I Met Your Mother	(2005–2014)	Comedy, Romance	22 min	8.4	657,600
30	Suits	(2011–2019)	Comedy, Drama	44 min	8.5	392,444
31	Mr. Robot	(2015–2019)	Crime, Drama, Thriller	49 min	8.6	370,752
32	The Originals	(2013–2018)	Drama, Fantasy, Horror	45 min	8.4	130,506
33	Supergirl	(2015–2021)	Action, Adventure, Drama	43 min	6.3	121,341
34	Gossip Girl	(2007–2012)	Drama, Romance	42 min	7.5	168,509
35	Sense8	(2015–2018)	Drama, Mystery, Sci-Fi	60 min	8.3	150,650
36	Gotham	(2014–2019)	Action, Crime, Drama	42 min	7.9	224,202
37	Westworld	(2016– )	Drama, Mystery, Sci-Fi	62 min	8.6	470,306
38	Jessica Jones	(2015–2019)	Action, Crime, Drama	56 min	7.9	207,674
39	Modern Family	(2009–2020)	Comedy, Drama, Romance	22 min	8.5	405,299
40	Rick and Morty	(2013– )	Animation, Adventure, Comedy	23 min	9.2	467,114
41	Shadowhunters: The Mortal Instruments	(2016–2019)	Action, Drama, Fantasy	42 min	6.8	60,427
42	The End of the F***ing World	(2017–2019)	Adventure, Comedy, Crime	25 min	8.1	175,162
43	House of Cards	(2013–2018)	Drama	51 min	8.7	492,013
44	Dark	(2017–2020)	Crime, Drama, Mystery	60 min	8.8	349,577
45	Élite	(2018– )	Crime, Drama, Thriller	60 min	7.5	69,887
46	Sex Education	(2019– )	Comedy, Drama	45 min	8.4	254,230
47	Shameless	(2011–2021)	Comedy, Drama	46 min	8.6	227,922
48	New Girl	(2011–2018)	Comedy, Romance	22 min	7.8	214,275
49	Agents of S.H.I.E.L.D.	(2013–2020)	Action, Adventure, Drama	45 min	7.6	212,534
50	You	(2018– )	Crime, Drama, Romance	45 min	7.8	223,165
51	Dexter	(2006–2013)	Crime, Drama, Mystery	53 min	8.7	708,702
52	Fear the Walking Dead	(2015– )	Drama, Horror, Sci-Fi	44 min	6.9	125,348
53	Family Guy	(1999– )	Animation, Comedy	22 min	8.2	324,482
54	The Blacklist	(2013– )	Crime, Drama, Mystery	43 min	8.1	234,821
55	Lost	(2004–2010)	Adventure, Drama, Fantasy	44 min	8.4	533,466
56	Peaky Blinders	(2013–2022)	Crime, Drama	60 min	8.8	468,675
57	House M.D.	(2004–2012)	Drama, Mystery	44 min	8.8	445,507
58	Quantico	(2015–2018)	Crime, Drama, Mystery	42 min	6.6	60,044
59	Orphan Black	(2013–2017)	Drama, Sci-Fi, Thriller	44 min	8.3	108,143
60	Homeland	(2011–2020)	Crime, Drama, Mystery	55 min	8.4	333,580
61	Blindspot	(2015–2020)	Action, Crime, Drama	42 min	7.4	72,021
62	Legends of Tomorrow	(2016– )	Action, Adventure, Drama	42 min	6.9	101,853
63	The Handmaid's Tale	(2017– )	Drama, Sci-Fi, Thriller	60 min	8.4	214,298
64	Chilling Adventures of Sabrina	(2018–2020)	Drama, Fantasy, Horror	60 min	7.5	89,310
65	The Good Doctor	(2017– )	Drama	41 min	8.2	86,777
66	Jane the Virgin	(2014–2019)	Comedy	60 min	8	46,941
67	Glee	(2009–2015)	Comedy, Drama, Music	44 min	6.9	144,728
68	South Park	(1997– )	Animation, Comedy	22 min	8.8	357,028
69	Brooklyn Nine-Nine	(2013–2021)	Comedy, Crime	22 min	8.5	288,713
70	Under the Dome	(2013–2015)	Drama, Mystery, Sci-Fi	43 min	6.6	105,072
71	The Umbrella Academy	(2019– )	Action, Adventure, Comedy	60 min	8	198,441
72	True Detective	(2014–2019)	Crime, Drama, Mystery	55 min	8.9	541,778
73	The OA	(2016–2019)	Drama, Fantasy, Mystery	60 min	7.9	100,944
74	Desperate Housewives	(2004–2012)	Comedy, Drama, Mystery	45 min	7.6	125,198
75	Better Call Saul	(2015–2022)	Crime, Drama	46 min	8.8	385,732
76	Bates Motel	(2013–2017)	Drama, Horror, Mystery	45 min	8.2	104,756
77	The Punisher	(2017–2019)	Action, Crime, Drama	53 min	8.5	216,901
78	Atypical	(2017–2021)	Comedy, Drama	30 min	8.3	82,383
79	Dynasty	(2017– )	Drama	42 min	7.4	20,850
80	This Is Us	(2016–2022)	Comedy, Drama, Romance	45 min	8.7	129,155
81	The Good Place	(2016–2020)	Comedy, Drama, Fantasy	22 min	8.2	145,497
82	Iron Fist	(2017–2018)	Action, Adventure, Crime	55 min	6.5	126,115
83	The Rain	(2018–2020)	Drama, Sci-Fi, Thriller	45 min	6.3	35,395
84	Mindhunter	(2017–2019)	Crime, Drama, Mystery	60 min	8.6	264,405
85	Revenge	(2011–2015)	Drama, Mystery, Thriller	44 min	8	118,347
86	Luke Cage	(2016–2018)	Action, Crime, Drama	55 min	7.3	126,565
87	Scandal	(2012–2018)	Drama, Thriller	43 min	7.8	71,881
88	The Defenders	(2017)	Action, Adventure, Crime	50 min	7.3	102,294
89	Big Little Lies	(2017–2019)	Crime, Drama, Mystery	60 min	8.5	186,333
90	Insatiable	(2018–2019)	Comedy, Drama, Thriller	45 min	6.6	26,862
91	The Mentalist	(2008–2015)	Crime, Drama, Mystery	43 min	8.2	178,084
92	The Crown	(2016– )	Biography, Drama, History	58 min	8.7	188,675
93	Chernobyl	(2019)	Drama, History, Thriller	330 min	9.4	670,040
94	iZombie	(2015–2019)	Comedy, Crime, Drama	42 min	7.9	65,934
95	Reign	(2013–2017)	Drama, Fantasy	42 min	7.6	48,105
96	A Series of Unfortunate Events	(2017–2019)	Adventure, Comedy, Drama	50 min	7.8	58,798
97	Criminal Minds	(2005–2020)	Crime, Drama, Mystery	42 min	8.2	187,087
98	Scream	(2015–2019)	Comedy, Crime, Drama	45 min	7.1	39,669
99	The Haunting of Hill House	(2018)	Drama, Horror, Mystery	572 min	8.6	223,809
"""