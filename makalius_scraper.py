import pandas as pd
import requests
from bs4 import BeautifulSoup

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
trip_data = []
for i in range(1, 11):
    url = f'https://www.makalius.lt/paskutine-minute/puslapis/{i}/'

# A function that retrieves all the available websites links and extends the DataFrame
    def scrape_links(url):
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            trips = soup.find_all('div', class_='offer')
            for trip in trips:
                link = trip.find('a', class_='link')
                if link:
                    href = link.get('href')
                    trip_details = scrape_details(href)
                    if trip_details:
                        trip_data.extend(trip_details)
        except Exception as e:
            print(f'Error: {e}')
        return trip_data

# A function that retrieves all required data of travel deals from the website
    def scrape_details(link):
        response = requests.get(link)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Collecting easily accessible data: description, destination, hotel rating and travel type (transport)
        destination = soup.find('div', class_='valign').text.strip()
        description = soup.find('div', class_='offer-top').text.strip()

        # Searching what kind of travel type (transport) is
        offer_feature_element_plane = soup.find('i', class_='ico-plane-dark')
        offer_feature_element_bus = soup.find('i', class_='ico-bus-dark')
        if offer_feature_element_plane:
            offer_transport = offer_feature_element_plane.get('title')
        elif offer_feature_element_bus:
            offer_transport = offer_feature_element_bus.get('title')
        else:
            offer_transport = None
        offer_feature_element_hotel = soup.find('i', class_='ico-comments-dark')
        if offer_feature_element_hotel:
            offer_feature_hotel = offer_feature_element_hotel.get('title')
        else:
            offer_feature_hotel = None
        trip_details_list = []

        # Webpage has multiple deals thus it is required to use additional loop to gather required data of each deal
        possible_deals = [
            'offers-list offers-list-date li-check-mark',
            'block block-position-1 block-combination block-selector clearfix last-border',
            'block block-position-1 block-combination block-selector clearfix',
            'block block-position-2 block-combination block-selector clearfix',
            'block block-position-3 block-combination block-selector clearfix'
        ]
        for j in possible_deals:
            deals = soup.find_all('div', class_=j)
            for deal in deals:
                date_element = deal.find('div', class_='date')
                if date_element is None:
                    date_element = deal.find('strong', class_='visible-sm visible-xs mb5')
                date = date_element.text.strip() if date_element else None
                duration_nights_element = deal.find('div', class_='pull-left length')
                duration_nights = duration_nights_element.find('em').text.strip().split()[0] \
                    if duration_nights_element else None
                price_element = deal.find('div', class_='pull-left price')
                price = price_element.find('span').text.strip().split()[0] if price_element else None
                short_info_element = deal.find('span', class_='offers-description')
                short_info = short_info_element.text.strip() if short_info_element else None

                # Standardizing 'feeding' element values
                feeding = None
                if 'su pusryčiais' in short_info:
                    feeding = 'Pusryčiai'
                elif 'viskas įskaičiuota' in short_info:
                    feeding = 'Viskas įskaičiuota'
                elif 'pusryčiais ir vakarienėmis' in short_info:
                    feeding = 'Pusryčiai ir vakarienė'
                elif 'su pilnu maitinimu' in short_info:
                    feeding = 'Pusryčiai, pietūs, vakarienė'

                # Describing dictionary elements
                trip_details = {
                    'Description': description,
                    'Destination': destination,
                    'Date': date,
                    'Travel Transport': offer_transport,
                    'Hotel Stars': offer_feature_hotel,
                    'Nights': duration_nights,
                    'Feeding': feeding,
                    'Price': price,
                    'Info': short_info
                }
                trip_details_list.append(trip_details)
        return trip_details_list
    scrape_links(url)

# Updating DataFrame and creating a .csv file after script is finished
df = pd.DataFrame(trip_data)
df.to_csv('csv/makalius.csv', index=False)
print(df)
