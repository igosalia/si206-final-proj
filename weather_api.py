import sqlite3
import requests

database_path = "weather_and_horse_race_data.db"
    
def get_weather_data():
    conn = sqlite3.connect(database_path)
    cur = conn.cursor()
    urls = ["https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Queens%2C%20New%20York/2024-12-09/2024-12-23?unitGroup=us&key=D6SC255PEZV3KFDTGD5ECR6H8&contentType=json", "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Louisville%2C%20Kentucky/2024-12-09/2024-12-23?unitGroup=us&key=D6SC255PEZV3KFDTGD5ECR6H8&contentType=json", "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/New%20Orleans%2C%20Louisiana/2024-12-09/2024-12-23?unitGroup=us&key=D6SC255PEZV3KFDTGD5ECR6H8&contentType=json", "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Del%20Mar%2C%20California/2024-12-09/2024-12-23?unitGroup=us&key=D6SC255PEZV3KFDTGD5ECR6H8&contentType=json", "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Hallandale%20Beach%2C%20Florida/2024-12-09/2024-12-23?unitGroup=us&key=D6SC255PEZV3KFDTGD5ECR6H8&contentType=json", "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Hot%20Springs%2C%20Arkansas/2024-12-09/2024-12-23?unitGroup=us&key=D6SC255PEZV3KFDTGD5ECR6H8&contentType=json", "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Tampa%2C%20Florida/2024-12-09/2024-12-23?unitGroup=us&key=D6SC255PEZV3KFDTGD5ECR6H8&contentType=json"]
    track_names = ["Aqueduct", "Churchill Downs", "Fair Grounds", "Del Mar", "Gulfstream Park", "Oaklawn Park", "Tampa Bay Downs"]
    
    cur.execute("SELECT COUNT(*) FROM weather")
    curr_url_idx = cur.fetchone()[0] / 15
    response = requests.get(urls[int(curr_url_idx)])
    print(response.status_code)
    print(response.text)
    track_name = track_names[int(curr_url_idx)]

    if response.status_code == 200:
        to_insert = response.json()
        days = to_insert["days"]
        for day in days:
            location = to_insert["resolvedAddress"]
            datetime = day["datetime"]
            temperature = day["temp"]
            dew = day["dew"]
            humidity = day["humidity"]
            windspeed = day["windspeed"]
            visibility = day["visibility"]
            conn.execute("""
             INSERT INTO weather (location, track_name, date, temperature, dew, humidity, windspeed, visibility)
             VALUES (?, ?, ?, ?, ?, ?, ?, ?)
             """, (location, track_name, datetime, temperature, dew, humidity, windspeed, visibility))
            conn.commit()      
    else:
        print("Failed to get data")
        exit

    conn.close()
    
if __name__ == "__main__":
    get_weather_data()
