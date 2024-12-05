import sqlite3

database_path = "weather_and_horse_race_data.db" #use same DB path in each of our files to insert data

def create_db():
    conn = sqlite3.connect(database_path)
    #create tables for each of our APIs/websites:

    #TODO: can have a race id foreign key thing that correlates in the equibase table, 
    # racing API table, and the weather api table so we can use this for calculations and database JOINS

    #weather api table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS weather
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            raceid INTEGER,
            location VARCHAR(120),
            date DATETIME NOT NULL,
            temperature DECIMAL (4, 1),
            dew DECIMAL (4, 1),
            humidity DECIMAL (4, 1),
            windspeed DECIMAL (4, 1),
            visibility DECIMAL (4, 1)
            
            FOREIGN KEY(raceid) REFERENCES equibase(raceid) ON DELETE CASCADE
        )
    """)
    conn.commit()

    #equibase table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS equibase
        (
            raceid INTEGER PRIMARY KEY AUTOINCREMENT,
            track_name VARCHAR(150),
            location VARCHAR(120),
            date DATETIME NOT NULL,
            winner_name VARCHAR(150), 
            racetime_minutes INTEGER,
            track_type VARCHAR(120),
        )
    """)
    conn.commit()

    #racing API table


    #wikipedia table
    

    conn.close() #close connection after creating and committing each table creation
