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
url = 'https://www.novaturas.lt/paskutine-minute'
gecko_service = Service(GeckoDriverManager().install())
gecko_service.start()
driver = webdriver.Firefox(service=gecko_service)
driver.get(url)
time.sleep(2)
cookies = WebDriverWait(driver, 10).until(
    ec.element_to_be_clickable((By.CSS_SELECTOR, 'button.GDPR-Button:nth-child(1)')))
cookies.click()
a = 0
while a < 0:
    load_more = WebDriverWait(driver, 10).until(ec.element_to_be_clickable((By.CSS_SELECTOR, 'button.c-gutLLG:nth-child(1)')))
    load_more.click()
    time.sleep(2)
    a += 1
trip_details_list = []
web_link = [link.get_attribute('href') for link in driver.find_elements(By.CSS_SELECTOR, '.c-foxNNj a')]
for link in web_link:
    full_link = f'{link}'
    driver.get(full_link)
    time.sleep(2)
    description_element = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.CSS_SELECTOR, 'h1.c-PJLV')))
    description = description_element.text
    # destination_element = driver.find_element(By.CLASS_NAME, 'c-bTjFtG')
    # destination = destination_element.text if destination_element else None
    destination_element = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.CSS_SELECTOR, '.c-bTjFtG')))
    destination = destination_element.text
    offer_transport_element = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.CSS_SELECTOR, 'li.c-eeCjTt:nth-child(1)')))
    offer_transport = offer_transport_element.text
    # hotel_element = WebDriverWait(driver, 10).until(
    #     ec.presence_of_element_located((By.CSS_SELECTOR, 'div.c-hnbPrw:nth-child(1) > div:nth-child(1)')))
    # if 'c-dPemeR c-lgAqJq c-lgAqJq-eCncRB-isFull-true' in hotel_element:
    #     hotel = 5
    # hotel = offer_feature_hotel_element.text if offer_feature_hotel_element else None
    offer_elements = driver.find_elements(By.CLASS_NAME, 'c-kQzNuN')
    for offer_element in offer_elements:
        room_element = driver.find_element(By.CLASS_NAME, 'c-juEpcc')
        room = room_element.text if room_element else None
        nights_element = driver.find_element(By.CLASS_NAME, 'c-eaRLdk')
        nights = nights_element.text[0] if nights_element else None
        date_element = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, 'div.c-kQzNuN:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > span:nth-child(2)')))
        date = date_element.text

        # service_element = WebDriverWait(driver, 10).until(
        #     ec.presence_of_element_located((By.CSS_SELECTOR, 'div.c-kQzNuN:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(3)')))
        # service = service_element.text

        # service_element = WebDriverWait(driver, 10).until(
        #     ec.presence_of_element_located((By.CSS_SELECTOR, 'c-iljIzD')))
        # service = service_element.text

        service_element = driver.find_element(By.CLASS_NAME, 'c-iljIzD')
        service = service_element.text if service_element else None

        price_element = driver.find_element(By.CLASS_NAME, 'c-bkJVKH')
        price = price_element.text if price_element else None
        trip_details = {
            'Description': description,
            'Destination': destination,
            'Date': date,
            'Travel Transport': offer_transport,
            # 'Hotel': offer_feature_hotel,
            'Room': room,
            'Service': service,
            'Nights': nights,
            'Price': price,
            # 'Info': short_info
        }
        trip_details_list.append(trip_details)
    time.sleep(2)
df = pd.DataFrame(trip_details_list)
df.to_csv('csv/novaturas.csv', index=False)
print(df)
driver.quit()

# price_element = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.CSS_SELECTOR, '')))
# price = price_element.text