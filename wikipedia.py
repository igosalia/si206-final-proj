import requests
from bs4 import BeautifulSoup
import sqlite3

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
    us_thoroughbred = us_venues.find_next('h3', id='Thoroughbred_racing_3')
    print(us_venues, us_thoroughbred)

    #go to next element in thoroughbred section
    next_element = us_thoroughbred.find_next_sibling()
    while next_element and next_element.name != 'h3':
        if next_element.name == 'h4':
            state = next_element.get_text()
        if next_element.name == 'ul':
            for li in next_element.find_all('li'):
                venue = li.get_text()
                active_us_venues.append(f"{venue}, {state}")
        next_element = next_element.find_next_sibling()
    
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
