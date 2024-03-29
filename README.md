# TRAVEL SITE (Makalius, Novaturas) LAST MINUTE DEALS ANALYSIS

## Details
Created by: Deividas Verbickas and Justė Petrėnė

This is the end project in Vilnius Coding School

## Project theme: Last minute travel deal data analysis and visualization

The main goal of the project is to find out the price differences by different last minute travel providers.

In this project we used Python and CSV files showcasing our practical coding skills acquired at Vilnius Coding School.


## Applied knowledge:
Used libraries: BeautifulSoup, Pandas, MatplotLib, SeaBorn, Selenium

makalius_scraper.py

Getting data from URL: https://www.makalius.lt/paskutine-minute

novaturas_scraper.py

Getting data from URL: https://www.novaturas.lt/paskutine-minute

deals_comparison.py

This is the main project file where all analysis were made. All visuals are controlled by functions, which helps to separate all graphs in the code.


## Results

Average Trip Price by provider:
![image](https://github.com/deividasve/final_project/assets/156001818/a850ffc5-7d5a-45ae-8219-35f1a41d1c4f)
According to this graph, "Makalius" offers cheaper last minute deals.

Last Minute Average Trip Price by Provider:
![image](https://github.com/deividasve/final_project/assets/156001818/0606bcd4-8252-42ab-92bc-aa9f8e9f4a4e)
This graph shows that the most expensive place to visit is Sri Lanka (provider: "Novaturas"), Maldives (provider: "Novaturas") and Dominican Republic (provider: "Makalius"), while cheapest offers are to Estonia (provider: "Makalius"), Poland (provider: "Novaturas") and France (provider: "Makalius").

Average Price per Hotel Stars by Provider:
![image](https://github.com/deividasve/final_project/assets/156001818/a65272e1-fda3-461e-ae34-61191b7f0e6f)
Analysis of price differences by Hotel Stars and Providers shows that travel provider "Makalius" offers cheaper prices in all Hotel Stars categories.

Correlation Matrix for price, hotel rating, season, nights:
![image](https://github.com/deividasve/final_project/assets/156001818/43753bb7-4472-4f86-98b9-f5a07eb7af39)
This graph shows that price differences correlate the most with the count of nights spent at given hotel (0,14).

Average Price per Date by Provider:
![image](https://github.com/deividasve/final_project/assets/156001818/c2dad4e4-8634-4550-8965-44b45461a686)
In this graph, we can see that "Makalius" provides offers from February to June and at this time, offers for trips in May and June are the cheapest. Meanwhile, Novaturas offers trips from begining to the middle of February.


## Conclusion

Analysis of the Last Minute Travel Offers shows that the site "Makalius" overall cheaper offers than "Novaturas". "Makalius" also has cheaper offers of same star rating hotels compared to its competitor "Novaturas". Our analysis shows that the most expensive place to visit is Sri Lanka (provider: "Novaturas"), Maldives (provider: "Novaturas") and Dominican Republic (provider: "Makalius"), while cheapest offers are to Estonia (provider: "Makalius"), Poland (provider: "Novaturas") and France (provider: "Makalius"). This is likely influenced by the distance, trip duration and means of transport to locations mentioned before. A weak correlation (0,14) between offer price and nights spent at a hotel was also found.
