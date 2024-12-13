import requests
from bs4 import BeautifulSoup
import sqlite3
import re

def scrape_wikipedia(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    active_gb_venues = []
    gb_venues = soup.find('h2', id='Great_Britain') #locate only active venues in GB#

    #go to next element in thoroughbred section
    next_element = gb_venues.find_next()
    while next_element:
        if next_element.name == 'h2':
            break
        if next_element.name == 'h3':
            area = next_element.get_text()
        if next_element.name == 'ul':
            for li in next_element.find_all('li'):
                pattern = r'\([^)]*\)|\[.*\]|Racetrack|Race.Course|Racecourse'
                venue = li.get_text()
                if "flat" in venue.split(',')[-1].lower():
                    venue = ','.join(venue.split(',')[:-1]).strip()
                venue = re.sub(pattern, '', venue).split(", ")
                if len(venue) >= 2 and len(venue) < 3:
                    venue_name = venue[0]
                    venue_city = venue[-1]
                    active_gb_venues.append(f"{venue_name}, {venue_city}, {area}, GB")
                elif len(venue) == 3:
                    print(venue)
                    venue_name = venue[0]
                    venue_city = venue[1]
                    active_gb_venues.append(f"{venue_name}, {venue_city}, {area}, GB")
        next_element = next_element.find_next()
    
    return active_gb_venues

url = "https://en.wikipedia.org/wiki/List_of_horse_racing_venues"
venues = scrape_wikipedia(url)
print(len(venues))
for venue in venues:
    print(venue)
