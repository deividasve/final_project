import pandas as pd
import requests
from bs4 import BeautifulSoup

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
trip_data = []
for i in range(1, 2):
    url = f'https://www.westexpress.lt/paskutine-minute?page={i}/'

    def scrape_links(url):
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            link = soup.find_all('a', class_='travel-block')
            for h in link:
                href = h.get('href')
                trip_details = scrape_details(href)
                if trip_details:
                    trip_data.extend(trip_details)
        except Exception as e:
            print(f'Error: {e}')
        return trip_data


    def scrape_details(link):
        response = requests.get(link)
        trip_details_list = []
        soup = BeautifulSoup(response.content, 'html.parser')
        destination = soup.find('li', class_='destination').text.strip()
        description = soup.find('div', class_='nopad section-title-lg').text.strip()

        trip_details = {
            'Description': description,
            'Destination': destination,
        #     'Date': date,
        #     'Travel Transport': offer_transport,
        #     'Hotel': offer_feature_hotel,
        #     'Nights': duration_nights,
        #     'Service': service,
        #     'Price': price,
        #     'Info': short_info
        }
        trip_details_list.append(trip_details)
        return trip_details_list

    a = scrape_links(url)
df = pd.DataFrame(trip_data)
df.to_csv('csv/makalius.csv', index=False)
print(df)