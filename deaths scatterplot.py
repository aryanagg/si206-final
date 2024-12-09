import sqlite3  # or another DB connector like psycopg2 for PostgreSQL
import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Establish a database connection (adjust as per your DB)
conn = sqlite3.connect('final_data.db')  # Change to your DB connection string

# Step 2: Query the data, aggregate deaths by country and join with pollution data
query = """
    SELECT covid_deaths.country_region AS country, 
           SUM(covid_deaths.deaths) AS total_deaths, 
           pollution_data.pollution_2023
    FROM covid_deaths
    JOIN pollution_data ON covid_deaths.country_region = pollution_data.country
    GROUP BY covid_deaths.country_region, pollution_data.pollution_2023;
"""

# Step 3: Execute query and load data into a pandas DataFrame
df = pd.read_sql(query, conn)

# Step 4: Close the connection
conn.close()

# Step 5: Create a scatter plot
df_sorted = df.sort_values(by='pollution_2023')
plt.figure(figsize=(20, 6))
plt.scatter(df_sorted['pollution_2023'], df_sorted['total_deaths'], alpha=0.7, edgecolors='w', s=100)

# Step 6: Customize the plot
plt.title('Number of COVID Deaths vs Air Pollution Level Per Country', fontsize=14)
plt.xlabel('Air Pollution Level', fontsize=12)
plt.ylabel('Number of COVID Deaths', fontsize=12)
plt.xticks(rotation=45, fontsize=6)
plt.show()