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

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
# for i in range(1, 2):
#     url = f'https://www.westexpress.lt/paskutine-minute?page={i}/'

url = 'https://www.westexpress.lt/paskutine-minute?page=1'
gecko_service = Service(GeckoDriverManager().install())
gecko_service.start()
driver = webdriver.Firefox(service=gecko_service)
driver.get(url)
time.sleep(2)
trip_details_list = []
web_link = [link.get_attribute('href') for link in driver.find_elements(By.CSS_SELECTOR, 'a.travel-block')]
# 'a.travel-block:nth-child(1)'
for link in web_link:
    full_link = f'{link}'
    print(full_link)
    driver.get(full_link)
    time.sleep(2)
    response = requests.get(link)
    trip_details_list = []
    soup = BeautifulSoup(response.content, 'html.parser')
    destination = soup.find('li', class_='destination').text.strip()
    description = soup.find('div', class_='nopad section-title-lg').text.strip()
    date_element = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.CSS_SELECTOR,
                                        'div.trip-choice-table-body:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > span:nth-child(1)')))
    date = date_element.text
    trip_details = {
        'Description': description,
        'Destination': destination,
        'Date': date,
    }
    trip_details_list.append(trip_details)
df = pd.DataFrame(trip_details_list)
print(df)