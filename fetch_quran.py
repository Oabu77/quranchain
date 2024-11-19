import requests
import json

BASE_URL = "https://api.quran.com/api/v4/verses/by_chapter/"
TRANSLATION_ID = 131

def fetch_quran():
    quran_data = []
    for chapter in range(1, 115):
        print(f"Fetching Surah {chapter}...")
        response = requests.get(f"{BASE_URL}{chapter}", params={"translations": TRANSLATION_ID})
        if response.status_code == 200:
            data = response.json()
            # Safely retrieve chapter_name or use a fallback
            surah_name = data["verses"][0].get("chapter_name", f"Surah {chapter}")
            surah_data = {
                "chapter": chapter,
                "name": surah_name,
                "verses": [
                    {
                        "arabic": verse.get("text_uthmani", ""),
                        "english": verse["translations"][0]["text"]
                    }
                    for verse in data["verses"]
                ],
            }
            quran_data.append(surah_data)
        else:
            print(f"Failed to fetch Surah {chapter}. Status code: {response.status_code}")
            break

    with open("full_quran_with_arabic.json", "w", encoding="utf-8") as file:
        json.dump(quran_data, file, ensure_ascii=False, indent=4)
    print("Quran text saved to full_quran_with_arabic.json.")

fetch_quran()
