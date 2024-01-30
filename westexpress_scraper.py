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
        date_element = soup.find('div', class_='trip-choice-days-large')
        if date_element is None:
            date_element = soup.find('span')
        date = date_element.text.strip() if date_element else None
        duration_nights = soup.find('div', class_='trip-choice-departure').text.strip()[0]
        price = soup.find('span', class_='trip-choice-table-price-total').text.strip().replace('€', '')
        meal_info_element = soup.find('li', class_='meal')
        if meal_info_element is None:
            meal_element = soup.find('span')
        meal = meal_element.text.strip() if meal_element else None
        hotel_rating = soup.find('div', class_='h2').text.strip()[0]

        trip_details = {
            'Description': description,
            'Destination': destination,
            'Price': price,
            'Length': duration_nights,
            'Date': date,
            'Meal': meal,
            'Hotel Rating': hotel_rating
        }
        trip_details_list.append(trip_details)
        return trip_details_list

    a = scrape_links(url)
df = pd.DataFrame(trip_data)
# df.to_csv('csv/westexpress.csv', index=False)
print(df)