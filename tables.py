import requests
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt


def setup_database():
    """
    Sets up the SQLite database and creates the required tables.
    """
    conn = sqlite3.connect("project_data.db")
    cursor = conn.cursor()

    # Create Country and Population tables
    cursor.execute("CREATE TABLE IF NOT EXISTS Country (id INTEGER PRIMARY KEY, name TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS Population (id INTEGER PRIMARY KEY, population INTEGER, FOREIGN KEY(id) REFERENCES Country(id))")

    conn.commit()
    conn.close()


def fetch_and_store_country_data(limit=25, offset=0):
    """
    Fetches country data from the Country Info API and stores it in the SQLite database.
    Fetches only a limited number of rows at a time to meet project requirements.
    """
    conn = sqlite3.connect("project_data.db")
    cursor = conn.cursor()
    API_URL = "https://countryinfoapi.com/api/countries"

    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()

        # Limit data by offset and range
        for entry in data[offset:offset + limit]:
            # Extract relevant data
            country_id = int(entry["ccn3"]) if entry["ccn3"].isdigit() else None
            country_name = entry.get("name", None)
            population = entry.get("population", None)

            # Validate and insert data
            if country_id and country_name and population:
                cursor.execute("INSERT OR IGNORE INTO Country (id, name) VALUES (?, ?)", (country_id, country_name))
                cursor.execute("INSERT OR IGNORE INTO Population (id, population) VALUES (?, ?)", (country_id, population))
            else:
                print(f"Skipping invalid entry: {entry}")

    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch data: {e}")

    conn.commit()
    conn.close()


def fetch_incremental_data():
    """
    Fetches data incrementally (25 rows per run) and stores it in the database.
    Keeps track of the current offset across runs to allow progression from the last fetch.
    """
    setup_database()  # Ensure the database and tables are set up

    conn = sqlite3.connect("project_data.db")
    cursor = conn.cursor()

    # Create a table to track the current offset if it doesn't exist
    cursor.execute("CREATE TABLE IF NOT EXISTS FetchTracker (current_offset INTEGER)")

    # Get the current offset; start from 0 if no entry exists
    cursor.execute("SELECT current_offset FROM FetchTracker LIMIT 1")
    result = cursor.fetchone()
    current_offset = result[0] if result else 0

    # Set the limit for rows to fetch in each run
    limit = 25

    # Fetch data with the current offset
    fetch_and_store_country_data(limit=limit, offset=current_offset)

    # Print the newly added rows for this run
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT Country.id, Country.name, Population.population FROM Country JOIN Population ON Country.id = Population.id LIMIT ? OFFSET ?", (limit, current_offset))
    rows = cursor.fetchall()
    print("Fetched rows:")
    for row in rows:
        print(dict(row))

    # Update the offset in the database
    new_offset = current_offset + limit
    if result:
        cursor.execute("UPDATE FetchTracker SET current_offset = ?", (new_offset,))
    else:
        cursor.execute("INSERT INTO FetchTracker (current_offset) VALUES (?)", (new_offset,))

    conn.commit()
    conn.close()

    print(f"Fetched and stored rows {current_offset + 1} to {current_offset + limit}")


def visualize_population():
    """
    Creates a simple bar chart for the top 10 countries by population.
    """
    conn = sqlite3.connect("project_data.db")
    query = """
        SELECT Country.name, Population.population
        FROM Country
        JOIN Population ON Country.id = Population.id
        ORDER BY Population.population DESC
        LIMIT 10
    """
    df = pd.read_sql_query(query, conn)
    conn.close()

    if df.empty:
        print("No data available for visualization.")
        return

    plt.figure(figsize=(12, 8))
    plt.bar(df["name"], df["population"], color="skyblue")
    plt.xlabel("Country")
    plt.ylabel("Population")
    plt.title("Top 10 Countries by Population")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("top_10_populated_countries.png")
    plt.show()


if __name__ == "__main__":
    print("Fetching data incrementally...")
    fetch_incremental_data()

    print("\nVisualizing top 10 countries by population...")
    visualize_population()
