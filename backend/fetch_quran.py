import requests
import json

# Base URL for fetching Quran chapters and verses
BASE_URL = "https://api.quran.com/api/v4/"
TRANSLATION_ID = 131  # Sahih International Translation

def fetch_surah_names():
    """
    Fetch all surah names from the Quran.com API.
    """
    print("Fetching surah names...")
    response = requests.get(f"{BASE_URL}chapters")
    
    if response.status_code == 200:
        data = response.json()
        surah_names = {surah["id"]: surah["name_simple"] for surah in data.get("chapters", [])}
        return surah_names
    else:
        print(f"Failed to fetch surah names. HTTP Status: {response.status_code}")
        return {}

def fetch_quran_data():
    """
    Fetch Quran data with Arabic and English translations and save it to a JSON file.
    """
    quran = []
    surah_names = fetch_surah_names()

    for chapter in range(1, 115):  # Loop through all 114 surahs
        print(f"Fetching Surah {chapter}...")
        response = requests.get(f"{BASE_URL}verses/by_chapter/{chapter}", 
                                params={"translations": TRANSLATION_ID, "fields": "text_uthmani"})
        
        # Check if the request is successful
        if response.status_code == 200:
            data = response.json()
            verses = data.get("verses", [])

            # Process each surah
            surah_data = {
                "chapter": chapter,
                "name": surah_names.get(chapter, f"Surah {chapter}"),
                "verses": [
                    {
                        "arabic": verse.get("text_uthmani", "N/A"),
                        "english": (
                            verse.get("translations", [{}])[0].get("text", "Translation unavailable")
                        )
                    }
                    for verse in verses
                ]
            }
            quran.append(surah_data)
        else:
            print(f"Failed to fetch Surah {chapter}. HTTP Status: {response.status_code}")
            break

    # Save Quran data to JSON file
    with open("full_quran_with_arabic.json", "w", encoding="utf-8") as file:
        json.dump(quran, file, ensure_ascii=False, indent=4)
    print("Quran data successfully saved to 'full_quran_with_arabic.json'.")

if __name__ == "__main__":
    # Fetch and save the Quran data
    fetch_quran_data()
