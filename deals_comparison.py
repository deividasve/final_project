import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 500)
pd.set_option('display.width', 500)
df1 = pd.read_csv('csv/makalius.csv')
df1['Provider'] = 'Makalius'
df1['Date'] = df1['Date'].str.replace('Data: ', '').str.split().str[0]
df1['Hotel Stars'] = df1['Hotel Stars'].str.replace(' žvaigždučių viešbutis', '')
df2 = pd.read_csv('csv/makalius.csv')
df2['Provider'] = 'Novaturas'
df3 = pd.read_csv('csv/westexpress.csv')
df3['Provider'] = 'WestExpress'
df = pd.concat([df1, df2, df3], ignore_index=True)
df['Month'] = pd.to_datetime(df['Date']).dt.month
df.loc[(df['Month'] >= 3) & (df['Month'] <= 5), 'Season'] = 'Spring'
df.loc[(df['Month'] >= 6) & (df['Month'] <= 8), 'Season'] = 'Summer'
df.loc[(df['Month'] >= 9) & (df['Month'] <= 11), 'Season'] = 'Autumn'
df.loc[~((df['Month'] >= 3) & (df['Month'] <= 11)), 'Season'] = 'Winter'
df['Hotel Stars'] = pd.to_numeric(df['Hotel Stars'])
# df['Country'] = df['Destination'].str.replace(',', '').str.replace('.', '').str.split().str[0]
df['Country'] = df['Destination'].apply(lambda x: x.split()[0] if x != 'Žaliasis Kyšulys' else x)
df.to_csv('csv/deals_comparison.csv', index=False)

# Grouping Price averages by Providers
price_avg_per_provider = df.groupby('Provider')['Price'].mean()

# Creating barplot for Average price by Provider
plt.figure(figsize=(12, 8))
price_avg_per_provider.plot(kind='bar')
plt.title('Last minute average trip price by Provider')
plt.xlabel('Provider')
plt.ylabel('Price average')
plt.show()

# Grouping Price averages by Countries
price_avg_per_country = df.groupby('Country')['Price'].mean()

# Creating barplot for Average price by Country
plt.figure(figsize=(12, 8))
price_avg_per_country.plot(kind='bar')
plt.title('Last minute average trip price by Country')
plt.xlabel('Country')
plt.ylabel('Price average')
plt.show()

isfiltruotas_df_egiptas = df[df['Country'] == 'Egiptas']
grouped_egypt_by_season = isfiltruotas_df_egiptas.groupby(df['Season'])['Price']
plt.figure(figsize=(12, 8))
grouped_egypt_by_season.plot(kind='line')
plt.title('Last minute price for Egypt by Season')
plt.xlabel('Price')
plt.ylabel('Season')
plt.show()
