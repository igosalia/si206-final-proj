import sqlite3
import requests
from datetime import datetime

database_path = "weather_and_horse_race_data.db"

def get_weather_data():
    conn = sqlite3.connect(database_path)
    cur = conn.cursor()

    urls = ["https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Bangor-on-Dee%2C%20Wales?unitGroup=us&key=D6SC255PEZV3KFDTGD5ECR6H8&contentType=json", "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Cheltenham%2C%20United%20Kingdom?unitGroup=us&key=D6SC255PEZV3KFDTGD5ECR6H8&contentType=json", "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Doncaster%2C%20United%20Kingdom?unitGroup=us&key=D6SC255PEZV3KFDTGD5ECR6H8&contentType=json", "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Southwell%2C%20United%20Kingdom?unitGroup=us&key=D6SC255PEZV3KFDTGD5ECR6H8&contentType=json", "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Cork%2C%20Ireland?unitGroup=us&key=D6SC255PEZV3KFDTGD5ECR6H8&contentType=json", "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Dundalk%2C%20Louth%2C%20Ireland?unitGroup=us&key=D6SC255PEZV3KFDTGD5ECR6H8&contentType=json", "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Dubai%2C%20United%20Arab%20Emirates?unitGroup=us&key=D6SC255PEZV3KFDTGD5ECR6H8&contentType=json", "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Buenos%20Aires%2C%20Argentina?unitGroup=us&key=D6SC255PEZV3KFDTGD5ECR6H8&contentType=json", "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Ascot%2C%20Australia?unitGroup=us&key=D6SC255PEZV3KFDTGD5ECR6H8&contentType=json", "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Deauville%2C%20France?unitGroup=us&key=D6SC255PEZV3KFDTGD5ECR6H8&contentType=json", "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Newcastle%20upon%20Tyne%2C%20United%20Kingdom?unitGroup=us&key=D6SC255PEZV3KFDTGD5ECR6H8&contentType=json", "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Wolverhampton%2C%20United%20Kingdom?unitGroup=us&key=D6SC255PEZV3KFDTGD5ECR6H8&contentType=json", "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/County%20Meath%2C%20Ireland?unitGroup=us&key=D6SC255PEZV3KFDTGD5ECR6H8&contentType=json"]
    
    track_names = ["Bangor-on-Dee", "Cheltenham", "Doncaster", "Southwell (AW)", "Cork", "Dundalk (AW)", "Meydan", "San Isidro", "Eagle Farm", "Deauville", "Newcastle", "Wolverhampton (AW)", "Fairyhouse"]
    
    cur.execute("SELECT COUNT(*) FROM weather")
    curr_url_idx = cur.fetchone()[0] / 15
    if(int(curr_url_idx) >= len(urls)):
        print("All data has been loaded into database already")
        return
    response = requests.get(urls[int(curr_url_idx)])
    
    track_name = track_names[int(curr_url_idx)]

    if response.status_code == 200:
        to_insert = response.json()
        days = to_insert["days"]
        for day in days:
            location = to_insert["resolvedAddress"]

            #convert date to unix timestamp
            date = day["datetime"]
            timestamp = int(datetime.strptime(date, '%Y-%m-%d').timestamp())

            temperature = day["temp"]
            dew = day["dew"]
            humidity = day["humidity"]
            windspeed = day["windspeed"]
            visibility = day["visibility"]
            
            cur.execute("""
                SELECT id FROM course_names WHERE course_name = ?
            """, (track_name,))
            course_id = cur.fetchone()[0]

            cur.execute("""
                SELECT id FROM location_names WHERE location_name = ?
            """, (location,))
            location_id = cur.fetchone()[0]

            conn.execute("""
             INSERT INTO weather (location_id, course_id, date, temperature, dew, humidity, windspeed, visibility)
             VALUES (?, ?, ?, ?, ?, ?, ?, ?)
             """, (location_id, course_id, timestamp, temperature, dew, humidity, windspeed, visibility))
            conn.commit()      
    else:
        print("Failed to get data")
        exit

    conn.close()
    
if __name__ == "__main__":
    get_weather_data()
