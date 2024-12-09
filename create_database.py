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
            location VARCHAR(120),
            track_name VARCHAR(150),
            date DATETIME NOT NULL,
            temperature DECIMAL (4, 1),
            dew DECIMAL (4, 1),
            humidity DECIMAL (4, 1),
            windspeed DECIMAL (4, 1),
            visibility DECIMAL (4, 1)
        )
    """)
    conn.commit()

    #racing API data tables
    conn.execute("""
        CREATE TABLE IF NOT EXISTS racedata
        (
            raceid INTEGER PRIMARY KEY AUTOINCREMENT,
            racetype VARCHAR(120),
            location VARCHAR(120),
            date DATETIME NOT NULL,
            winner_name VARCHAR(150), 
            racetime_minutes INTEGER
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS race_track_info
        (
            raceid INTEGER, 
            track_type VARCHAR(120),
            track_name VARCHAR(150),
            FOREIGN KEY(raceid) REFERENCES racedata(raceid) ON DELETE CASCADE
        )
    """)
    conn.commit()
    
    conn.close() #close connection after creating and committing each table creation

if __name__ == "__main__":
    create_db()