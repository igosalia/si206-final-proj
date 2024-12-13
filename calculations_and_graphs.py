"""Calculations using weather and racing data"""

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as py

database_path = "weather_and_horse_race_data.db"

def load_data_from_db():
    conn = sqlite3.connect(database_path)

    #joining race_card, horse_info, and weather
    query = """
        SELECT rc.course, rc.date, hi.horse_name, hi.horse_age, hi.horse_weight,
        hi.horse_rating, w.temperature, w.humidity, w.windspeed, w.visibility
        FROM race_cards rc
        JOIN horse_info hi ON rc.raceid = hi.raceid
        JOIN weather w ON rc.course = w.track_name AND rc.date = w.date
    """

    data = pd.read_sql_query(query, conn)
    conn.close()
    return data

def calculate_weather_info(data):
    #group by track and calculate mean for each weather attr
    weather_stats = data.groupby('course')[['temperature', 'humidity', 'windspeed', 'visibility']].mean()
    #add header to weather dataframe
    weather_stats.rename(columns={
        'temperature': 'average_temp',
        'humidity' : 'average_humidity',
        'windspeed' : 'average_windspeed',
        'visibility' : 'average_visibility'
    }, inplace=True)

    return weather_stats


tracks = ["Bangor-on-Dee", "Cheltenham", "Doncaster", "Southwell (AW)", "Cork", "Dundalk (AW)", "Meydan", "San Isidro", "Eagle Farm", "Deauville", "Newcastle", "Wolverhampton (AW)", "Fairyhouse"]
weather_tracks_map = {}

conn = sqlite3.connect(database_path)
cur = conn.cursor()

def main():
    #load data
    data = load_data_from_db()
    print(data.head())

    #weather calculations
    weather_stats = calculate_weather_info(data)
    print(weather_stats)

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