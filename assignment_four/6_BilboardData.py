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
6. Scrape the details of top 100 songs on billiboard.com. Url = https:/www.billboard.com/
You have to find the following details:
A) Song name
B) Artist name
C) Last week rank
D) Peak rank
E) Weeks on board
Note: - From the home page you have to click on the charts option then hot 100-page link through code.
"""


class BilliBoardData:

    def __init__(self):
        # Parsing through the webpage
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
        self.driver = None

    # def open_browser(self):
    #     try:
    #         # Set chrome options
    #         opt = Options()
    #         opt.add_argument("--disable-infobars")
    #         opt.add_argument("--disable-extensions")
    #         opt.add_argument('--log-level=OFF')
    #         opt.add_argument("--start-maximized")
    #         opt.add_experimental_option('excludeSwitches', ['enable-logging'])
    # 
    #         url = "https://www.billboard.com/"
    # 
    #         # Download and install required driver
    #         self.driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=opt)
    # 
    #         # Website URL
    #         self.driver.get(url)
    # 
    #         # Wait till the page has been loaded
    #         time.sleep(60)
    # 
    #         # Maximizing the browser window
    #         self.driver.maximize_window()
    # 
    #         # Getting current URL source code
    #         expected_title = "Billboard – Music Charts, News, Photos & Video".strip()
    #         print("Actual Title: " + self.driver.title)
    # 
    #         # Assert title of the page & Handled assertion error
    #         try:
    #             assert expected_title in self.driver.title.strip()
    #         except AssertionError:
    #             print("This is main title assertion error " + inspect.stack()[0][3])
    # 
    #         # set implicit wait time
    #         self.driver.implicitly_wait(60)
    #     except (NoSuchWindowException, WebDriverException) as err:
    #         print(err.msg + "Error while calling " + inspect.stack()[0][3])

    # def go_top_100_Songs_page(self):
    #     try:
    #         actions = ActionChains(self.driver)
    #         self.driver.switch_to.frame(1)
    #         self.driver.find_element_by_link_text('Charts').click()
    #         time.sleep(3)
    #     except NoSuchElementException as exception:
    #         print("Element not found for..." + inspect.stack()[0][3] + exception.msg)

    def extract_top_100_songs_data(self):
        song_name = []
        artist_name = []
        last_week_rank = []
        peak_rank = []
        weeks_on_board = []

        try:
            results = requests.get('https://www.billboard.com/charts/hot-100/', headers=self.headers, timeout=10)
            time.sleep(3)
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

        if results.status_code == 200:
            main_div = soup.find('div', {'class': 'pmc-paywall'})
            all_div = main_div.find_all('div', {'class': 'o-chart-results-list-row-container'})

            for i in range(len(all_div)):
                current_div = all_div[i]

                # Get song name
                try:
                    name = current_div.find('h3', {'id': 'title-of-a-story'}).text
                    song_name.append(name.strip().replace('\n', ""))
                except AttributeError:
                    print("Unable to get Get song name...")

                # Get artist name
                try:
                    artist = current_div.find('li', {'class': 'lrv-u-width-100p'}).find('span').text
                    artist_name.append(artist.strip().replace('\n', "").replace('\t', ""))
                except AttributeError:
                    print("Unable to get artist name...")

                # Get last week rank
                try:
                    last_week = current_div.find('li', {'class': 'lrv-u-width-100p'}).find_all('li')[3].text
                    last_week_rank.append(last_week.strip().replace('\n', ""))
                except AttributeError:
                    print("Unable to get last week rank..")

                # Get peak rank
                try:
                    peak = current_div.find('li', {'class': 'lrv-u-width-100p'}).find_all('li')[4].text
                    peak_rank.append(peak.strip().replace('\n', ""))
                except AttributeError:
                    print("Unable to get peak rank...")

                # Get last weeks on board
                try:
                    weeks_board = current_div.find('li', {'class': 'lrv-u-width-100p'}).find_all('li')[5].text
                    weeks_on_board.append(weeks_board.strip().replace('\n', ""))
                except AttributeError:
                    print("Unable to get weeks on board..")

        github_trending_repo_info = pd.DataFrame({'Song Name': song_name,
                                                  'Artist Name': artist_name,
                                                  'Last Week Rank': last_week_rank,
                                                  'Peak Rank': peak_rank,
                                                  'Weeks On Board': weeks_on_board})
        display(github_trending_repo_info)


if __name__ == "__main__":
    bb_data = BilliBoardData()
    # bb_data.open_browser()
    # bb_data.go_top_100_Songs_page()
    bb_data.extract_top_100_songs_data()


"""
Sample Output:
 Song Name                                        Artist Name Last Week Rank Peak Rank Weeks On Board
