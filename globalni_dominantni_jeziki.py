import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import time
import re

# ==============================================================================
# 1. PODATKI: SEZNAM DRŽAV IN PRVI URADNI/DOMINANTNI JEZIK
# ==============================================================================

GLOBALNI_JEZIKI = {
    "Afghanistan": "Pashto, Northern", "Albania": "Albanian, Tosk", "Algeria": "Arabic, Standard",
    "Andorra": "Catalan-Valencian-Balear", "Angola": "Portuguese Portugal", "Antigua and Barbuda": "English",
    "Argentina": "Spanish", "Armenia": "Armenian", "Australia": "English", "Austria": "German, Standard",
    "Azerbaijan": "Azerbaijani, North Latin", "Bahamas": "English", "Bahrain": "Arabic, Standard",
    "Bangladesh": "Bengali", "Barbados": "English", "Belarus": "Belarusan", "Belgium": "French",
    "Belize": "English", "Benin": "French", "Bhutan": "Dzongkha", "Bolivia": "Spanish",
    "Bosnia and Herzegovina": "Bosnian Latin", "Botswana": "English", "Brazil": "Portuguese Brazil",
    "Brunei": "Malay Latin", "Bulgaria": "Bulgarian", "Burkina Faso": "French", "Burundi": "Rwanda",
    "Cambodia": "Khmer, Central", "Cameroon": "French", "Canada": "English", "Cape Verde": "Portuguese Portugal",
    "Central African Republic": "French", "Chad": "Arabic, Standard", "Chile": "Spanish",
    "China": "Chinese, Mandarin Simplified", "Colombia": "Spanish", "Comoros": "French",
    "Congo (Brazzaville)": "French", "Congo (Kinshasa)": "Lingala", "Costa Rica": "Spanish",
    "Cote d'Ivoire": "French", "Croatia": "Croatian", "Cuba": "Spanish", "Cyprus": "Greek monotonic",
    "Czech Republic": "Czech", "Denmark": "Danish", "Djibouti": "French", "Dominica": "English",
    "Dominican Republic": "Spanish", "Ecuador": "Spanish", "Egypt": "Arabic, Standard",
    "El Salvador": "Spanish", "Equatorial Guinea": "Spanish", "Eritrea": "Tigrigna",
    "Estonia": "Estonian", "Eswatini": "English", "Ethiopia": "Amharic", "Fiji": "Fijian",
    "Finland": "Finnish", "France": "French", "Gabon": "French", "Gambia": "English",
    "Georgia": "Georgian", "Germany": "German, Standard", "Ghana": "English", "Greece": "Greek monotonic",
    "Grenada": "English", "Guatemala": "Spanish", "Guinea": "French", "Guinea-Bissau": "Portuguese Portugal",
    "Guyana": "English", "Haiti": "Haitian Creole French Kreyol", "Honduras": "Spanish",
    "Hungary": "Hungarian", "Iceland": "Icelandic", "India": "Hindi", "Indonesia": "Indonesian",
    "Iran": "Farsi, Western", "Iraq": "Arabic, Standard", "Ireland": "Gaelic, Irish", "Israel": "Hebrew",
    "Italy": "Italian", "Jamaica": "English", "Japan": "Japanese", "Jordan": "Arabic, Standard",
    "Kazakhstan": "Kazakh", "Kenya": "Swahili", "Kiribati": "English", "Kosovo": "Albanian, Tosk",
    "Kuwait": "Arabic, Standard", "Kyrgyzstan": "Kirghiz", "Laos": "Lao", "Latvia": "Latvian",
    "Lebanon": "Arabic, Standard", "Lesotho": "English", "Liberia": "English", "Libya": "Arabic, Standard",
    "Liechtenstein": "German, Standard", "Lithuania": "Lithuanian", "Luxembourg": "French",
    "Madagascar": "Malagasy, Plateau", "Malawi": "English", "Malaysia": "Malay Latin",
    "Maldives": "Maldivian", "Mali": "French", "Malta": "Maltese", "Marshall Islands": "English",
    "Mauritania": "Arabic, Standard", "Mauritius": "English", "Mexico": "Spanish", "Micronesia": "English",
    "Moldova": "Romanian", "Monaco": "French", "Mongolia": "Mongolian, Halh Cyrillic", "Montenegro": "Serbian Latin",
    "Morocco": "Tamazight, Standard Morocan", "Mozambique": "Portuguese Portugal", "Myanmar": "Burmese",
    "Namibia": "English", "Nauru": "English", "Nepal": "Nepali", "Netherlands": "Dutch",
    "New Zealand": "English", "Nicaragua": "Spanish", "Niger": "French", "Nigeria": "English",
    "North Korea": "Korean", "North Macedonia": "Macedonian", "Norway": "Norwegian, Bokma╠Ől", "Oman": "Arabic, Standard",
    "Pakistan": "Urdu", "Palau": "Palauan", "Palestine": "Arabic, Standard", "Panama": "Spanish",
    "Papua New Guinea": "English", "Paraguay": "Guarani╠ü, Paraguayan", "Peru": "Spanish",
    "Philippines": "Tagalog", "Poland": "Polish", "Portugal": "Portuguese Portugal", "Qatar": "Arabic, Standard",
    "Romania": "Romanian", "Russia": "Russian", "Rwanda": "Rwanda", "Saint Kitts and Nevis": "English",
    "Saint Lucia": "English", "Saint Vincent and the Grenadines": "English", "Samoa": "Samoan",
    "San Marino": "Italian", "Sao Tome and Principe": "Portuguese Portugal", "Saudi Arabia": "Arabic, Standard",
    "Senegal": "French", "Serbia": "Serbian Latin", "Seychelles": "French", "Sierra Leone": "English",
    "Singapore": "English", "Slovakia": "Slovak", "Slovenia": "Slovenian", "Solomon Islands": "English",
    "Somalia": "Somali", "South Africa": "English", "South Korea": "Korean", "South Sudan": "English",
    "Spain": "Spanish", "Sri Lanka": "Sinhala", "Sudan": "Arabic, Standard", "Suriname": "Dutch",
    "Sweden": "Swedish", "Switzerland": "German, Standard", "Syria": "Arabic, Standard",
    "Taiwan": "Chinese, Mandarin Traditional", "Tajikistan": "Tajiki", "Tanzania": "Swahili",
    "Thailand": "Thai", "Timor-Leste": "Portuguese Portugal", "Togo": "French", "Tonga": "Tongan",
    "Trinidad and Tobago": "English", "Tunisia": "Arabic, Standard", "Turkey": "Turkish",
    "Turkmenistan": "Turkmen Latin", "Tuvalu": "English", "Uganda": "English", "Ukraine": "Ukrainian",
    "United Arab Emirates": "Arabic, Standard", "United Kingdom": "English", "United States": "English",
    "Uruguay": "Spanish", "Uzbekistan": "Uzbek, Northern Latin", "Vanuatu": "French",
    "Vatican City": "Latin", "Venezuela": "Spanish", "Vietnam": "Vietnamese", "Yemen": "Arabic, Standard",
    "Zambia": "English", "Zimbabwe": "Shona"
}

