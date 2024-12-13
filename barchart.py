import requests
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

API_URL = "https://countryinfoapi.com/api/countries"

def setup_database():
    """
    Sets up the SQLite database and creates the required tables.
    """
    conn = sqlite3.connect("project_data.db")
    cursor = conn.cursor()

    #Creates tables
    cursor.execute("CREATE TABLE IF NOT EXISTS Country (id INTEGER PRIMARY KEY, name TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS Population (id INTEGER PRIMARY KEY, population INTEGER, FOREIGN KEY(id) REFERENCES Country(id))")
    cursor.execute("CREATE TABLE IF NOT EXISTS Pollution (id INTEGER PRIMARY KEY, pollution_level REAL, FOREIGN KEY(id) REFERENCES Country(id))")

    conn.commit()
    conn.close()

#Stores the data from Country Info API
def fetch_and_store_country_data():
    conn = sqlite3.connect("project_data.db")
    cursor = conn.cursor()

    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()

        for entry in data:
            country_id = int(entry["ccn3"]) if "ccn3" in entry and entry["ccn3"].isdigit() else None
            country_name = entry.get("name", None)
            population = entry.get("population", None)

            #insert data
            if country_id and country_name and population:
                cursor.execute("INSERT OR IGNORE INTO Country (id, name) VALUES (?, ?)", (country_id, country_name))
                cursor.execute("INSERT OR IGNORE INTO Population (id, population) VALUES (?, ?)", (country_id, population))
            else:
                print(f"Skipping invalid entry: {entry}")

    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch country data from API: {e}")
    
    conn.commit()
    conn.close()

#Populate Pollution Data (Static Data for Testing)
def populate_pollution_data():
    conn = sqlite3.connect("project_data.db")
    cursor = conn.cursor()

    #Example pollution data Country ID, Pollution Level
    pollution_data = [
        (586, 54.17),  # Bangladesh
        (356, 41.39),   # India
        (524, 39.18),   # United States
        (586, 38.90),   # Indonesia
        (108, 34.04),   # Pakistan
        (646, 33.37),   # South Africa
        (120, 32.58),   # Myanmar
        (368, 32.42),   # Kenya
        (68, 29.63),   # South Korea
        (104, 28.64),   # Colombia
    ]

    for country_id, pollution_level in pollution_data:
        cursor.execute("INSERT OR REPLACE INTO Pollution (id, pollution_level) VALUES (?, ?)", 
                       (country_id, pollution_level))

    conn.commit()
    conn.close()

#Create Bar Chart for Top 10 Most Polluted Countries
def create_pollution_bar_chart():
    """
    Creates a bar chart of the top 10 most polluted countries using Matplotlib.
    """
    conn = sqlite3.connect("project_data.db")
    
    # Query to fetch data
    query = """
        SELECT Country.name, Pollution.pollution_level
        FROM Pollution
        JOIN Country ON Pollution.id = Country.id
        ORDER BY Pollution.pollution_level DESC
        LIMIT 10
    """
    df = pd.read_sql_query(query, conn)
    conn.close()

    # Check if data exists
    if df.empty:
        print("No data available for visualization.")
        return

    # Create the bar chart
    plt.figure(figsize=(12, 8))
    plt.bar(df["name"], df["pollution_level"], color="skyblue")
    plt.xlabel("Country")
    plt.ylabel("Pollution Level (µg/m³)")
    plt.title("Top 10 Most Polluted Countries")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("top_10_polluted_countries.png")
    plt.show()

# Main Execution
if __name__ == "__main__":
    print("Setting up database...")
    setup_database()
    
    print("Fetching and storing country data...")
    fetch_and_store_country_data()
    
    print("Populating pollution data...")
    populate_pollution_data()
    
    print("Creating bar chart...")
    create_pollution_bar_chart()
