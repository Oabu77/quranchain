import requests
import json

def fetch_masjid_locations():
    """
    Fetch masjid (mosque) locations worldwide using Overpass API.
    """
    # Overpass API URL
    OVERPASS_API_URL = "https://overpass-api.de/api/interpreter"

    # Overpass Query: Fetch all places of worship tagged as Muslim
    overpass_query = """
    [out:json];
    node["amenity"="place_of_worship"]["religion"="muslim"];
    out body;
    """

    try:
        # Send the request to Overpass API
        print("Fetching masjid locations from Overpass API...")
        response = requests.get(OVERPASS_API_URL, params={"data": overpass_query})

        if response.status_code == 200:
            data = response.json()

            # Extract relevant information from the response
            masjids = []
            for element in data["elements"]:
                if "lat" in element and "lon" in element:
                    masjid_info = {
                        "name": element.get("tags", {}).get("name", "Unknown"),
                        "latitude": element["lat"],
                        "longitude": element["lon"],
                        "address": element.get("tags", {}).get("addr:full", "Unknown Address"),
                    }
                    masjids.append(masjid_info)

            print(f"Found {len(masjids)} masjid locations.")
            return masjids
        else:
            print(f"Failed to fetch data. HTTP Status Code: {response.status_code}")
            return []

    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def save_masjid_data_to_file(masjids, filename="masjid_locations.json"):
    """
    Save masjid location data to a JSON file.
    """
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(masjids, file, ensure_ascii=False, indent=4)
    print(f"Masjid data saved to {filename}.")

if __name__ == "__main__":
    # Fetch masjid locations
    masjid_locations = fetch_masjid_locations()

    # Save to file
    if masjid_locations:
        save_masjid_data_to_file(masjid_locations)
