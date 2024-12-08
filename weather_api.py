import sqlite3
import requests

database_path = "weather_and_horse_race_data.db"
    
def get_weather_data():
    conn = sqlite3.connect(database_path)
    cur = conn.cursor()
    #API request urls of major race tracks: possible TODO: add more locations?
    urls = ["https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Prescott%20Valley/2024-12-08/2024-12-22?unitGroup=us&key=D6SC255PEZV3KFDTGD5ECR6H8&contentType=json", "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Santa%20Rosa%2C%20California/2024-12-08/2024-12-22?unitGroup=us&key=D6SC255PEZV3KFDTGD5ECR6H8&contentType=json", "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Fresno%2C%20California/2024-12-08/2024-12-22?unitGroup=us&key=D6SC255PEZV3KFDTGD5ECR6H8&contentType=json", "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Fresno%2C%20California/2024-12-08/2024-12-22?unitGroup=us&key=D6SC255PEZV3KFDTGD5ECR6H8&contentType=json", "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Vinton%2C%20Louisiana/2024-12-08/2024-12-22?unitGroup=us&key=D6SC255PEZV3KFDTGD5ECR6H8&contentType=json", "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/New%20Orleans%2C%20Lousiana/2024-12-08/2024-12-22?unitGroup=us&key=D6SC255PEZV3KFDTGD5ECR6H8&contentType=json", "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Albuquerque%2C%20New%20Mexico/2024-12-08/2024-12-22?unitGroup=us&key=D6SC255PEZV3KFDTGD5ECR6H8&contentType=json", "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Tulsa%2C%20Oklahoma/2024-12-08/2024-12-22?unitGroup=us&key=D6SC255PEZV3KFDTGD5ECR6H8&contentType=json", "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Grantville%2C%20Pennsylvania/2024-12-08/2024-12-22?unitGroup=us&key=D6SC255PEZV3KFDTGD5ECR6H8&contentType=json"]
    cur.execute("SELECT COUNT(*) FROM weather")
    curr_url_idx = cur.fetchone()[0] / 15
    response = requests.get(urls[int(curr_url_idx)])
    print(response.status_code)
    print(response.text)

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
             INSERT INTO weather (location, date, temperature, dew, humidity, windspeed, visibility)
             VALUES (?, ?, ?, ?, ?, ?, ?)
             """, (location, datetime, temperature, dew, humidity, windspeed, visibility))
             conn.commit()      
    else:
        print("Failed to get data")
        exit

    conn.close()
    
if __name__ == "__main__":
    get_weather_data()
