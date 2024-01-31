import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

# for i in range(1, 18):
#     url = f'https://www.westexpress.lt/paskutine-minute?page={i}/'

url = 'https://www.westexpress.lt/paskutine-minute?page=1'
service = Service(ChromeDriverManager().install())
service.start()
driver = webdriver.Chrome(service=service)
driver.get(url)
time.sleep(5)
trip_details_list = []
web_link = [link.get_attribute('href') for link in driver.find_elements(By.CSS_SELECTOR, 'a.travel-block')]
# 'a.travel-block:nth-child(1)'
for link in web_link:
    full_link = f'{link}'
    # print(full_link)
    driver.get(full_link)
    time.sleep(5)
    response = requests.get(link)
    trip_details_list = []
    soup = BeautifulSoup(response.content, 'html.parser')
    destination = soup.find('li', class_='destination').text.strip()
    description = soup.find('div', class_='nopad section-title-lg').text.strip()
    try:
        date_element = WebDriverWait(driver, 30).until(
            ec.presence_of_element_located((By.CSS_SELECTOR,
                'div.trip-choice-table-body:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > span:nth-child(1)')))
        date = date_element.text
    except TimeoutException:
        print('CSS_SELECTOR or Website not found')
        continue

    date_element = WebDriverWait(driver, 30).until(
        ec.presence_of_element_located((By.CSS_SELECTOR,
                                        'div.trip-choice-table-body:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > span:nth-child(1)')))
    date = date_element.text

    price_element = WebDriverWait(driver, 25).until(ec.presence_of_element_located((By.CSS_SELECTOR,
                                        'div.trip-choice-table-body:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > span:nth-child(2)')))
    price = price_element.text.replace('€', '')
    length_element = WebDriverWait(driver, 25).until(ec.presence_of_element_located((By.CSS_SELECTOR,
                                        'div.trip-choice-table-body:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2)')))
    length = length_element.text[0]
    meal_element = WebDriverWait(driver, 25).until(ec.presence_of_element_located((By.CSS_SELECTOR,
                                        'div.trip-choice-table-body:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > ul:nth-child(1) > li:nth-child(2) > div:nth-child(2) > span:nth-child(1)')))
    meal = meal_element.text
    hotel_rating_element = WebDriverWait(driver, 25).until(ec.presence_of_element_located((By.CSS_SELECTOR, '.h2')))
    hotel_rating = hotel_rating_element.text[0]

    trip_details = {
        'Description': description,
        'Destination': destination,
        'Date': date,
        'Price': price,
        'Length': length,
        'Meal': meal,
        'Hotel Rating': hotel_rating
    }
    trip_details_list.append(trip_details)
    time.sleep(5)
df = pd.DataFrame(trip_details_list)
# df.to_csv('csv/WestExpress.csv', index=False)
print(df)