# ==============================================================================
# 2. DODATNI PODATKI: GOVORCI V MILIJONIH
# Ocene na podlagi Ethnologue in drugih demografskih virov.
# ==============================================================================

GOVORCEV_MIL = {
    "English": 1500, "Chinese, Mandarin Simplified": 1100, "Spanish": 550, "Hindi": 615, 
    "French": 280, "Arabic, Standard": 370, "Russian": 258, "Portuguese Portugal": 250, 
    "Portuguese Brazil": 250, "Indonesian": 199, "Japanese": 128, "German, Standard": 132, 
    "Urdu": 230, "Italian": 67, "Korean": 82, "Vietnamese": 96, "Turkish": 88, 
    "Polish": 40, "Dutch": 28, "Swedish": 10, "Finnish": 6, "Slovak": 5.5, 
    "Slovenian": 2.5, "Croatian": 5.5, "Bulgarian": 9, "Czech": 10.7, "Hungarian": 13, 
    "Romanian": 24, "Greek monotonic": 13, "Bengali": 265, "Thai": 69, "Swahili": 98, 
    "Zulu": 12, "Afrikaans": 18, "Nepali": 35, "Hebrew": 9.5, "Yoruba": 50, 
    "Hausa": 150, "Ukrainian": 45, "Tagalog": 106, "Malay Latin": 290, 
    "Catalan-Valencian-Balear": 10.5, "Bosnian Latin": 2.2, "Albanian, Tosk": 3.5, 
    "Belarusan": 10, "Armenian": 6.7, "Georgian": 3.7, "Kazakh": 17, "Latvian": 1.7, 
    "Lithuanian": 3.2, "Macedonian": 2.2, "Somali": 21, "Shona": 10.8, 
    "Pashto, Northern": 60, "Dzongkha": 0.16, "Kirghiz": 6.5, "Lao": 30, 
    "Malagasy, Plateau": 25, "Maldivian": 0.4, "Maltese": 0.5, "Palauan": 0.015,
    "Guarani╠ü, Paraguayan": 7.0, "Samoan": 0.5, "Serbian Latin": 8.5, "Sinhala": 16.5, 
    "Tigrigna": 10.5, "Tongan": 0.2, "Turkmen Latin": 7.2, "Uzbek, Northern Latin": 34.0, 
    "Haitian Creole French Kreyol": 12.0, "Chinese, Mandarin Traditional": 10, "Latin": 0.01,
    "Tamazight, Standard Morocan": 14.0, "Urdu": 230, "Burmese": 43, "Khmer, Central": 16,
    "Amharic": 32, "Rwanda": 13, "Haitian Creole French Kreyol": 12
}


