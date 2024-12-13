import sqlite3

database_path = "weather_and_horse_race_data.db" #use same DB path in each of our files to insert data

def create_db():
    conn = sqlite3.connect(database_path)
    #create tables for each of our APIs/websites:

    #wikipedia table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS wikipedia
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            venue VARCHAR(255),
            location VARCHAR(255)
        )
    """)
    conn.commit()

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

    #racing data tables
    conn.execute("""
            CREATE TABLE IF NOT EXISTS race_cards
            (
                raceid INTEGER PRIMARY KEY AUTOINCREMENT,
                course VARCHAR(150), 
                date VARCHAR(150), 
                off_time VARCHAR(150), 
                race_name VARCHAR(150),
                distance VARCHAR(150),
                region VARCHAR(150),
                type VARCHAR(150),
                track_condition VARCHAR(150),
                surface_type VARCHAR(150)
            )
    """)
    conn.commit() 

    conn.execute("""
            CREATE TABLE IF NOT EXISTS horse_info
            (
                raceid INTEGER,
                horse_name VARCHAR(150),
                horse_age VARCHAR(150),
                region VARCHAR(150),
                horse_weight VARCHAR(150),
                horse_rating VARCHAR(150),
                previous_performance VARCHAR(150),
                FOREIGN KEY(raceid) REFERENCES race_cards(raceid) ON DELETE CASCADE
            )
    """)
    conn.commit()

    conn.close() #close connection after creating and committing each table creation

if __name__ == "__main__":
    create_db()