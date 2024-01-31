# TRAVEL SITE (Makalius, Novaturas, WestExpress) LAST MINUTE DEALS ANALYSIS

## Details
Created by: Deividas Verbickas and Justė Petrėnė

This is the end project in Vilnius Coding School

## Project theme: Last minute travel deal data analysis and visualization

The main goal of the project is to find out the price differences by different last minute travel providers.

In this project we used Python and CSV files showcasing our practical coding skills acquired at Vilnius Coding School.

## Applied knowledge:
Used libraries: Pandas, MatplotLib, SeaBorn, Selenium

makalius_scraper.py
Getting data from URL ("'https://www.makalius.lt/paskutine-minute/puslapis/{i}/").

novaturas_scraper.py
Getting data from URL https://www.novaturas.lt/paskutine-minute

westexpress_scraper.py
Getting data from URL https://www.westexpress.lt/paskutine-minute?page={i}

deals_comparison.py
Merging all csv file data into one csv file deals_comparison.csv. This is the main project file where all analysis were made. All visuals are controlled by functions, which helps to separate all graphs in the code.

## Results

Function price_avg_per_provider() provides this graph:
![image](https://github.com/deividasve/final_project/assets/156001818/4cc1fbf4-ac44-4c61-b302-31d9e56cc0d4)

Function price_avg_per_country() provides this graph:
![image](https://github.com/deividasve/final_project/assets/156001818/b7a4453e-aa05-4c5c-97ff-496657543baa)

Function grouped_egypt_by_season_and_provider() provides this graph:

## Conclusion

An analysis of the Last Minute Travel Offers shows that the since 2013 to 2023 in the municipality of Mažeikiai has the highest number of cases. Since 2005, the most frequent diagnosis has been Mechanical vibrations. In terms of occupational diseases by gender, males are the leading group in the period from 2014 to 2022. Next graph clearly shows the evolution of occupational diseases in the municipalities a decrease in the number of cases. This is likely to be influenced by the rapid development of technology and occupational safety requirements. The last graph shows a selection of municipalities where the number of occupational diseases is increasing in a linear regression, i.e. there is an upward trend in the number of cases over the period shown in the graph.
