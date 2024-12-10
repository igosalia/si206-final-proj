import requests
from bs4 import BeautifulSoup
import sqlite3
import re

#weather API uses state abbreviations, matched here for consistency
state_abbreviations = {
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Delaware": "DE",
    "Florida": "FL",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maryland": "MD",
    "Minnesota": "MN",
    "Nebraska": "NE",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Texas": "TX",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wyoming": "WY"
}

def scrape_wikipedia(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    active_us_venues = []
    us_venues = soup.find('h2', id='United_States') #locate only active venues in US#

    #go to next element in thoroughbred section
    next_element = us_venues.find_next()
    while next_element and ('Harness racing' not in next_element.text):
        if next_element.name == 'h2':
            break
        if next_element.name == 'h4':
            state = next_element.get_text()
            print(f"Found state: {state}")
        if next_element.name == 'ul':
            for li in next_element.find_all('li'):
                pattern = r'\([^)]*\)|\[.*\]'
                venue = li.get_text()
                venue = re.sub(pattern, '', venue).split(", ")
                if len(venue) >= 2:
                    venue_name = venue[0]
                    venue_city = venue[-1]
                    print(f"Found venue: {venue_name}, {venue_city}")
                    active_us_venues.append(f"{venue_name}, {venue_city}, {state}")
        next_element = next_element.find_next()
    
    return active_us_venues
    """    print(next_element)
        if next_element.get('class') == ['mw-heading mw-heading4']:
            state = next_element.find('h4').get_text(strip=True)
            state_abbreviated = state_abbreviations.get(state, '')
            print(state_abbreviated)
            next_ul = next_element.find_next('ul')
            if next_ul:
                for li in next_ul.find_all('li'):
                    venue = li.get_text(strip=True)
                    venue_info = venue.split(', ')
                    
                    #venue name and city
                    venue_name = venue_info[0]
                    venue_city = venue_info[-1]
                    full_venue_name = f"{venue_name, venue_city, state_abbreviated}"
                    active_us_venues.append(full_venue_name)     
        next_element = next_element.find_next()
    return active_us_venues
    """

url = "https://en.wikipedia.org/wiki/List_of_horse_racing_venues"
venues = scrape_wikipedia(url)
for venue in venues:
    print(venue)
