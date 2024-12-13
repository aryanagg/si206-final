import requests
import pandas as pd
import matplotlib.pyplot as plt

API_URL = "https://countryinfoapi.com/api/countries"

# Fetches country data from the API and stores it in memory
def fetch_country_data():
    """
    Fetches data from the API and returns it as a DataFrame.
    """
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()

        # Extract relevant data
        country_data = [
            {
                "id": int(entry["ccn3"]) if "ccn3" in entry and entry["ccn3"].isdigit() else None,
                "name": entry.get("name", None),
                "population": entry.get("population", None)
            }
            for entry in data
        ]

        # Filter out invalid entries
        country_data = [
            entry for entry in country_data
            if entry["id"] is not None and entry["name"] and entry["population"] is not None
        ]

        return pd.DataFrame(country_data)
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch country data from API: {e}")
        return pd.DataFrame()

# Adds static pollution data to the DataFrame
def add_pollution_data(country_df):
    """
    Adds pollution data to the DataFrame based on country ID.
    """
    pollution_data = {
        586: 54.17,  # Pakistan
        356: 41.39,  # India
        524: 39.18,  # Nepal
        586: 38.90,  # Pakistan (update)
        108: 34.04,  # Burundi
        646: 33.37,  # Rwanda
        120: 32.58,  # Cameroon
        368: 32.42,  # Iraq
        68: 29.63,   # Bolivia
        104: 28.64   # Myanmar
    }

    # Map pollution data to country DataFrame
    pollution_df = pd.DataFrame(list(pollution_data.items()), columns=["id", "pollution_level"])
    return pd.merge(country_df, pollution_df, on="id", how="inner")

# Create Bar Chart for Top 10 Most Polluted Countries
def create_pollution_bar_chart(pollution_df):
    """
    Creates a bar chart of the top 10 most polluted countries using Matplotlib.
    """
    # Sort by pollution level and select top 10
    top_polluted = pollution_df.sort_values(by="pollution_level", ascending=False).head(10)

    # Check if data exists
    if top_polluted.empty:
        print("No data available for visualization.")
        return

    # Create the bar chart
    plt.figure(figsize=(12, 8))
    plt.bar(top_polluted["name"], top_polluted["pollution_level"], color="skyblue")
    plt.xlabel("Country")
    plt.ylabel("Pollution Level (µg/m³)")
    plt.title("Top 10 Most Polluted Countries")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("top_10_polluted_countries.png")
    plt.show()

# Main Execution
if __name__ == "__main__":
    print("Fetching country data...")
    country_df = fetch_country_data()

    if not country_df.empty:
        print("Adding pollution data...")
        pollution_df = add_pollution_data(country_df)

        print("Creating bar chart...")
        create_pollution_bar_chart(pollution_df)
    else:
        print("No country data available.")