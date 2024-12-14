import sqlite3

database_path = "weather_and_horse_race_data.db" #use same DB path in each of our files to insert data

def create_db():
    conn = sqlite3.connect(database_path)
    #create tables for each of our APIs/websites:
    #weather api table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS weather
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            location_id INTEGER,
            course_id INTEGER,
            date INTEGER,
            temperature DECIMAL (4, 1),
            dew DECIMAL (4, 1),
            humidity DECIMAL (4, 1),
            windspeed DECIMAL (4, 1),
            visibility DECIMAL (4, 1)
        )
    """)
    conn.commit()

    #so we dont store duplicate string data of the locations
    conn.execute("""
        CREATE TABLE IF NOT EXISTS location_names
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            location_name VARCHAR(150)
        )
    """)
    conn.commit()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS course_names
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_name VARCHAR(150)
        )
    """)
    conn.commit()

    #racing data tables
    conn.execute("""
            CREATE TABLE IF NOT EXISTS race_cards
            (
                raceid INTEGER PRIMARY KEY AUTOINCREMENT,
                course_id INTEGER, 
                date INTEGER, 
                off_time VARCHAR(150), 
                race_name VARCHAR(150),
                distance VARCHAR(150)
            )
    """)
    conn.commit() 

    conn.execute("""
            CREATE TABLE IF NOT EXISTS horse_info
            (
                raceid INTEGER,
                horse_name VARCHAR(150),
                horse_age VARCHAR(150),
                horse_weight VARCHAR(150),
                horse_rating VARCHAR(150),
                previous_performance VARCHAR(150),
                FOREIGN KEY(raceid) REFERENCES race_cards(raceid) ON DELETE CASCADE
            )
    """)
    conn.commit()

    conn.close() #close connection after creating and committing each table creation

#Storing the locations of races on 12/13/2024 and 12/14/2024
def insert_locations_into_db():
    locations = ["Bangor Isycoed, Wrexham, Wales, United Kingdom", "Cheltenham, England, United Kingdom", "Doncaster, England, United Kingdom", "Southwell, England, United Kingdom", "Cork, Ireland", "Dundalk, Ireland", "دبي, الإمارات العربية المتحدة", "Ciudad de Buenos Aires, Ciudad Autónoma de Buenos Aires, Argentina", "Ascot, QLD 4359, Australia", "Deauville, Normandie, France", "Newcastle upon Tyne, England, United Kingdom", "Wolverhampton, England, United Kingdom", "County Meath, Ireland"]
    conn = sqlite3.connect(database_path)
    for location in locations:
        conn.execute("""
            INSERT INTO location_names (location_name)
            VALUES(?)
        """, (location,))
    conn.commit()

def insert_courses_into_db():
    courses = ["Bangor-on-Dee", "Cheltenham", "Doncaster", "Southwell (AW)", "Cork", "Dundalk (AW)", "Meydan", "San Isidro", "Eagle Farm", "Deauville", "Newcastle", "Wolverhampton (AW)", "Fairyhouse"]
    conn = sqlite3.connect(database_path)
    for course in courses:
        conn.execute("""
            INSERT INTO course_names (course_name)
            VALUES(?)
        """, (course,))
    conn.commit()


if __name__ == "__main__":
    create_db()
    insert_locations_into_db()
    insert_courses_into_db()