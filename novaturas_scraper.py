import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
url = 'https://www.novaturas.lt/paskutine-minute'
service = Service(GeckoDriverManager().install())
service.start()
driver = webdriver.Firefox(service=service)
driver.get(url)
time.sleep(2)
cookies = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.GDPR-Button:nth-child(1)')))
cookies.click()
a = 0
# while a < 1:
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#     try:
#         load_more = WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.c-gutLLG:nth-child(1)')))
#         load_more.click()
#         time.sleep(2)
#         a += 1
#     except TimeoutException:
#         break
while a < 5:
    load_more = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.c-gutLLG:nth-child(1)')))
    load_more.click()
    time.sleep(2)
    a += 1
trip_details_list = []
film_link = [link.get_attribute('href') for link in
             driver.find_elements(By.CSS_SELECTOR, '.c-foxNNj a')]
for link in film_link:
    full_link = f'{link}'
    driver.get(full_link)
    description_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'h1.c-PJLV')))
    description = description_element.text if description_element else None
    destination_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.c-bTjFtG')))
    destination = destination_element.text if description_element else None
    # offer_transport_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.c-hjDhzf > div:nth-child(3) > div:nth-child(2)')))
    # offer_transport = offer_transport_element.text if offer_transport_element else None
    # price_element = WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.CSS_SELECTOR,
    #                                     'div.c-khfJHt:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > span:nth-child(1)')))
    # price = price_element.text if price_element else None
    # nights_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,
    #                                     'div.c-khfJHt:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > span:nth-child(1)')))
    # nights = nights_element.text if nights_element else None
    trip_details = {
        'Description': description,
        'Destination': destination,
        # 'Travel Transport': offer_transport,
        # 'Nights': nights,
        # 'Price': price
    }
    trip_details_list.append(trip_details)
    time.sleep(2)
df = pd.DataFrame(trip_details_list)
print(df)
driver.quit()

# price_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '')))
# price = price_element.text

# trip_details = {
#     'Description': description,
#     'Destination': destination,
#     'Date': date,
#     'Travel Transport': offer_transport,
#     'Hotel': offer_feature_hotel,
#     'Nights': duration_nights,
#     'Service': service,
#     'Price': price,
#     'Info': short_info