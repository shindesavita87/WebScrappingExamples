import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

# Declare array of all search keywords
search_images = ["fruits", "cars", "Machine Learning", "Guitar", "Cakes"]

# Creating intance of chrome driver by passing its executable path
driver = webdriver.Chrome(executable_path="/Users/savitasurajhitansh/DevTools/chromedriver")

# Maximizing the browser window
driver.maximize_window()

# Entering the URL
driver.get("https://www.google.co.in/imghp?hl=en&ogbl")

# Applying implicit wait will be applicable throughout
driver.implicitly_wait(60)

for search_keyword in search_images:
    # Entering search text into search text box
    search_txt = driver.find_element_by_name('q')
    search_txt.send_keys(search_keyword, Keys.RETURN)

    # Getting current URL source code
    actual_title = driver.title
    expected_title = search_keyword + " - Google Search"
    print("expected_title: " + expected_title)

    # Assert title of the page
    assert expected_title in driver.title

    page = requests.get("driver.current_url")

    soup = BeautifulSoup(page, 'html.parser')
    all_img = soup.find_all('img')
    i = 1
    for i in range(11):
        link = all_img[i].get('src')
        print(link)
        if (i > 2 & 1 <= 10):
            driver.get(link)
            img = driver.find_element_by_xpath('//img')
            actionChains = ActionChains(driver)
            actionChains.move_to_element(img).context_click().send_keys(Keys.ARROW_DOWN).send_keys(
                Keys.ARROW_DOWN).send_keys(Keys.RETURN).send_keys(Keys.RETURN).perform()

    driver.get("https://www.google.co.in/imghp?hl=en&ogbl")

# Close all instance of browser which is opened by webdriver
driver.quit()
