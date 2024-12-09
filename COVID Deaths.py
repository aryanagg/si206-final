import requests
import sqlite3
import json

API_URL = "https://coronavirus.m.pipedream.net/"

def get_data():
    response = requests.get(API_URL)
    if response.status_code == 200:
        data = response.json()
        return data.get("rawData", [])
    
db_name="final_data.db"

def get_current_row_count(cursor):
    cursor.execute("SELECT COUNT(*) FROM covid_deaths")
    return cursor.fetchone()[0]

def insert_rows(data, chunk_size=25):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    # Create the table if it doesn't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS covid_deaths (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        latitude FLOAT,
        longitude FLOAT,
        province_state TEXT,
        country_region TEXT,
        confirmed INTEGER,
        deaths INTEGER
    )
    """)

    # Get the current number of rows in the table
    current_count = get_current_row_count(cursor)

    # Insert data based on current count
    if current_count < 100:
        # Insert rows in chunks of 25 until 100 rows are reached
        start_index = current_count
        end_index = min(start_index + chunk_size, len(data), 100)
        for record in data[start_index:end_index]:
            cursor.execute("""
            INSERT INTO covid_deaths (latitude, longitude, province_state, country_region, confirmed, deaths)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (
                record.get("Lat"),
                record.get("Long_"),
                record.get("Province_State"),
                record.get("Country_Region"),
                int(record.get("Confirmed", 0)),
                int(record.get("Deaths", 0)),
            ))
        rows_inserted = end_index - start_index
        print(f"Inserted {rows_inserted} rows (from row {start_index} to {end_index - 1}).")
    else:
        # Once 100 rows are reached, insert all remaining rows at once
        remaining_data = data[current_count:]
        for record in remaining_data:
            cursor.execute("""
            INSERT INTO covid_deaths (latitude, longitude, province_state, country_region, confirmed, deaths)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (
                record.get("Lat"),
                record.get("Long_"),
                record.get("Province_State"),
                record.get("Country_Region"),
                int(record.get("Confirmed", 0)),
                int(record.get("Deaths", 0)),
            ))
        print(f"Inserted all remaining {len(remaining_data)} rows after reaching 100 rows.")

    # Commit changes
    connection.commit()
    connection.close()


def main():
    data = get_data()
    if data:
        insert_rows(data)

if __name__ == "__main__":
    main()




