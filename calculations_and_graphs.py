"""Calculations using weather and racing data"""

import sqlite3

database_path = "weather_and_horse_race_data.db"

tracks = ["Arizona Downs", "Rillito Park", "Turf Paradise", "Oaklawn Park", "Sonoma County Fairgrounds", "Pleasanton", "Del Mar", "Fresno Race Track", "Los Alamitos", "Santa Anita Park", "Cal-Expo Race Track", "Humboldt County Fair", "Arapahoe Park", "Delaware Park", "Gulfstream Park", "Tampa Bay Downs", "Fairmount Park", "Hawthorne", "Horseshoe Indianapolis", "Prairie Meadows", "Churchill Downs", "Ellis Park", "Keeneland", "Kentucky Downs", "Turfway Park", "Delta Downs", "Evangeline Downs", "Fair Grounds", "Louisiana Downs", "Laurel Park", "Maryland State Fairgrounds", "Pimlico", "Canterbury Park", "Columbus Races", "Fonner Park", "Horsemen's Park", "Legacy Downs", "Meadowlands", "Monmouth Park", "Albuquerque Downs", "Ruidoso Downs", "Sunland Park", "SunRay Park", "Zia Park", "Aqueduct", "Belmont Park", "Finger Lakes Gaming and Race Track", "Saratoga", "North Dakota Horse Park", "Chippewa Downs", "Belterra Park", "Hollywood Gaming at Mahoning Valley", "Thistledown Racino", "Fair Meadows Race Track", "Remington Park", "Will Rogers Downs", "Grants Pass Downs", "Parx Casino and Racing", "Hollywood Casino at Penn National", "Presque Isle Downs", "Lone Star Park", "Retama Park", "Sam Houston Race Park", "Colonial Downs", "Emerald Downs", "Hollywood Casino at Charles Town Races", "Mountaineer Casino", "Wyoming Downs", "Sweetwater Downs", "Energy Downs"]
weather_tracks_map = {}

conn = sqlite3.connect(database_path)
cur = conn.cursor()

def main():
    #weather calculations
    calculate_avg_temps()
    calculate_avg_humidity()
    calculate_avg_windspeed()
    calculate_avg_visibility

def calculate_avg_temps():
    for track in tracks:
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
            weather_tracks_map[track] = {}
            weather_tracks_map[track]["average_temp"] = temp_sum / num_days

        else:
            "Error getting data for this location"
    

def calculate_avg_humidity():
    #calculate average humidity at each major racing course in DB
    for track in tracks:
        cur.execute("""
            SELECT humidity FROM weather
            WHERE track_name = ?
        """, (track,))
        values = cur.fetchall()
        num_days = len(values)
        if num_days > 0:
            hum_sum = 0
            for val in values:
                hum_sum += val[0]
            weather_tracks_map[track] = {}
            weather_tracks_map[track]["average_humidity"] = hum_sum / num_days

        else:
            "Error getting data for this location"

def calculate_avg_windspeed():
    #calculate average windspeed at each major racing course in DB
    for track in tracks:
        cur.execute("""
            SELECT windspeed FROM weather
            WHERE track_name = ?
        """, (track,))
        values = cur.fetchall()
        num_days = len(values)
        if num_days > 0:
            wind_sum = 0
            for val in values:
                wind_sum += val[0]
            weather_tracks_map[track] = {}
            weather_tracks_map[track]["average_windspeed"] = wind_sum / num_days

        else:
            "Error getting data for this location"

def calculate_avg_visibility():
    #calculate average visibility at each major racing course in DB
    for track in tracks:
        cur.execute("""
            SELECT visibility FROM weather
            WHERE track_name = ?
        """, (track,))
        values = cur.fetchall()
        num_days = len(values)
        if num_days > 0:
            vis_sum = 0
            for val in values:
                vis_sum += val[0]
            weather_tracks_map[track]["average_windspeed"] = vis_sum / num_days
        else:
            "Error getting data for this location"

#TODO: Database Join calculation, more calculations and graphs

if __name__ == "__main__":
    main()