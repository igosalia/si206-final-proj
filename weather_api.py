import sqlite3
import requests

database_path = "weather_and_horse_race_data.db"

def get_weather_data():
    conn = sqlite3.connect(database_path)
    cur = conn.cursor()

    #get locations of each major race track in the US
    cur.execute("""
            SELECT track_name, city, state
            FROM race_locations
    """)
    locations = cur.fetchall()

    all_data = []

    #go thru each location, make API requests
    for location in locations:
        city = location[0]
        state = location[1]
        city = city.replace(" ", "%20")
        state.replace(" ", "%20")

        #make request and get data: for now just getting 25 days from each location, prob have to change later
        response = requests.get("https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}%2C%20{state}/2023-05-01/2023-05-25?unitGroup=us&key=D6SC255PEZV3KFDTGD5ECR6H8&contentType=json")
        if response.status_code == 200:
            weather_data = response.json()
            all_data.append(weather_data) #add data from each location to list
    
    cur.execute("SELECT COUNT(*) FROM weather")
    curr_num_rows = cur.fetchone()[0] #get current num of rows in db since we only want to insert 25 rows at a time

    idx = curr_num_rows / 25
    to_insert = all_data[idx]

    #get data from JSON object
    location = to_insert["name"]
    datetime = to_insert["datetime"]
    temperature = to_insert["temp"]
    dew = to_insert["dew"]
    humidity = to_insert["humidity"]
    windspeed = to_insert["windspeed"]
    visibility = to_insert["visibility"]

    conn.execute("""
            INSERT INTO weather (location, date, temperature, dew, humidity, windspeed, visibility)
            VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (location, datetime, temperature, dew, humidity, windspeed, visibility))
    conn.commit()

    conn.close()
    

    

