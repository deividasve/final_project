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

# link = 'https://www.westexpress.lt/kelione-i-jungtine-karalyste/peckham-rooms-hotel-londone-2553#date/2024-03-14/2/0/8|10|12/2-7'
link = 'https://www.westexpress.lt/kelione-i-austrija/hotel-mozart-vienoje-2252#date/2024-03-26/2/0/8|10|12/2-7'
gecko_service = Service(GeckoDriverManager().install())
gecko_service.start()
driver = webdriver.Firefox(service=gecko_service)
driver.get(link)
time.sleep(5)
trip_details_list = []
# web_link = [link.get_attribute('href') for link in driver.find_elements(By.CSS_SELECTOR, 'a.travel-block')]
save_interval = 1
rows_count = 0
full_link = f'{link}'
driver.get(link)





time.sleep(5)
# cookies = WebDriverWait(driver, 100).until(
#     ec.element_to_be_clickable((By.CSS_SELECTOR, '.close')))
# cookies.click()
response = requests.get(link)

print(full_link)

soup = BeautifulSoup(response.content, 'html.parser')
destination = soup.find('li', class_='destination').text.strip()
description = soup.find('div', class_='nopad section-title-lg').text.strip()
hotel_stars_element = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.CSS_SELECTOR, '.h2')))
hotel_stars = hotel_stars_element.text[0]
# offer_elements = driver.find_elements(By.CLASS_NAME, 'trip-choice-table-row')
html_code = driver.page_source
# print(html_code)
soup = BeautifulSoup(html_code, 'html.parser')
trimmed_soup = soup.find('div', class_='small-12 columns nopad trip-choice-table-body')
# print(trimmed_soup)

# offer_elements = driver.find_elements(By.CLASS_NAME, 'trip-choice-table-row')
offer_elements = trimmed_soup.find_element(By.CLASS_NAME, 'trip-choice-table-row')
for offer_element in offer_elements:
    try:
        date_element = offer_element.find_element(By.CLASS_NAME, 'trip-choice-days-large')
        date = date_element.text.split(' → ')[0].replace(' ', '-') if date_element else None
    except NoSuchElementException:
        date = None
    try:
        room_element = offer_element.find_element(By.CLASS_NAME, 'room')
        # room = room_element.text.split('\n')[1] if room_element else None
        room = room_element.text.split('\n') if room_element else None
    except NoSuchElementException:
        room = None
    try:
        feeding_element = offer_element.find_element(By.CLASS_NAME, 'meal')
        feeding = feeding_element.text.split('\n')[1].replace('Be maitinimo', '') if feeding_element else None
    except NoSuchElementException:
        feeding = None
    try:
        nights_element = offer_element.find_element(By.CLASS_NAME, 'trip-choice-departure')
        nights = nights_element.text[0] if nights_element else None
    except NoSuchElementException:
        nights = None
    try:
        price_element = offer_element.find_element(By.CLASS_NAME, 'trip-choice-table-price-total')
        price = price_element.text.replace('€', '') if price_element else None
    except NoSuchElementException:
        price = None
    trip_details = {
        'Description': description,
        'Destination': destination,
        'Date': date,
        'Hotel Stars': hotel_stars,
        'Room': room,
        'Feeding': feeding,
        'Nights': nights,
        'Price': price
    }
    trip_details_list.append(trip_details)
    rows_count += 1
    if rows_count % save_interval == 0:
        df = pd.DataFrame(trip_details_list)
        df.to_csv('csv/westexpress.csv', index=False)
        print('Additional data has been added to .csv')
    time.sleep(2)
df = pd.DataFrame(trip_details_list)
df.to_csv('csv/westexpress.csv', index=False)
print(df)


# try:
#     date_element = WebDriverWait(driver, 30).until(
#         ec.presence_of_element_located((By.CSS_SELECTOR,
#             'div.trip-choice-table-body:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > span:nth-child(1)')))
#     date = date_element.text
# except TimeoutException:
#     print('CSS_SELECTOR or Website not found')
#     continue


