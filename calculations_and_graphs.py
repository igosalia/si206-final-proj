"""Calculations using weather and racing data"""

import sqlite3

database_path = "weather_and_horse_race_data.db"

tracks = ["Arizona Downs", "Rillito Park", "Turf Paradise", "Oaklawn Park", "Sonoma County Fairgrounds", "Pleasanton", "Del Mar", "Fresno Race Track", "Los Alamitos", "Santa Anita Park", "Cal-Expo Race Track", "Humboldt County Fair", "Arapahoe Park", "Delaware Park", "Gulfstream Park", "Tampa Bay Downs", "Fairmount Park", "Hawthorne", "Horseshoe Indianapolis", "Prairie Meadows", "Churchill Downs", "Ellis Park", "Keeneland", "Kentucky Downs", "Turfway Park", "Delta Downs", "Evangeline Downs", "Fair Grounds", "Louisiana Downs", "Laurel Park", "Maryland State Fairgrounds", "Pimlico", "Canterbury Park", "Columbus Races", "Fonner Park", "Horsemen's Park", "Legacy Downs", "Meadowlands", "Monmouth Park", "Albuquerque Downs", "Ruidoso Downs", "Sunland Park", "SunRay Park", "Zia Park", "Aqueduct", "Belmont Park", "Finger Lakes Gaming and Race Track", "Saratoga", "North Dakota Horse Park", "Chippewa Downs", "Belterra Park", "Hollywood Gaming at Mahoning Valley", "Thistledown Racino", "Fair Meadows Race Track", "Remington Park", "Will Rogers Downs", "Grants Pass Downs", "Parx Casino and Racing", "Hollywood Casino at Penn National", "Presque Isle Downs", "Lone Star Park", "Retama Park", "Sam Houston Race Park", "Colonial Downs", "Emerald Downs", "Hollywood Casino at Charles Town Races", "Mountaineer Casino", "Wyoming Downs", "Sweetwater Downs", "Energy Downs"]
weather_tracks_map = {}

conn = sqlite3.connect(database_path)
cur = conn.cursor()

def main():
    calculate_avg_temps()

def calculate_avg_temps():
    average_temps_by_race_track = {}
    for track in tracks:
        sum = 0
        cur.execute("""
            SELECT temperature FROM weather
            WHERE track_name = ?
        """, (track,))
        temps = cur.fetchall()
        num_days = len(temps)
        if num_days > 0:
            temp_sum = 0
            for temp in temps:
                temp_sum += temp[0]
            average_temps_by_race_track[track] = temp_sum / num_days
        else:
            "Error getting data for this location"

        

def calculate_avg_humidity():
    #calculate average humidity at each major racing course in DB
    pass

def calculate_avg_windspeed():
    #calculate average windspeed at each major racing course in DB
    pass

def calculate_avg_visibility():
    #calculate average visibility at each major racing course in DB
    pass

def calculate_avg_race_pace():
    #calculate average race pace/times per mile at each racing course
    pass

def hypothesis_tests():
    #hypothesis tests and correlation coefficients for each independent variable (temperature, humidity, visibility, etc)
    pass

def temp_vs_pace():
    #create graph to compare temp and race pace/time
    pass

def windspeed_vs_pace():
    #create graph to compare windspeed and race pace/time
    pass

def tracktype_vs_pace():
    #create graph to compare track type to race pace
    pass

if __name__ == "__main__":
    main()