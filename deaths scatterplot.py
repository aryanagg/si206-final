import sqlite3 
import pandas as pd
import matplotlib.pyplot as plt
import csv

def get_data(db_path, query):
    conn = sqlite3.connect(db_path)
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def write_to_csv(df, filepath):
    with open(filepath, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Country', 'Total Deaths']) 
        writer.writerows(df[['country', 'total_deaths']].values.tolist())

def create_scatter_plot(df):
    df_sorted = df.sort_values(by='pollution_2023')
    plt.figure(figsize=(20, 6))
    plt.scatter(df_sorted['pollution_2023'], df_sorted['total_deaths'], alpha=0.7, edgecolors='w', s=100)
    plt.title('Number of COVID Deaths vs Air Pollution Level Per Country', fontsize=14)
    plt.xlabel('Air Pollution Level', fontsize=12)
    plt.ylabel('Number of COVID Deaths', fontsize=12)
    plt.xticks(rotation=45, fontsize=6)
    plt.show()

def main():
    db_path = 'final_data.db'
    query = """
        SELECT covid_deaths.country_region AS country, 
               SUM(covid_deaths.deaths) AS total_deaths, 
               pollution_data.pollution_2023
        FROM covid_deaths
        JOIN pollution_data ON covid_deaths.country_region = pollution_data.country
        GROUP BY covid_deaths.country_region, pollution_data.pollution_2023;
    """
    
    df = get_data(db_path, query)
    write_to_csv(df, 'pollution_scatterplot_calculated_data.csv')
    create_scatter_plot(df)

if __name__ == "__main__":
    main()
