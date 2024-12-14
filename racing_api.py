import requests
from requests.auth import HTTPBasicAuth
import sqlite3
import json
from datetime import datetime
import os

database_path = "weather_and_horse_race_data.db"
racecards = []

def make_api_requests():
    #get todays racecards
    url = "https://api.theracingapi.com/v1/racecards/free"
    params = {}
    response = requests.request("GET", url, auth=HTTPBasicAuth('8zp8SbgXUDm0B6GqMlYnaHjS','05d2cBS8wawcdx29sUwF7XuX'), params=params)
    if response.status_code == 200:
        data = response.json()
    if data["racecards"] not in racecards:
        racecards.extend(data["racecards"])
    else:
        print("Error getting data")
        print(response.status_code)

    #get tomorrows racecards
    url = "https://api.theracingapi.com/v1/racecards/free"
    params = {"day": "tomorrow"}
    response = requests.request("GET", url, auth=HTTPBasicAuth('8zp8SbgXUDm0B6GqMlYnaHjS','05d2cBS8wawcdx29sUwF7XuX'), params=params)
    if response.status_code == 200:
        data = response.json()
    if data["racecards"] not in racecards:
        racecards.extend(data["racecards"])
    else:
        print("Error getting data")
        print(response.status_code)
    
    race_cards_file = "racecards.json" #save
    with open(race_cards_file, 'w') as f:
        json.dump(racecards, f)

def get_data():
    with open("racecards.json", 'r') as f:
        racecards_data = json.load(f)
    return racecards_data

def get_racecards():
    racecards_data = get_data()

    conn = sqlite3.connect(database_path)
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM race_cards")
    idx = cur.fetchone()[0]
    for i in range(int(idx), min(int(idx)+25, len(racecards_data))):
        curr_card = racecards_data[i]

        #convert date to unix timestamp
        date = curr_card["date"]
        timestamp = int(datetime.strptime(date, '%Y-%m-%d').timestamp())

        course = curr_card["course"]
        cur.execute("""
            SELECT id FROM course_names
            WHERE course_name = ?
        """, (course,))
        course_id = cur.fetchone()[0]

        conn.execute("""
            INSERT OR IGNORE INTO race_cards (course_id, date, off_time, race_name, distance)
            VALUES (?, ?, ?, ?, ?)
        """, (course_id, timestamp, curr_card["off_time"], curr_card["race_name"], curr_card["distance_f"]))
    conn.commit()
    
    conn.close()

def get_runners():
    conn = sqlite3.connect(database_path)
    cur = conn.cursor()

    runners = []
    racecards_data = get_data()
    #get all the runners
    for racecard in racecards_data:
        race_name = racecard["race_name"]
        cur.execute("""
            SELECT id FROM course_names
            WHERE course_name = ?
        """, (racecard["course"],))
        courseid = cur.fetchone()[0]

        date = racecard["date"]
        timestamp = int(datetime.strptime(date, '%Y-%m-%d').timestamp())

        cur.execute("""
                SELECT raceid FROM race_cards
                WHERE course_id = ? AND race_name = ? AND date = ? AND off_time = ?
        """, (courseid, race_name, timestamp, racecard["off_time"]))
        raceid = cur.fetchone()[0]
        for i in range(len(racecard["runners"])):
            racecard["runners"][i]["raceid"] = raceid
        runners.extend(racecard["runners"])
    
    #insert into DB
    cur.execute("SELECT COUNT(*) FROM horse_info")
    idx = cur.fetchone()[0]
    for i in range(int(idx), min(int(idx) + 25, len(runners))):
        runner = runners[i]
        conn.execute("""
            INSERT INTO horse_info (raceid, horse_name, horse_age, horse_weight, horse_rating, previous_performance)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (runner["raceid"], runner["horse"], runner["age"], runner["lbs"], runner["ofr"], runner["form"]))
    conn.commit()

def clear_db():
    conn = sqlite3.connect(database_path)
    conn.execute("DELETE FROM race_cards")
    conn.execute("DELETE FROM sqlite_sequence WHERE name = 'race_cards'")
    conn.commit()
    conn.close()

def is_empty():
    flag = False
    if not os.path.exists("racecards.json"):
        flag = True
    else:
        with open('racecards.json', 'r') as f:
            data = json.load(f)
            if not data:
                flag = True
    if flag == True:
        make_api_requests() #If we have not already made API requests to get the racecards, run the make_api_requests function
if __name__ == "__main__":
    is_empty()
    get_racecards()

    conn = sqlite3.connect(database_path)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM race_cards")
    count = cur.fetchone()[0]
    if count > 100:
        get_runners()