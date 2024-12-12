import sqlite3 
import pandas as pd
import matplotlib.pyplot as plt
import csv

def get_data(db, query):
    conn = sqlite3.connect(db)
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def write_to_csv(df, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Country', 'Total Number of COVID Deaths', 'Population']) 
        writer.writerows(df[['country', 'total_deaths', 'population']].values.tolist())

def create_scatter_plot(df):
    df_sorted = df.sort_values(by='population')
    fig, ax = plt.subplots(figsize=(20, 6))
    plt.scatter(df_sorted['population'], df_sorted['total_deaths'], alpha=0.7, edgecolors='w', s=100, marker='*')
    ax.set(title = 'Number of COVID Deaths vs Country Population',
           xlabel = 'Population',
           ylabel = 'Number of COVID Deaths')
    plt.xticks(rotation=45, fontsize=6)
    plt.savefig("covid_deaths_vs_population.png")
    plt.show()

def main():
    db = 'final_data.db'
    query = """
        SELECT covid_deaths.country_region AS country, 
               SUM(covid_deaths.deaths) AS total_deaths, 
               country_and_population.population
        FROM covid_deaths
        JOIN country_and_population ON covid_deaths.country_region = country_and_population.country
        GROUP BY covid_deaths.country_region;
    """
    
    df = get_data(db, query)
    write_to_csv(df, 'covid_deaths_pop.csv')
    create_scatter_plot(df)

if __name__ == "__main__":
    main()