0                          Heat Waves                                      Glass Animals              1         1             61
1                                Stay                      The Kid LAROI & Justin Bieber              5         1             36
2                       Super Gremlin                                        Kodak Black              3         3             19
3                             abcdefu                                              GAYLE              4         3             17
4           We Don't Talk About Bruno  Carolina Gaitan, Mauro Castillo, Adassa, Rhenz...              2         1             12
5                               Ghost                                      Justin Bieber              7         6             25
6                          Easy On Me                                              Adele              6         1             23
7                               Enemy                              Imagine Dragons X JID             12         8             17
8                   Thats What I Want                                          Lil Nas X             10         9             26
9                          Bad Habits                                         Ed Sheeran              8         2             38
10                            Shivers                                         Ed Sheeran              9         4             27
11                              Woman                                           Doja Cat             15        12             33
12            Cold Heart (PNAU Remix)                              Elton John & Dua Lipa             11         7             28
13                         Big Energy                                              Latto             14        14             21
14                       Sweetest Pie                     Megan Thee Stallion & Dua Lipa              -        15              1
15                       Need To Know                                           Doja Cat             13         8             40
16                    Save Your Tears                         The Weeknd & Ariana Grande             17         1             63
17                            Ahhh Ha                                           Lil Durk             34        18              4
18                         Levitating                                           Dua Lipa             16         2             71
19                           Pushin P                Gunna & Future Featuring Young Thug             18         7             10
20                      Industry Baby                            Lil Nas X & Jack Harlow             19         1             34
21                     'Til You Can't                                       Cody Johnson             25        22             23
22                      One Right Now                           Post Malone & The Weeknd             21         6             19
23            What Happened To Virgil                           Lil Durk Featuring Gunna              -        24              1
24                           I Hate U                                                SZA             22         7             15
25                          Petty Too                          Lil Durk Featuring Future              -        26              1
26                        Hrs And Hrs                                          Muni Long             24        16             12
27                             MAMIII                                  Becky G X Karol G             26        15              5
28                   Surface Pressure                                     Jessica Darrow             20         8             12
29                      No Interviews                                           Lil Durk              -        30              1
30                          You Right                              Doja Cat & The Weeknd             29        11             37
31                           Good 4 U                                     Olivia Rodrigo             31         1             44
32                       Light Switch                                       Charlie Puth             27        27              8
33                       Golden Child                                           Lil Durk              -        34              1
34                           Buy Dirt                  Jordan Davis Featuring Luke Bryan             28        22             32
35                         Fancy Like                                       Walker Hayes             30         3             39
36              Thinking With My Dick                      Kevin Gates Featuring Juicy J              -        37              1
37                    Fingers Crossed                               Lauren Spencer-Smith             35        19             11
38                            Bam Bam                Camila Cabello Featuring Ed Sheeran             23        23              2
39                          Handsomer                               Russ Featuring Ktlyn             60        40              2
40           Love Nwantiti (Ah Ah Ah)                                               CKay             32        26             26
41                        Beers On Me                    Dierks Bentley, Breland & HARDY             40        40             12
42                     Broadway Girls                   Lil Durk Featuring Morgan Wallen             62        14             13
43                   Sand In My Boots                                      Morgan Wallen             33        30             35
44                         Doin' This                                         Luke Combs             37        37             14
45               Something In The Way                                            Nirvana              -        46              1
46                         Knife Talk            Drake Featuring 21 Savage & Project Pat             38         4             28
47                          Barbarian                                           Lil Durk              -        48              1
48                          Boyfriend                                       Dove Cameron             42        42              5
49                 To Be Loved By You                                    Parker McCollum             41        41             16
50                    Never Say Never                      Cole Swindell / Lainey Wilson             45        45              9
51                                 AA                                       Walker Hayes             43        43             10
52                 Shootout @ My Crib                                           Lil Durk              -        53              1
53                    Numb Little Bug                                         Em Beihold             48        48              7
54                       Started From                                           Lil Durk              -        55              1
55  Drunk (And I Don't Wanna Go Home)                        Elle King & Miranda Lambert             47        47             26
56                The Family Madrigal     Stephanie Beatriz, Olga Merediz & Encanto Cast             36        20             11
57                           Headtaps                                           Lil Durk              -        58              1
58               She's All I Wanna Be                                         Tate McRae             49        49              6
59                 Smoking & Thinking                                           Lil Durk              -        60              1
60                                 23                                           Sam Hunt             59        53             12
61                   Slow Down Summer                                       Thomas Rhett             52        52              4
62                               Peru                           Fireboy DML & Ed Sheeran             57        57              7
63                          The Motto                                   Tiesto & Ava Max             71        64              7
64         Grow Up/Keep It On Speaker                                           Lil Durk              -        65              1
65              Do We Have A Problem?                             Nicki Minaj X Lil Baby             54         2              6
66                What Else Can I Do?                 Diane Guerrero & Stephanie Beatriz             51        27             11
67                          Nail Tech                                        Jack Harlow             55        18              4
68                          Blocklist                                           Lil Durk              -        69              1
69                          Me Or Sum                      Nardo Wick, Lil Baby & Future             66        58             10
70                      Heart On Fire                                        Eric Church             68        56             17
71                      Dos Oruguitas                                    Sebastian Yatra             58        36             11
72                      Difference Is                   Lil Durk Featuring Summer Walker              -        73              1
73           Circles Around This Town                                       Maren Morris             65        63             10
74                       Freaky Deaky                                    Tyga X Doja Cat             67        43              3
75                  If I Was A Cowboy                                    Miranda Lambert             74        74              7
76                     Beautiful Lies                                Yung Bleu & Kehlani             69        65              8
77                       Flower Shops                     ERNEST Featuring Morgan Wallen             88        68              8
78                          Sacrifice                                         The Weeknd             56        11             10
79              Smokin Out The Window           Silk Sonic (Bruno Mars & Anderson .Paak)             64         5             19
80                       To The Moon!                            JNR CHOI & Sam Tompkins             87        81              3
81                            P Power                              Gunna Featuring Drake             75        24              9
82                               High                                   The Chainsmokers             76        57              7
83                           Pressure                                         Ari Lennox             70        66             12
84                 Federal Nightmares                                           Lil Durk              -        85              1
85                             Rumors                      Gucci Mane Featuring Lil Durk             79        51              7
86       Never Wanted To Be That Girl                      Carly Pearce & Ashley McBryde             78        78             10
87                Half Of My Hometown           Kelsea Ballerini Featuring Kenny Chesney             63        53             18
88                      I Love You So                                        The Walters             85        71              9
89                      Banking On Me                                              Gunna             80        61              4
90              Give Heaven Some Hell                                              HARDY             91        91              3
91                          I'm Tired                                 Labrinth & Zendaya             53        53              3
92                              Bones                                    Imagine Dragons              -        93              1
93      Rocking A Cardigan In Atlanta                                  Lil Shordie Scott             77        77              3
94                      Pissed Me Off                                           Lil Durk              -        39              4
95                       By Your Side                                           Rod Wave             86        58             16
96               Waiting On A Miracle                                  Stephanie Beatriz             83        48             11
97                    I Hate YoungBoy                         YoungBoy Never Broke Again             81        79              3
98                       City Of Gods            Fivio Foreign, Kanye West & Alicia Keys             90        46              5
99                             Closer                          Saweetie Featuring H.E.R.             99        89              5
"""