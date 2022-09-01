import requests
from IPython.core.display_functions import display
from bs4 import BeautifulSoup
import pandas as pd
import openpyxl

pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 100)
pd.set_option('display.width', 100)

"""
1. ScrapethedetailsofmostviewedvideosonYouTubefromWikipedia.
Url = https://en.wikipedia.org/wiki/List_of_most-viewed_YouTube_videos
You need to find following details: A) Rank
B) Name
C) Artist
D) Upload date E) Views
"""


def extract_wikipedia_information():
    rank_no = []
    video_names = []
    uploader_details = []
    views_in_billions = []
    upload_dates = []

    """  Handled request error.It will raise error in case of failure. """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
    req_url = 'https://en.wikipedia.org/wiki/List_of_most-viewed_YouTube_videos'
    try:
        results = requests.get(req_url, headers=headers, timeout=3)
        # Raise error in case of failure
        results.raise_for_status()
        soup = BeautifulSoup(results.text, 'html.parser')
        print(soup)
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
        table_div = soup.find('div', {'id': 'mw-content-text'})
        all_tr = table_div.find_all('table', {'class': 'wikitable sortable'})[0].find_all('tr')
        h1 = all_tr[0].find_all('th')[0].text
        h2 = all_tr[0].find_all('th')[1].text
        h3 = all_tr[0].find_all('th')[2].text
        h4 = all_tr[0].find_all('th')[3].text
        h5 = all_tr[0].find_all('th')[4].text

        """  Handled attribute error. """
        for i in range(1, len(all_tr) - 1):
            item = all_tr[i]

            try:
                rank = item.find_all('td')[0].text
                rank_no.append(rank)
            except AttributeError:
                print("Error while reading column value...")

            try:
                name = item.find_all('td')[1].text
                # Slice string to remove last 3 characters from string
                name = name[:len(name) - 4]
                video_names.append(name)
            except AttributeError:
                print("Error while reading column value...")

            try:
                uploader = item.find_all('td')[2].text
                uploader_details.append(uploader)
            except AttributeError:
                print("Error while reading column value...")

            try:
                views = item.find_all('td')[3].text
                views_in_billions.append(views)
            except AttributeError:
                print("Error while reading column value...")

            try:
                date = item.find_all('td')[4].text
                upload_dates.append(date)
            except AttributeError:
                print("Error while reading column value...")

        exception_info = pd.DataFrame({h1: rank_no,
                                       h2: video_names,
                                       h3: uploader_details,
                                       h4: views_in_billions,
                                       h5: upload_dates})

        display(exception_info)

        """  Handled file error. """
        try:
            # Save data in CSV file
            exception_info.to_csv('~/Desktop/wekipedioa_youtube_ranking.csv', sep='\t')

            # Save data in excel file
            exception_info.to_excel("~/Desktop/wekipedioa_youtube_ranking.xlsx")
        except IOError:
            print("Error: While writing in file.")


extract_wikipedia_information()

"""
Sample Output:
	No.\n	Video name\n	Uploader\n	Views (billions)\n	Upload date\n
0	1.	"Baby Shark Dance	Pinkfong Baby Shark - Kids' Songs & Stories	10.35	June 17, 2016
1	2.	"Despacito	Luis Fonsi	7.79	January 12, 2017
2	3.	"Johny Johny Yes Papa"	LooLoo Kids	6.24	October 8, 2016
3	4.	"Shape of You"	Ed Sheeran	5.65	January 30, 2017
4	5.	"See You Again"	Wiz Khalifa	5.45	April 6, 2015
5	6.	"Bath Song"	Cocomelon – Nursery Rhymes	5.12	May 2, 2018
6	7.	"Learning Colors – Colorful Eggs on a Farm"	Miroshka TV	4.56	February 27, 2018
7	8.	"Phonics Song with Two Words"	ChuChu TV	4.52	March 6, 2014
8	9.	"Uptown Funk"	Mark Ronson	4.50	November 19, 2014
9	10.	"Masha and the Bear – Recipe for Disaster"	Get Movies	4.49	January 31, 2012
10	11.	"Gangnam Style"	Psy	4.37	July 15, 2012
11	12.	"Dame Tu Cosita"	El Chombo	3.89	April 5, 2018
12	13.	"Wheels on the Bus"	Cocomelon – Nursery Rhymes	3.82	May 24, 2018
13	14.	"Sugar"	Maroon 5	3.66	January 14, 2015
14	15.	"Roar"	Katy Perry	3.54	September 5, 2013
15	16.	"Counting Stars"	OneRepublic	3.53	May 31, 2013
16	17.	"Sorry"	Justin Bieber	3.52	October 22, 2015
17	18.	"Thinking Out Loud"	Ed Sheeran	3.42	October 7, 2014
18	19.	"Axel F"	Crazy Frog	3.28	June 16, 2009
19	20.	"Girls Like You"	Maroon 5	3.25	May 31, 2018
20	21.	"Faded"	Alan Walker	3.25	December 3, 2015
21	22.	"Dark Horse"	Katy Perry	3.24	February 20, 2014
22	23.	"Let Her Go"	Passenger	3.19	July 25, 2012
23	24.	"Bailando"	Enrique Iglesias	3.18	April 11, 2014
24	25.	"Lean On"	Major Lazer	3.18	March 22, 2015
25	26.	"Baa Baa Black Sheep"	Cocomelon – Nursery Rhymes	3.17	June 25, 2018
26	27.	"Shake It Off"	Taylor Swift	3.15	August 18, 2014
27	28.	"Perfect"	Ed Sheeran	3.12	November 9, 2017
28	29.	"Waka Waka (This Time for Africa)"	Shakira	3.09	June 4, 2010
29	30.	"Mi Gente"	J Balvin	3.05	June 29, 2017

"""
