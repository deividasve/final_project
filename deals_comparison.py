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

# Formatting data types and overriding existing .csv file with updated DataFrame
df['Date'] = pd.to_datetime(df['Date'])
df['Hotel Stars'] = pd.to_numeric(df['Hotel Stars'])
df.to_csv('csv/deals_comparison.csv', index=False)

# Last Minute Average Trip Price by Provider
price_avg_per_provider = df.groupby('Provider')['Price'].mean()
plt.figure(figsize=(12, 8))
price_avg_per_provider.plot(kind='bar', color='olive')
plt.title('Last Minute Average Trip Price by Provider')
plt.xlabel('Provider')
plt.ylabel('Price average')
plt.xticks(rotation=0)
plt.show()


# A function that trims the ending of element name
def truncate_title(title, max_length=11):
    if len(title) > max_length:
        return title[:max_length] + '...'
    return title


# Average Price per Country by Provider
df['Country'] = df['Country'].apply(truncate_title)
plt.figure(figsize=(10, 10))
sns.barplot(x='Country', y='Price', hue='Provider', data=df)
plt.title('Average Price per Country by Provider')
plt.xlabel('Country')
plt.ylabel('Average Price')
plt.xticks(rotation=45)
plt.grid()
plt.show()

# Average Price per Hotel Stars by Provider
plt.figure(figsize=(10, 8))
sns.lineplot(x='Hotel Stars', y='Price', hue='Provider', data=df)
plt.title('Average Price per Hotel Stars by Provider')
plt.xlabel('Hotel Stars')
plt.ylabel('Average Price')
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
plt.figure(figsize=(10, 10))
plt.subplot(2, 2, 1)
plt.pie(percentage_5stars, labels=percentage_5stars.index, startangle=90, autopct='%1.1f%%', colors='green')
plt.title('Percentage of 5-Star Hotel Deals by Provider')
plt.subplot(2, 2, 2)
plt.pie(percentage_4stars, labels=percentage_4stars.index, startangle=90, autopct='%1.1f%%')
plt.title('Percentage of 4-Star Hotel Deals by Provider')
plt.subplot(2, 2, 3)
plt.pie(percentage_3stars, labels=percentage_3stars.index, startangle=90, autopct='%1.1f%%')
plt.title('Percentage of 3-Star Hotel Deals by Provider')
plt.subplot(2, 2, 4)
plt.pie(percentage_2stars, labels=percentage_2stars.index, startangle=90, autopct='%1.1f%%', colors='green')
plt.title('Percentage of 2-Star Hotel Deals by Provider')
plt.show()

# Correlation Matrix for price, hotel rating, season, nights
correlation_matrix = df[['Price', 'Hotel Stars', 'Nights']].corr()
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation Matrix for Price, Hotel Stars, and Nights')
plt.show()

# Average Price per Date by Provider
plt.figure(figsize=(20, 8))
sns.lineplot(x='Date', y='Price', data=df, hue='Provider', palette='spring', marker='o')
sns.set_theme(font_scale=2)
plt.title('Average Price per Date by Provider')
plt.xlabel('Date')
plt.ylabel('Average Price')
plt.grid()
plt.show()
