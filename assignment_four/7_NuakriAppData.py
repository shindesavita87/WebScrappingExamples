import inspect
import time
import requests
from IPython.core.display_functions import display
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchWindowException, WebDriverException, NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

"""
Scrape the details of Data science recruiters from naukri.com. Url = https://www.naukri.com/
You have to find the following details:
A) Name
B) Designation
C) Company
D) Skills they hire for
E) Location
Note: - From naukri.com homepage click on the recruiters option and the on the search pane type Data science and click on search. All this should be done through code
"""


class NaukriDataScience:
    def __init__(self):
        self.driver = None
        self.input = 'Data science'

    def open_browser(self):
        try:
            # Set chrome options
            opt = Options()
            opt.add_argument("--disable-infobars")
            opt.add_argument("--disable-extensions")
            opt.add_argument('--log-level=OFF')
            opt.add_experimental_option('excludeSwitches', ['enable-logging'])

            url = "https://www.naukri.com/"

            # Download and install required driver
            self.driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=opt)

            # Maximizing the browser window
            self.driver.maximize_window()

            # Website URL
            self.driver.get(url)

            # Wait till the page has been loaded
            time.sleep(5)
        except (NoSuchWindowException, WebDriverException) as err:
            print(err.msg + "Error while calling " + inspect.stack()[0][3])
        except:
            print("Error while calling " + inspect.stack()[0][3])

    def go_to_data_science_data_page(self):

        # Getting current URL source code
        expected_title = "Jobs - Recruitment - Job Search - Employment - Job Vacancies - Naukri.com"
        print("Actual Title: " + self.driver.title)

        # Assert title of the page & Handled assertion error
        try:
            assert expected_title in self.driver.title
        except AssertionError:
            print("This is assertion error " + inspect.stack()[0][3])

        try:
            self.driver.find_element(By.CLASS_NAME, 'suggestor-input').send_keys(self.input, Keys.ENTER)
            # Wait till the page has been loaded
            time.sleep(5)
        except NoSuchElementException as exception:
            print("Element not found for..." + inspect.stack()[0][3])

    def extract_data_science_information(self):
        job_name = []
        job_designation = []
        company_name = []
        skills_they_hire_for = []
        location = []

        # Parsing through the webpage
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}

        try:
            results = requests.get(self.driver.current_url, headers=headers, timeout=3)
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

        # Get product brand from product details page
        if results.status_code == 200:
            main_div = soup.find('div', {'class': 'list'})
            all_div = main_div.find_all('article', {'class': 'jobTuple bgWhite br4 mb-8'})

            for i in range(len(all_div)):
                item = all_div[i]

                # Get job name
                try:
                    name = item.find('a', {'class': 'title fw500 ellipsis'}).text
                    job_name.append(name)
                except AttributeError:
                    print("Unable to get job name..")

                # Get job designation
                try:
                    designation = item.find('a', {'class': 'title fw500 ellipsis'}).text
                    job_designation.append(designation)
                except AttributeError:
                    print("Unable to job designation..")

                # Get company name
                try:
                    company = item.find('div', {'class': 'mt-7 companyInfo subheading lh16'}).find('a').text
                    company_name.append(company)
                except AttributeError:
                    print("Unable to company name..")

                # Get skills they hire for
                try:
                    temp_list = []
                    skills = item.find('ul', {'class': 'tags has-description'}).find_all('li')
                    for j in range(len(skills)):
                        temp_list.append(skills[j])
                    skills_they_hire_for.append(temp_list)
                except AttributeError:
                    print("Unable to get skills they hire for..")

                # Get location
                try:
                    loc = item.find('i', {'class': 'fleft icon-16 lh16 mr-4 naukicon naukicon-location'}).find_next_sibling('span').text
                    location.append(loc)
                except AttributeError:
                    print("Unable to get location..")

            nuakri_ds_jobs = pd.DataFrame({'Job Title': job_name,
                                           'Job Designation': job_designation,
                                           'Company Name': company_name,
                                           'Skills They Hire For': skills_they_hire_for,
                                           'Location': location})

            display(nuakri_ds_jobs)

            print(job_name, job_designation, company_name, skills_they_hire_for, location)
            self.driver.close()


