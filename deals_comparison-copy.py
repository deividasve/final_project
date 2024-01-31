import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 500)
pd.set_option('display.width', 500)

# Importing DataFrames, cleaning, formatting values and assigning a provider for each DataFrame
df1 = pd.read_csv('csv/makalius.csv')
df1['Provider'] = 'Makalius'

# Specifying 'Destination' column
df1['Destination'] = (df1['Destination'].str.replace('Saremos sala', 'Estija, Saremos sala')
  .str.replace('Pažintinis Egiptas', 'Egiptas').str.replace('Kruizas „MSC Orchestra“', 'Viduržemio jūra')
  .str.replace('Karibų kruizas su „MSC Seascape”', 'Karibų jūra').str.replace('Dubajus', 'JAE, Dubajus')
  .str.replace('Madeira', 'Portugalija, Madeira').str.replace('Tenerifė', 'Ispanija, Tenerifė')
  .str.replace('Zanzibaras', 'Tanzanija, Zanzibaras').str.replace('Roma', 'Italija, Roma'))

# Creating a new 'Country' column based on 'Destination' data
df1['Country'] = (df1['Destination'].apply(lambda x: x.split()[0] if x != 'Dominikos Respublika'
  and x != 'Žaliasis Kyšulys' and x != 'Šri Lanka' and x != 'Viduržemio jūra' and x != 'Karibų jūra' else x)
  .str.replace(',', ''))

df1['Date'] = df1['Date'].str.replace('Data: ', '').str.split().str[0]
df1['Hotel Stars'] = df1['Hotel Stars'].str.replace(' žvaigždučių viešbutis', '')
df2 = pd.read_csv('csv/novaturas.csv')
df2['Provider'] = 'Novaturas'
df2['Country'] = df2['Destination'].str.split(', ').str[-1]

# Merging DataFrames
df = pd.concat([df1, df2], ignore_index=True)

# Creating new 'Season' column by converting 'Month' column data based on value
df['Month'] = pd.to_datetime(df['Date']).dt.month
df.loc[(df['Month'] >= 3) & (df['Month'] <= 5), 'Season'] = 'Spring'
df.loc[(df['Month'] >= 6) & (df['Month'] <= 8), 'Season'] = 'Summer'
df.loc[(df['Month'] >= 9) & (df['Month'] <= 11), 'Season'] = 'Autumn'
df.loc[~((df['Month'] >= 3) & (df['Month'] <= 11)), 'Season'] = 'Winter'
df['Hotel Stars'] = pd.to_numeric(df['Hotel Stars'])

df.to_csv('csv/deals_comparison-copy.csv', index=False)

# Grouping Price averages by Providers
price_avg_per_provider = df.groupby('Provider')['Price'].mean()

# Creating barplot for Average price by Provider
plt.figure(figsize=(12, 8))
price_avg_per_provider.plot(kind='bar')
plt.title('Last minute average trip price by Provider')
plt.xlabel('Provider')
plt.ylabel('Price average')
# plt.show()

# Grouping Price averages by Countries
price_avg_per_country = df.groupby('Country')['Price'].mean()

# Creating barplot for Average price by Country
plt.figure(figsize=(12, 8))
price_avg_per_country.plot(kind='bar')
plt.title('Last minute average trip price by Country')
plt.xlabel('Country')
plt.ylabel('Price average')
# plt.show()

isfiltruotas_df_egiptas = df[df['Country'] == 'Egiptas']
grouped_egypt_by_season = isfiltruotas_df_egiptas.groupby(df['Season'])['Price']
plt.figure(figsize=(12, 8))
grouped_egypt_by_season.plot(kind='line')
plt.title('Last minute price for Egypt by Season')
plt.xlabel('Price')
plt.ylabel('Season')
# plt.show()
