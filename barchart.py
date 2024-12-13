import sqlite3 
import pandas as pd
import matplotlib.pyplot as plt
import csv

def get_data(db, query):
    conn = sqlite3.connect(db)
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Create Bar Chart for Top 10 Most Polluted Countries
def create_pollution_bar_chart(df):
    plt.figure(figsize=(12, 8))
    plt.bar(df['country'], df['pollution_2023'], color="green")
    plt.xlabel("Country")
    plt.ylabel("Air Pollution Level (µg/m³)")
    plt.title("Top 10 Most Polluted Countries")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("top_10_polluted_countries.png")
    plt.show()

def main():
    db = 'final_data.db'
    query = """
        SELECT country, pollution_2023
        FROM pollution_data
        ORDER BY pollution_2023 DESC
        LIMIT 10;
    """
    
    df = get_data(db, query)
    create_pollution_bar_chart(df)

# Main Execution
if __name__ == "__main__":
    main()