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
try:
    cookies = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.GDPR-Button:nth-child(1)')))
    cookies.click()
    # while True:
    #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #     try:
    #         load_more = WebDriverWait(driver, 10).until(
    #             EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.c-PJLV:nth-child(2)')))
    #         load_more.click()
    #         time.sleep(2)
    #     except TimeoutException:
    #         break

    # link = WebDriverWait(driver, 10).until(
    #         EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.c-foxNNj:nth-child(1) > a:nth-child(1)')))
    # link.click()
    link_list = driver.find_elements(By.CSS_SELECTOR, 'div.c-foxNNj:nth-child(1) > a:nth-child(1) > div:nth-child(1) > div:nth-child(3) > div:nth-child(3) > button:nth-child(3)')
    print(link_list)

    # description_element = WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.CSS_SELECTOR, 'h1.c-PJLV')))
    # description = description_element.text
    # price_element = WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.CSS_SELECTOR, '.c-bkJVKH-jdRMib-discounts-enabled')))
    # price = price_element.text
    # print(price, description)
    # find_all('div', class_='c-MMqCZ c-jDKfzn')


except Exception as e:
    print(f'Ivyko nezinoma klaida: {e}')
finally:
    driver.quit()

# price_element = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.CSS_SELECTOR, '')))
# price = price_element.text