# ==============================================================================
# 3. FUNKCIJE: GEOKODIRANJE IN ZBIRANJE PODATKOV
# ==============================================================================

def pridobi_koordinate(drzava, geolocator):
    """ Pridobi koordinate za ime države. """
    query = f"{drzava}"
    try:
        location = geolocator.geocode(query, timeout=20)
        if location:
            return location.latitude, location.longitude
    except (GeocoderTimedOut, GeocoderServiceError):
        pass
    except Exception:
        pass
    return None, None


def ustvari_globalno_tabelo(globalni_jeziki, govorcev_mil):
    geolocator = Nominatim(user_agent="Jezikoslovni_Projekt_GLOBAL", timeout=20)
    rezultati = []
    
    drzave = sorted(list(globalni_jeziki.keys()))
    print(f"Začenjam geokodiranje za {len(drzave)} držav...")
    
    for i, drzava in enumerate(drzave):
        dominantni_jezik = globalni_jeziki[drzava]
        
        # Pridobivanje števila govorcev
        st_govorcev_mil = govorcev_mil.get(dominantni_jezik, 1.0)
        
        # Časovni Zamik
        if i % 20 == 0 and i > 0:
            print(f"--- Premor 45 sekund ({i}/{len(drzave)}) ---")
            time.sleep(45)
            
        latitude, longitude = pridobi_koordinate(drzava, geolocator)
        
        if latitude is not None:
            print(f"  > OK ({i+1}/{len(drzave)}): {drzava} -> {dominantni_jezik} ({st_govorcev_mil}M) -> {latitude:.4f}, {longitude:.4f}")
        else:
            print(f"  > Napaka ({i+1}/{len(drzave)}): Lokacija ni najdena za '{drzava}'.")
            
        rezultati.append({
            "Drzava": drzava,
            "Dominantni_Jezik": dominantni_jezik,
            "Govorci_Milijoni": st_govorcev_mil, 
            "latitude": latitude,
            "longitude": longitude

        })
        time.sleep(2.5)
        
    return pd.DataFrame(rezultati)


# ==============================================================================
# 4. IZVAJANJE
# ==============================================================================

if __name__ == "__main__":
    
    IME_IZHODNE_DATOTEKE = "globalni_dominantni_jeziki_z_govorci2.csv"
    
    df_drzave = ustvari_globalno_tabelo(GLOBALNI_JEZIKI, GOVORCEV_MIL)

    # Shranjevanje končne datoteke
    df_drzave.to_csv(IME_IZHODNE_DATOTEKE, index=False, sep=';', encoding='utf-8')

    print("\n" + "=" * 65)
    print(f"PODATKI SHRANJENI. Datoteka: {IME_IZHODNE_DATOTEKE}")

    print("=" * 65)
