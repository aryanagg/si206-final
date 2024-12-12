import sqlite3
import requests
from bs4 import BeautifulSoup

# URL of the website
url = "https://en.wikipedia.org/wiki/List_of_countries_by_air_pollution"

# Send a GET request to the website
response = requests.get(url)

if response.status_code == 200:
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the table containing air pollution data
    table = soup.find('table', {'class': 'wikitable'})
    if table:
        rows = table.find_all('tr')[1:]  # Skip the header row
        data = []
        for row in rows:
            columns = row.find_all('td')
            if len(columns) >= 2:
                country = columns[1].text.strip()
                pollution = columns[2].text.strip()
                data.append((country, pollution))

        # Connect to the SQLite3 database
        conn = sqlite3.connect('final_data.db')
        cursor = conn.cursor()

        # Create a new table for storing pollution data
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pollution_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                country TEXT NOT NULL,
                pollution_2023 TEXT NOT NULL
            )
        ''')

        # Keep track of how many entries are already in the table
        cursor.execute('SELECT COUNT(*) FROM pollution_data')
        existing_count = cursor.fetchone()[0]

        # Insert only the next 25 entries into the table
        batch_size = 25
        start_index = existing_count
        end_index = start_index + batch_size
        batch = data[start_index:end_index]
        cursor.executemany('''
            INSERT INTO pollution_data (country, pollution_2023) 
            VALUES (?, ?)
        ''', batch)

        # Commit changes and close the connection
        conn.commit()
        conn.close()

        print(f"Added {len(batch)} entries to the database.")
    else:
        print("Error: Unable to find the table with pollution data on the webpage.")
else:
    print(f"Failed to fetch the webpage. Status code: {response.status_code}")