if __name__ == "__main__":
    naukri_data = NaukriDataScience()
    naukri_data.open_browser()
    naukri_data.go_to_data_science_data_page()
    naukri_data.extract_data_science_information()

"""
Sample Output:

Job Title	Job Designation	Company Name	Skills They Hire For	Location
0	Capgemini hiring Business Analyst with Cards ...	Capgemini hiring Business Analyst with Cards ...	Capgemini	[[IT Skills], [Testing], [credit car], [Cards]...	Pune, Bangalore/Bengaluru, Mumbai (All Areas)
1	Urgent Requirement of Cyber Security Business ...	Urgent Requirement of Cyber Security Business ...	Wipro	[[Agile], [business analysis], [vulnerability ...	Hyderabad/Secunderabad, Pune, Chennai, Bangalo...
2	DXC is hiring For Data Architect	DXC is hiring For Data Architect	DXC Technology	[[ETL], [Qlicksense], [written], [Power BI], [...	Hyderabad/Secunderabad, Pune, Chennai, Bangalo...
3	Big Data Developer	Big Data Developer	Capgemini	[[SCALA], [Big Data], [Spark], [IT Skills], [S...	Pune, Bangalore/Bengaluru, India
4	Hadoop Developer	Hadoop Developer	Mindtree	[[IT Skills], [Java], [Python], [Cloud], [Elas...	Noida, Kolkata, Hyderabad/Secunderabad, Pune, ...
5	Google Cloud Platform (GCP)	Google Cloud Platform (GCP)	eClerx	[[Google Cloud Platform], [Python], [Big data]...	Navi Mumbai, Pune
6	Deep Learning Engineer - NLP/Computer Vision	Deep Learning Engineer - NLP/Computer Vision	DataToBiz	[[Python programming], [DL Model optimization]...	Kolkata, Mumbai, Hyderabad/Secunderabad, Pune,...
7	Computer Vision Python Data Scientist	Computer Vision Python Data Scientist	OceanOfWeb	[[DL], [ML], [Natural Language], [communicatio...	Mumbai, Hyderabad/Secunderabad, Pune, Chennai,...
8	Business Analyst - RPA	Business Analyst - RPA	WNS Global Services	[[BPO], [voice], [Gap Analysis], [Rpa], [Use C...	Pune, Gurgaon/Gurugram, Bangalore/Bengaluru
9	Rpa Developer	Rpa Developer	WNS Global Services	[[rpa], [.net], [blue prism], [technical desig...	Pune, Bangalore/Bengaluru
10	Executive Assistant	Executive Assistant	Bajaj Finserv	[[Root cause analysis], [Executive], [Networki...	Pune
11	Urgent Openings For Google Analytics -Tag Deve...	Urgent Openings For Google Analytics -Tag Deve...	LOGICSERVE DIGITAL PRIVATE LIMITED	[[Gtm], [Google Tag Management], [Javascript],...	Navi Mumbai, Pune, Gurgaon/Gurugram, Bangalore...
12	eClerx is hiring For Business Analytics/Data A...	eClerx is hiring For Business Analytics/Data A...	eClerx	[[Project Handling], [digital analytics], [Pow...	Pune, Mumbai (All Areas)
13	Digital - Data Engineer	Digital - Data Engineer	eClerx	[[Alteryx], [data engineering], [Python], [IT ...	Pune, Mumbai (All Areas)
14	Digital Analytics- Implementation	Digital Analytics- Implementation	eClerx	[[IT Skills], [HTML], [CSS], [Javascript], [Ta...	Chandigarh, Navi Mumbai, Pune
15	Data Engineer	Data Engineer	Collabera India	[[GIT], [Airflow], [Redshift], [Python], [data...	New Delhi, Pune, Gurgaon/Gurugram, Bangalore/B...
16	Business Requirement Analysis Business Analyst	Business Requirement Analysis Business Analyst	Accenture	[[verbal communication], [written], [SAP IBP],...	Pune
17	Lead - Payments - Acquiring Business/Senior Lead	Lead - Payments - Acquiring Business/Senior Lead	Bajaj Finserv	[[Training], [MS Office Powerpoint], [B2B], [P...	Pune
18	Analytics Engineer-Emerson	Analytics Engineer-Emerson	Emerson Automation Solutions	[[Analysis], [Data Analysis], [Data Analytics]...	Pune
19	CI Regional Expert	CI Regional Expert	AkzoNobel	[[SAP], [Conflict resolution], [Social network...	Pune
['Capgemini hiring Business Analyst  with Cards Domain', 'Urgent Requirement of Cyber Security Business Analyst in Wipro', 'DXC is hiring For Data Architect', 'Big Data Developer', 'Hadoop Developer', 'Google Cloud Platform (GCP)', 'Deep Learning Engineer - NLP/Computer Vision', 'Computer Vision Python Data Scientist', 'Business Analyst - RPA', 'Rpa Developer', 'Executive Assistant', 'Urgent Openings For Google Analytics -Tag Development', 'eClerx is hiring For Business Analytics/Data Analytics', 'Digital - Data Engineer', 'Digital Analytics- Implementation', 'Data Engineer', 'Business Requirement Analysis Business Analyst', 'Lead - Payments - Acquiring Business/Senior Lead', 'Analytics Engineer-Emerson', 'CI Regional Expert'] ['Capgemini hiring Business Analyst  with Cards Domain', 'Urgent Requirement of Cyber Security Business Analyst in Wipro', 'DXC is hiring For Data Architect', 'Big Data Developer', 'Hadoop Developer', 'Google Cloud Platform (GCP)', 'Deep Learning Engineer - NLP/Computer Vision', 'Computer Vision Python Data Scientist', 'Business Analyst - RPA', 'Rpa Developer', 'Executive Assistant', 'Urgent Openings For Google Analytics -Tag Development', 'eClerx is hiring For Business Analytics/Data Analytics', 'Digital - Data Engineer', 'Digital Analytics- Implementation', 'Data Engineer', 'Business Requirement Analysis Business Analyst', 'Lead - Payments - Acquiring Business/Senior Lead', 'Analytics Engineer-Emerson', 'CI Regional Expert'] ['Capgemini', 'Wipro', 'DXC Technology', 'Capgemini', 'Mindtree', 'eClerx', 'DataToBiz', 'OceanOfWeb', 'WNS Global Services', 'WNS Global Services', 'Bajaj Finserv', 'LOGICSERVE DIGITAL PRIVATE LIMITED', 'eClerx', 'eClerx', 'eClerx', 'Collabera India', 'Accenture', 'Bajaj Finserv', 'Emerson Automation Solutions', 'AkzoNobel'] [[<li class="fleft fs12 grey-text lh16 dot">IT Skills</li>, <li class="fleft fs12 grey-text lh16 dot">Testing</li>, <li class="fleft fs12 grey-text lh16 dot">credit car</li>, <li class="fleft fs12 grey-text lh16 dot">Cards</li>, <li class="fleft fs12 grey-text lh16 dot">Business Analysis</li>], [<li class="fleft fs12 grey-text lh16 dot">Agile</li>, <li class="fleft fs12 grey-text lh16 dot">business analysis</li>, <li class="fleft fs12 grey-text lh16 dot">vulnerability management</li>, <li class="fleft fs12 grey-text lh16 dot">communication</li>, <li class="fleft fs12 grey-text lh16 dot">SDLC</li>, <li class="fleft fs12 grey-text lh16 dot">Jira</li>, <li class="fleft fs12 grey-text lh16 dot">written</li>, <li class="fleft fs12 grey-text lh16 dot">verbal</li>], [<li class="fleft fs12 grey-text lh16 dot">ETL</li>, <li class="fleft fs12 grey-text lh16 dot">Qlicksense</li>, <li class="fleft fs12 grey-text lh16 dot">written</li>, <li class="fleft fs12 grey-text lh16 dot">Power BI</li>, <li class="fleft fs12 grey-text lh16 dot">Tableau</li>, <li class="fleft fs12 grey-text lh16 dot">SAP BO</li>, <li class="fleft fs12 grey-text lh16 dot">modeling</li>, <li class="fleft fs12 grey-text lh16 dot">Data warehousing</li>], [<li class="fleft fs12 grey-text lh16 dot">SCALA</li>, <li class="fleft fs12 grey-text lh16 dot">Big Data</li>, <li class="fleft fs12 grey-text lh16 dot">Spark</li>, <li class="fleft fs12 grey-text lh16 dot">IT Skills</li>, <li class="fleft fs12 grey-text lh16 dot">Software Development</li>, <li class="fleft fs12 grey-text lh16 dot">Testing</li>, <li class="fleft fs12 grey-text lh16 dot">Cloud</li>, <li class="fleft fs12 grey-text lh16 dot">Oracle</li>], [<li class="fleft fs12 grey-text lh16 dot">IT Skills</li>, <li class="fleft fs12 grey-text lh16 dot">Java</li>, <li class="fleft fs12 grey-text lh16 dot">Python</li>, <li class="fleft fs12 grey-text lh16 dot">Cloud</li>, <li class="fleft fs12 grey-text lh16 dot">Elastic Search</li>, <li class="fleft fs12 grey-text lh16 dot">Big Data</li>, <li class="fleft fs12 grey-text lh16 dot">Azure</li>, <li class="fleft fs12 grey-text lh16 dot">Hive</li>], [<li class="fleft fs12 grey-text lh16 dot">Google Cloud Platform</li>, <li class="fleft fs12 grey-text lh16 dot">Python</li>, <li class="fleft fs12 grey-text lh16 dot">Big data</li>, <li class="fleft fs12 grey-text lh16 dot">Spark</li>, <li class="fleft fs12 grey-text lh16 dot">GCP</li>, <li class="fleft fs12 grey-text lh16 dot">Big Query</li>, <li class="fleft fs12 grey-text lh16 dot">Airflow</li>], [<li class="fleft fs12 grey-text lh16 dot">Python programming</li>, <li class="fleft fs12 grey-text lh16 dot">DL Model optimization</li>, <li class="fleft fs12 grey-text lh16 dot">Deep Learning</li>, <li class="fleft fs12 grey-text lh16 dot">RCNN</li>, <li class="fleft fs12 grey-text lh16 dot">YOLO</li>, <li class="fleft fs12 grey-text lh16 dot">GPT</li>, <li class="fleft fs12 grey-text lh16 dot">DL Model</li>, <li class="fleft fs12 grey-text lh16 dot">Machine learning</li>], [<li class="fleft fs12 grey-text lh16 dot">DL</li>, <li class="fleft fs12 grey-text lh16 dot">ML</li>, <li class="fleft fs12 grey-text lh16 dot">Natural Language</li>, <li class="fleft fs12 grey-text lh16 dot">communication</li>, <li class="fleft fs12 grey-text lh16 dot">analytical</li>, <li class="fleft fs12 grey-text lh16 dot">Python</li>, <li class="fleft fs12 grey-text lh16 dot">IT Skills</li>, <li class="fleft fs12 grey-text lh16 dot">Data Science</li>], [<li class="fleft fs12 grey-text lh16 dot">BPO</li>, <li class="fleft fs12 grey-text lh16 dot">voice</li>, <li class="fleft fs12 grey-text lh16 dot">Gap Analysis</li>, <li class="fleft fs12 grey-text lh16 dot">Rpa</li>, <li class="fleft fs12 grey-text lh16 dot">Use Cases</li>, <li class="fleft fs12 grey-text lh16 dot">Requirement Gathering</li>, <li class="fleft fs12 grey-text lh16 dot">Business Analysis</li>], [<li class="fleft fs12 grey-text lh16 dot">rpa</li>, <li class="fleft fs12 grey-text lh16 dot">.net</li>, <li class="fleft fs12 grey-text lh16 dot">blue prism</li>, <li class="fleft fs12 grey-text lh16 dot">technical design</li>, <li class="fleft fs12 grey-text lh16 dot">java</li>, <li class="fleft fs12 grey-text lh16 dot">quality control</li>, <li class="fleft fs12 grey-text lh16 dot">scalability</li>, <li class="fleft fs12 grey-text lh16 dot">programming</li>], [<li class="fleft fs12 grey-text lh16 dot">Root cause analysis</li>, <li class="fleft fs12 grey-text lh16 dot">Executive</li>, <li class="fleft fs12 grey-text lh16 dot">Networking</li>, <li class="fleft fs12 grey-text lh16 dot">IRDA</li>, <li class="fleft fs12 grey-text lh16 dot">Analytical</li>, <li class="fleft fs12 grey-text lh16 dot">Research</li>, <li class="fleft fs12 grey-text lh16 dot">Financial services</li>, <li class="fleft fs12 grey-text lh16 dot">Principal</li>], [<li class="fleft fs12 grey-text lh16 dot">Gtm</li>, <li class="fleft fs12 grey-text lh16 dot">Google Tag Management</li>, <li class="fleft fs12 grey-text lh16 dot">Javascript</li>, <li class="fleft fs12 grey-text lh16 dot">google analytics</li>, <li class="fleft fs12 grey-text lh16 dot">Google Tag Manager</li>], [<li class="fleft fs12 grey-text lh16 dot">Project Handling</li>, <li class="fleft fs12 grey-text lh16 dot">digital analytics</li>, <li class="fleft fs12 grey-text lh16 dot">Power Bi</li>, <li class="fleft fs12 grey-text lh16 dot">consulting</li>, <li class="fleft fs12 grey-text lh16 dot">business analysis</li>, <li class="fleft fs12 grey-text lh16 dot">business analytics</li>, <li class="fleft fs12 grey-text lh16 dot">data insight</li>, <li class="fleft fs12 grey-text lh16 dot">false negative</li>], [<li class="fleft fs12 grey-text lh16 dot">Alteryx</li>, <li class="fleft fs12 grey-text lh16 dot">data engineering</li>, <li class="fleft fs12 grey-text lh16 dot">Python</li>, <li class="fleft fs12 grey-text lh16 dot">IT Skills</li>, <li class="fleft fs12 grey-text lh16 dot">Data Science</li>, <li class="fleft fs12 grey-text lh16 dot">Artificial Intelligence</li>, <li class="fleft fs12 grey-text lh16 dot">Tableau</li>, <li class="fleft fs12 grey-text lh16 dot">digital analytics</li>], [<li class="fleft fs12 grey-text lh16 dot">IT Skills</li>, <li class="fleft fs12 grey-text lh16 dot">HTML</li>, <li class="fleft fs12 grey-text lh16 dot">CSS</li>, <li class="fleft fs12 grey-text lh16 dot">Javascript</li>, <li class="fleft fs12 grey-text lh16 dot">Tableau</li>, <li class="fleft fs12 grey-text lh16 dot">Power BI</li>, <li class="fleft fs12 grey-text lh16 dot">digital analytics</li>, <li class="fleft fs12 grey-text lh16 dot">Adobe launch</li>], [<li class="fleft fs12 grey-text lh16 dot">GIT</li>, <li class="fleft fs12 grey-text lh16 dot">Airflow</li>, <li class="fleft fs12 grey-text lh16 dot">Redshift</li>, <li class="fleft fs12 grey-text lh16 dot">Python</li>, <li class="fleft fs12 grey-text lh16 dot">data modelling</li>, <li class="fleft fs12 grey-text lh16 dot">Databricks Spark</li>, <li class="fleft fs12 grey-text lh16 dot">SQL</li>, <li class="fleft fs12 grey-text lh16 dot">Jenkins</li>], [<li class="fleft fs12 grey-text lh16 dot">verbal communication</li>, <li class="fleft fs12 grey-text lh16 dot">written</li>, <li class="fleft fs12 grey-text lh16 dot">SAP IBP</li>, <li class="fleft fs12 grey-text lh16 dot">IBP</li>, <li class="fleft fs12 grey-text lh16 dot">IT Skills</li>, <li class="fleft fs12 grey-text lh16 dot">SAP</li>, <li class="fleft fs12 grey-text lh16 dot">Business process</li>, <li class="fleft fs12 grey-text lh16 dot">Demand planning</li>], [<li class="fleft fs12 grey-text lh16 dot">Training</li>, <li class="fleft fs12 grey-text lh16 dot">MS Office Powerpoint</li>, <li class="fleft fs12 grey-text lh16 dot">B2B</li>, <li class="fleft fs12 grey-text lh16 dot">Penetration</li>, <li class="fleft fs12 grey-text lh16 dot">Sales</li>, <li class="fleft fs12 grey-text lh16 dot">Project management</li>, <li class="fleft fs12 grey-text lh16 dot">Lead</li>, <li class="fleft fs12 grey-text lh16 dot">Issue resolution</li>], [<li class="fleft fs12 grey-text lh16 dot">Analysis</li>, <li class="fleft fs12 grey-text lh16 dot">Data Analysis</li>, <li class="fleft fs12 grey-text lh16 dot">Data Analytics</li>, <li class="fleft fs12 grey-text lh16 dot">Statistics</li>, <li class="fleft fs12 grey-text lh16 dot">Analytics</li>], [<li class="fleft fs12 grey-text lh16 dot">SAP</li>, <li class="fleft fs12 grey-text lh16 dot">Conflict resolution</li>, <li class="fleft fs12 grey-text lh16 dot">Social networking</li>, <li class="fleft fs12 grey-text lh16 dot">Service excellence</li>, <li class="fleft fs12 grey-text lh16 dot">Business process management</li>, <li class="fleft fs12 grey-text lh16 dot">Continuous improvement</li>, <li class="fleft fs12 grey-text lh16 dot">Operations</li>, <li class="fleft fs12 grey-text lh16 dot">Six sigma black belt</li>]] ['Pune, Bangalore/Bengaluru, Mumbai (All Areas)', 'Hyderabad/Secunderabad, Pune, Chennai, Bangalore/Bengaluru, Delhi / NCR', 'Hyderabad/Secunderabad, Pune, Chennai, Bangalore/Bengaluru, Delhi / NCR', 'Pune, Bangalore/Bengaluru, India', 'Noida, Kolkata, Hyderabad/Secunderabad, Pune, Chennai, Coimbatore, Bangalore/Bengaluru', 'Navi Mumbai, Pune', 'Kolkata, Mumbai, Hyderabad/Secunderabad, Pune, Ahmedabad, Chennai, Bangalore/Bengaluru, Delhi / NCR', 'Mumbai, Hyderabad/Secunderabad, Pune, Chennai, Bangalore/Bengaluru', 'Pune, Gurgaon/Gurugram, Bangalore/Bengaluru', 'Pune, Bangalore/Bengaluru', 'Pune', 'Navi Mumbai, Pune, Gurgaon/Gurugram, Bangalore/Bengaluru', 'Pune, Mumbai (All Areas)', 'Pune, Mumbai (All Areas)', 'Chandigarh, Navi Mumbai, Pune', 'New Delhi, Pune, Gurgaon/Gurugram, Bangalore/Bengaluru, Delhi / NCR', 'Pune', 'Pune', 'Pune', 'Pune']
"""
