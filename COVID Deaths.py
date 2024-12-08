import requests
import sqlite3
import json

API_URL = "https://coronavirus.m.pipedream.net/"

def get_data():
    response = requests.get(API_URL)
    if response.status_code == 200:
        data = response.json()
        return data.get("rawData", [])
    
db_name="final_project_data.db"
def store_data(data):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    # Create table if it doesn't exist
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

    cursor.execute("SELECT latitude FROM covid_deaths")
    existing_lats = []
    for row in cursor.fetchall():
        existing_lats.append(str(row[0]))

    count = 0
    for line in data:
        #if count>=25:
        #   break
        if line.get("Lat")!= "" and line.get("Lat") not in existing_lats:
            cursor.execute("""
            INSERT INTO covid_deaths (latitude, longitude, province_state, country_region, confirmed, deaths)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (
                line.get("Lat"),
                line.get("Long_"),
                line.get("Province_State"),
                line.get("Country_Region"),
                int(line.get("Confirmed", 0)),
                int(line.get("Deaths", 0))
            ))
            count += 1

    connection.commit()
    connection.close()
    print(f"Inserted {count} new lines into the table.")

def main():
    data = get_data()
    if data:
        store_data(data)

if __name__ == "__main__":
    main()




