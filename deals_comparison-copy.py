import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 500)
pd.set_option('display.width', 500)

# Importing DataFrames, cleaning, formatting values and assigning a provider for each DataFrame
df1 = pd.read_csv('csv/makalius.csv')
df1['Provider'] = 'Makalius'

# Removing cruises from the DataFrame
cruises = ['Kruizas „MSC Orchestra“', 'Karibų kruizas su „MSC Seascape”']
df1 = df1[df1.Destination.isin(cruises) == False]

# Specifying 'Destination' column from Makalius DataFrame
df1['Destination'] = (df1['Destination'].str.replace('Saremos sala', 'Estija, Saremos sala')
                      .str.replace('Pažintinis Egiptas', 'Egiptas').str.replace('Dubajus', 'JAE, Dubajus')
                      .str.replace('Madeira', 'Portugalija, Madeira').str.replace('Tenerifė', 'Ispanija, Tenerifė')
                      .str.replace('Zanzibaras', 'Tanzanija, Zanzibaras').str.replace('Roma', 'Italija, Roma')
                      .str.replace('Paryžius', 'Prancūzija, Paryžius')
                      .str.replace('Kanarų Salos', 'Ispanija, Kanarų Salos'))

# Creating a new 'Country' column based on 'Destination' data
df1['Country'] = (df1['Destination'].apply(lambda x: x.split()[0] if x != 'Dominikos Respublika'
                  and x != 'Žaliasis Kyšulys' and x != 'Šri Lanka' else x)
                  .str.replace(',', ''))

df1['Date'] = df1['Date'].str.replace('Data: ', '').str.split().str[0]
df1['Hotel Stars'] = df1['Hotel Stars'].str.replace(' žvaigždučių viešbutis', '')
df2 = pd.read_csv('csv/novaturas.csv')
df2['Provider'] = 'Novaturas'
df2['Country'] = df2['Destination'].str.split(', ').str[-1]

# Merging DataFrames
df = pd.concat([df1, df2], ignore_index=True)

# Creating new 'Season' column by converting 'Month' column data based on value
df['Date'] = pd.to_datetime(df['Date'])
df['Month'] = df['Date'].dt.month
df.loc[(df['Month'] >= 3) & (df['Month'] <= 5), 'Season'] = 'Spring'
df.loc[(df['Month'] >= 6) & (df['Month'] <= 8), 'Season'] = 'Summer'
df.loc[(df['Month'] >= 9) & (df['Month'] <= 11), 'Season'] = 'Autumn'
df.loc[~((df['Month'] >= 3) & (df['Month'] <= 11)), 'Season'] = 'Winter'
df['Hotel Stars'] = pd.to_numeric(df['Hotel Stars'])

df.to_csv('csv/deals_comparison-copy.csv', index=False)


# Grouping Price averages by Providers
price_avg_per_provider = df.groupby('Provider')['Price'].mean()
# print(price_avg_per_provider)
# Creating barplot for Average price by Provider
# plt.figure(figsize=(12, 8))
# price_avg_per_provider.plot(kind='bar')
# plt.title('Last minute average trip price by Provider')
# plt.xlabel('Provider')
# plt.ylabel('Price average')
# plt.show()

# Grouping Price averages by Countries
# price_avg_per_country = df.groupby('Country')['Price'].mean()
# print(price_avg_per_country)

# Creating barplot for Average price by Country
# plt.figure(figsize=(12, 8))
# price_avg_per_country.plot(kind='bar')
# plt.title('Last minute average trip price by Country')
# plt.xlabel('Country')
# plt.ylabel('Price average')
# plt.show()


# isfiltruotas_df_egiptas = df[df['Country'] == 'Egiptas']
# grouped_egypt_by_season = isfiltruotas_df_egiptas.groupby(df['Season'])['Price']
# plt.figure(figsize=(12, 8))
# grouped_egypt_by_season.plot(kind='line')
# plt.title('Last minute price for Egypt by Season')
# plt.xlabel('Price')
# plt.ylabel('Season')
# plt.show()



# A function that trims the ending of element name
def truncate_title(title, max_length=11):
    if len(title) > max_length:
        return title[:max_length] + '...'
    return title


