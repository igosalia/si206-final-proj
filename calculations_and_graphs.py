"""Calculations using weather and racing data"""

import sqlite3

database_path = "weather_and_horse_race_data.db"

track_names = ["Aqueduct", "Churchill Downs", "Fair Grounds", "Del Mar", "Gulfstream Park", "Oaklawn Park", "Tampa Bay Downs"]
weather_tracks_map = {}

conn = sqlite3.connect(database_path)
cur = conn.cursor()

def main():
    calculate_avg_temps()

def calculate_avg_temps():
    pass

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