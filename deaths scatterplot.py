import sqlite3 
import pandas as pd
import matplotlib.pyplot as plt
import csv

conn = sqlite3.connect('final_data.db')  

query = """
    SELECT covid_deaths.country_region AS country, 
           SUM(covid_deaths.deaths) AS total_deaths, 
           pollution_data.pollution_2023
    FROM covid_deaths
    JOIN pollution_data ON covid_deaths.country_region = pollution_data.country
    GROUP BY covid_deaths.country_region, pollution_data.pollution_2023;
"""

df = pd.read_sql(query, conn)

conn.close()

with open('pollution_scatterplot_calculated_data.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Country', 'Total Count of COVID Deaths']) 
    writer.writerows(df[['country', 'total_deaths']].values.tolist()) 

df_sorted = df.sort_values(by='pollution_2023')
plt.figure(figsize=(20, 6))
plt.scatter(df_sorted['pollution_2023'], df_sorted['total_deaths'], alpha=0.7, edgecolors='w', s=100)

plt.title('Number of COVID Deaths vs Air Pollution Level Per Country', fontsize=14)
plt.xlabel('Air Pollution Level', fontsize=12)
plt.ylabel('Number of COVID Deaths', fontsize=12)
plt.xticks(rotation=45, fontsize=6)
plt.savefig("covid_deaths_vs_pollution.png")
plt.show()