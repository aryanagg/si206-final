import requests
import sqlite3

conn = sqlite3.connect('final_data.db')
cursor = conn.cursor()
# Create a new table for storing pollution data
cursor.execute('''
CREATE TABLE IF NOT EXISTS country_and_population (
                id INTEGER PRIMARY KEY,
                country TEXT NOT NULL,
                population INTEGER NOT NULL
            )
        ''')
cursor.execute('''
INSERT INTO country_and_population (id, country, population)
SELECT 
    Country.id,
    Country.name AS country,
    Population.population
FROM 
    Country
JOIN 
    Population ON Country.id = Population.id
''')
conn.commit()
conn.close()