# 11.
# Average Price per Country by Provider
# df['Country'] = df['Country'].apply(truncate_title)
# plt.figure(figsize=(10, 10))
# sns.barplot(x='Country', y='Price', hue='Provider', data=df)
# plt.title('Average Price per Country by Provider')
# plt.xlabel('Country')
# plt.ylabel('Average Price')
# plt.xticks(rotation=45)
# plt.grid()
# plt.show()

# Average Price per Hotel Stars by Provider
avg_price_stars = df['Price'].mean()
df['Hotel Stars'] = df['Hotel Stars'].replace('.0', '')
plt.figure(figsize=(10, 10))
sns.barplot(x='Hotel Stars', y='Price', hue='Provider', data=df)
plt.title('Count of Deals per Hotel Rating by Provider')
plt.xlabel('Hotel Stars')
plt.ylabel('Average Price')
# plt.axhline(avg_price_stars, color='seagreen', linestyle='dashed', label=f'Average: {avg_price_stars:.2f}')
plt.grid()
plt.show()


# Percentage of Deals per Hotel Rating by Provider
df = df.dropna(subset=['Hotel Stars'])
df_5stars = df[df['Hotel Stars'] == 5]
df_4stars = df[df['Hotel Stars'] == 4]
df_3stars = df[df['Hotel Stars'] == 3]
df_2stars = df[df['Hotel Stars'] == 2]
count_5stars_by_provider = df_5stars.groupby('Provider')['Hotel Stars'].count()
count_4stars_by_provider = df_4stars.groupby('Provider')['Hotel Stars'].count()
count_3stars_by_provider = df_3stars.groupby('Provider')['Hotel Stars'].count()
count_2stars_by_provider = df_2stars.groupby('Provider')['Hotel Stars'].count()
total_counts_5stars = count_5stars_by_provider.sum()
total_counts_4stars = count_4stars_by_provider.sum()
total_counts_3stars = count_3stars_by_provider.sum()
total_counts_2stars = count_2stars_by_provider.sum()
percentage_5stars = count_5stars_by_provider / total_counts_5stars * 100
percentage_4stars = count_4stars_by_provider / total_counts_4stars * 100
percentage_3stars = count_3stars_by_provider / total_counts_3stars * 100
percentage_2stars = count_2stars_by_provider / total_counts_2stars * 100
# plt.figure(figsize=(10, 10))
# plt.subplot(2, 2, 1)
# plt.pie(percentage_5stars, labels=percentage_5stars.index, startangle=90, autopct='%1.1f%%', colors='green')
# plt.title('Percentage of 5-Star Hotel Deals by Provider')
# plt.subplot(2, 2, 2)
# plt.pie(percentage_4stars, labels=percentage_4stars.index, startangle=90, autopct='%1.1f%%')
# plt.title('Percentage of 4-Star Hotel Deals by Provider')
# plt.subplot(2, 2, 3)
# plt.pie(percentage_3stars, labels=percentage_3stars.index, startangle=90, autopct='%1.1f%%')
# plt.title('Percentage of 3-Star Hotel Deals by Provider')
# plt.subplot(2, 2, 4)
# plt.pie(percentage_2stars, labels=percentage_2stars.index, startangle=90, autopct='%1.1f%%', colors='green')
# plt.title('Percentage of 2-Star Hotel Deals by Provider')
# plt.show()

# Count of Deals per Hotel Rating by Provider
# plt.figure(figsize=(10, 10))
# sns.lineplot(x='Hotel Stars', y='Price', hue='Provider', data=df)
# plt.show()

# Correlation Matrix for price, hotel rating, season, nights
correlation_matrix = df[['Price', 'Hotel Stars', 'Nights']].corr()
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation Matrix for price, hotel rating, nights')
plt.show()







"""# 1. Top 10 Lowest Price Deals by Country

# 2. Seasonal Average Price by Provider Grouped by Country

# 3. Count of Deals per Hotel Rating by Provider

# 4. Count of Stays by Provider

# 5. Average Price per Stays by Provider

# 6. Average Price per Hotel Rating by Provider

# 7. The most popular Countries by Provider's Deals Count

# 8. Percentange of Different Country Coverage by Provider

# 9. Showcase Country Location Pins on Map by Provider

# 10. Average Price per Season by Provider

# 11. Average Price per Country by Provider"""

"""
# Correlation Matrix for price, hotel rating, season, nights
correlation_matrix = df[['Price', 'Hotel Stars', 'Nights']].corr()
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation Matrix for price, hotel rating, nights')
plt.show()



"""
