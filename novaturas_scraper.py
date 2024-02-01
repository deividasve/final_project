import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
url = 'https://www.novaturas.lt/paskutine-minute'
gecko_service = Service(GeckoDriverManager().install())
gecko_service.start()
driver = webdriver.Firefox(service=gecko_service)
driver.get(url)
time.sleep(2)

# Accepting cookie's policy and loading more page elements
cookies = WebDriverWait(driver, 20).until(
    ec.element_to_be_clickable((By.CSS_SELECTOR, 'button.GDPR-Button:nth-child(1)')))
cookies.click()
load_more = WebDriverWait(driver, 20).until(ec.element_to_be_clickable((By.CSS_SELECTOR, 'button.c-PJLV:nth-child(2)')))
load_more.click()
time.sleep(2)
scrolls_count = 0
while scrolls_count < 30:
    time.sleep(3)
    scroll_until_element = driver.find_element(By.XPATH,
                                               '/html/body/div[1]/div/div[2]/div/div[4]/div[1]/div/div/div/div/div/a/div/div[2]/span[1]')
    driver.execute_script('arguments[0].scrollIntoView(true);', scroll_until_element)
    scrolls_count += 1
    time.sleep(3)
trip_details_list = []
web_link = [link.get_attribute('href') for link in driver.find_elements(By.CSS_SELECTOR, '.c-foxNNj a')]
save_interval = 1
rows_count = 0

# Starting a loop to access each of a website from web_link list and retrieve required data
for link in web_link:
    full_link = f'{link}'
    driver.get(full_link)
    time.sleep(2)

    # Collecting easily accessible data: description, destination, hotel rating and travel type (transport)
    try:
        description_element = WebDriverWait(driver, 20).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, 'h1.c-PJLV')))
        description = description_element.text
    except NoSuchElementException:
        description = None
    try:
        destination_element = WebDriverWait(driver, 20).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, '.c-bTjFtG')))
        destination = destination_element.text
    except NoSuchElementException:
        destination = None
    try:
        offer_transport_element = WebDriverWait(driver, 20).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, 'li.c-eeCjTt:nth-child(1)')))
        offer_transport = offer_transport_element.text
    except NoSuchElementException:
        offer_transport = None

    # Counting how many 'stars' does the hotel have
    html_code = driver.page_source
    soup = BeautifulSoup(html_code, 'html.parser')
    trimmed_soup = soup.find('div', class_='c-hnbPrw')
    if trimmed_soup:
        hotel_stars_element = trimmed_soup.find_all('svg', class_='c-dPemeR c-lgAqJq c-lgAqJq-eCncRB-isFull-true')
        hotel_stars = len(hotel_stars_element)
    else:
        hotel_stars = None

    # Webpage has multiple deals thus it is required to use additional loop to gather required data of each deal
    try:
        offer_elements_block = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, '.c-craXUg'))
        )
    except TimeoutException:
        print('CSS_SELECTOR or Website not found')
        continue
    offer_elements = offer_elements_block.find_elements(By.CLASS_NAME, 'c-kQzNuN')
    for offer_element in offer_elements:
        try:
            room_element = offer_element.find_element(By.CLASS_NAME, 'c-juEpcc')
            room = room_element.text if room_element else None
        except NoSuchElementException:
            room = None
        try:
            nights_element = offer_element.find_element(By.CLASS_NAME, 'c-eaRLdk')
            nights = nights_element.text[0] if nights_element else None
        except NoSuchElementException:
            nights = None
        try:
            date_element = offer_element.find_element(By.CLASS_NAME, 'c-eaRLdk')
            date = date_element.text.split('\n')[1] if date_element else None
        except NoSuchElementException:
            date = None
        try:
            price_element = offer_element.find_element(By.CLASS_NAME, 'c-bkJVKH')
            price = price_element.text if price_element else None
        except NoSuchElementException:
            price = None
            print(f'Price element not found in: {full_link}')

        # Standardizing 'feeding' element values
        feeding = None
        try:
            feeding_element = offer_element.find_element(By.CLASS_NAME, 'c-fqaKYk').text.strip()
            if 'Pusryčiai ir vakarienė' in feeding_element or '4 pusryčiai, 2 vakarienės' in feeding_element:
                feeding = 'Pusryčiai ir vakarienė'
            elif 'Pusryčiai, pietūs, vakarienė' in feeding_element:
                feeding = 'Pusryčiai, pietūs, vakarienė'
            elif 'Pusryčiai' in feeding_element or 'pusryčiai' in feeding_element:
                feeding = 'Pusryčiai'
            elif ('Viskas įskaičiuota' in feeding_element or 'viskas įskaičiuota' in feeding_element
                  or 'Premium All Inclusive ' in feeding_element):
                feeding = 'Viskas įskaičiuota'
        except NoSuchElementException:
            feeding = None

        # Describing dictionary elements
        trip_details = {
            'Description': description,
            'Destination': destination,
            'Date': date,
            'Travel Transport': offer_transport,
            'Hotel Stars': hotel_stars,
            'Room': room,
            'Feeding': feeding,
            'Nights': nights,
            'Price': price,
        }
        trip_details_list.append(trip_details)

        # Updating a .csv file when scraping each deal
        rows_count += 1
        if rows_count % save_interval == 0:
            df = pd.DataFrame(trip_details_list)
            df.to_csv('csv/novaturas.csv', index=False)
            print('Additional data has been added to .csv')
    time.sleep(2)

# Once again updating DataFrame and a .csv file after script is finished
df = pd.DataFrame(trip_details_list)
df.to_csv('csv/novaturas.csv', index=False)
print(df)
driver.quit()
