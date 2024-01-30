import pandas as pd
import requests
from bs4 import BeautifulSoup

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 500)

trip_data = []

for i in range(1, 2):
    url = f'https://www.westexpress.lt/paskutine-minute?page={i}'
    # response = requests.get(url)
    # print(url)

    def scrape_links(url):
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            trips = soup.find_all('div', class_='travels main-catalog')
            for trip in trips:
                link = trip.find('a', class_='travel-block')
                if link:
                    href = link.get('href')
                    print(href)
                    trip_details = scrape_details(href)
                    if trip_details:
                        trip_data.extend(trip_details)
        except Exception as e:
            print(f'Uh-oh, something went wrong: {e}')
        return trip_data

    def scrape_details(link):
        response = requests.get(link)
        soup = BeautifulSoup(response.content, 'html.parser')
        destination_element = soup.find('div', class_='trip-info-titles')
        destination = destination_element.find('h3').text.strip()
        date_element = soup.find('span', class_='exact-date')
        date = date_element.find('svg').text.strip().split()[2] if date_element else 'N/A'
        length_element = soup.find('span', class_='exact-date')
        length = length_element.find('svg').text.strip().rsplit()[1].replace(' n.', '').replace(')', '') \
            if length_element else 'N/A'
        price = soup.find('span', class_='main-price').text.strip()
        rating = soup.find('span', class_='rate').text.strip()
        trip_details_list = []
        trip_details = {
            'Destination': destination,
            'Date': date,
            'Length': length,
            'Price': price,
            'Rating': rating
        }
        trip_details_list.append(trip_details)
        return trip_details_list


    a = scrape_links(url)
df = pd.DataFrame(trip_data)
print(df)