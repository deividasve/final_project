import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

# for i in range(1, 18):
#     url = f'https://www.westexpress.lt/paskutine-minute?page={i}/'

url = 'https://www.westexpress.lt/paskutine-minute?page=1'
gecko_service = Service(GeckoDriverManager().install())
gecko_service.start()
driver = webdriver.Firefox(service=gecko_service)
driver.get(url)
time.sleep(2)
# add_close = WebDriverWait(driver, 100).until(ec.element_to_be_clickable((By.CSS_SELECTOR, '.close')))
# add_close = WebDriverWait(driver, 10).until(ec.element_to_be_clickable((By.XPATH, '/div/div/div/button')))
add_close = WebDriverWait(driver, 10).until(ec.element_to_be_clickable((By.CLASS_NAME, 'close')))

add_close.click()
trip_details_list = []
web_link = [link.get_attribute('href') for link in driver.find_elements(By.CSS_SELECTOR, 'a.travel-block')]
save_interval = 1
rows_count = 0
for link in web_link:
    full_link = f'{link}'
    driver.get(full_link)
    time.sleep(5)
    response = requests.get(link)

    print(full_link)

    soup = BeautifulSoup(response.content, 'html.parser')
    destination_element = soup.find('li', class_='destination')
    destination = destination_element.text.strip() if destination_element else None
    description_element = soup.find('div', class_='nopad section-title-lg')
    description = description_element.text.strip() if description_element else None
    hotel_stars_element = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.CSS_SELECTOR, '.h2')))
    hotel_stars = hotel_stars_element.text[0] if hotel_stars_element else None

    html_code = driver.page_source
    soup = BeautifulSoup(html_code, 'html.parser')
    trimmed_soup = soup.find('div', class_='package_filter_content')



    offer_elements = trimmed_soup.find_elements(By.CLASS_NAME, 'trip-choice-table-row')
    for offer_element in offer_elements:
        try:
            date_element = offer_element.find_element(By.CLASS_NAME, 'trip-choice-days-large')
            date = date_element.text.split(' → ')[0].replace(' ', '-') if date_element else None
        except NoSuchElementException:
            date = None
        # try:
        #     room_element = offer_element.find_element(By.CLASS_NAME, 'room')
        #     room = room_element.text.split('\n') if room_element else None
        # except NoSuchElementException:
        #     room = None
        # try:
        #     feeding_element = offer_element.find_element(By.CLASS_NAME, 'meal')
        #     feeding = feeding_element.text.split('\n') if feeding_element else None
        # except NoSuchElementException:
        #     feeding = None
        # try:
        #     nights_element = offer_element.find_element(By.CLASS_NAME, 'trip-choice-departure')
        #     nights = nights_element.text[0] if nights_element else None
        # except NoSuchElementException:
        #     nights = None
        # try:
        #     price_element = offer_element.find_element(By.CLASS_NAME, 'trip-choice-table-price-total')
        #     price = price_element.text.replace('€', '') if price_element else None
        # except NoSuchElementException:
        #     price = None
        trip_details = {
            'Description': description,
            'Destination': destination,
            'Date': date,
            'Hotel Stars': hotel_stars,
            # 'Room': room,
            # 'Feeding': feeding,
            # 'Nights': nights,
            # 'Price': price
        }
        trip_details_list.append(trip_details)
        rows_count += 1
        if rows_count % save_interval == 0:
            df = pd.DataFrame(trip_details_list)
            df.to_csv('csv/westexpress.csv', index=False)
            print('Additional data has been added to .csv')
        time.sleep(5)
    df = pd.DataFrame(trip_details_list)
    df.to_csv('csv/westexpress.csv', index=False)
    print(df)
df = pd.DataFrame(trip_details_list)
df.to_csv('csv/westexpress.csv', index=False)
print(df)
