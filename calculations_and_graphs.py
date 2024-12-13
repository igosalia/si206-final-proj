"""Calculations using weather and racing data"""

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as py
import seaborn as sns

database_path = "weather_and_horse_race_data.db"

def load_data_from_db():
    conn = sqlite3.connect(database_path)

    #joining race_card, horse_info, and weather
    query = """
        SELECT rc.course, rc.date, hi.horse_name, hi.horse_age, hi.horse_weight,
        hi.horse_rating, w.temperature, w.humidity, w.windspeed, w.visibility
        FROM race_cards rc
        JOIN horse_info hi ON rc.raceid = hi.raceid
        JOIN weather w ON rc.course = w.track_name AND rc.date = w.date
    """

    data = pd.read_sql_query(query, conn)
    conn.close()
    return data

def calculate_weather_info(data):
    #group by track and calculate mean for each weather attr
    weather_stats = data.groupby('course')[['temperature', 'humidity', 'windspeed', 'visibility']].mean()
    #add header to weather dataframe
    weather_stats.rename(columns={
        'temperature': 'average_temp',
        'humidity' : 'average_humidity',
        'windspeed' : 'average_windspeed',
        'visibility' : 'average_visibility'
    }, inplace=True)

    return weather_stats

def linreg(x, y):
    #linear regression 
    x = py.array(x)
    y = py.array(y)
    A = py.vstack([x, py.ones(len(x))]).T
    slope, intercept = py.linalg.lstsq(A, y, rcond=None)[0]
    return slope, intercept

def calculate_residuals(x, y, slope, intercept):
    predicted_y = slope * x + intercept
    residuals = y - predicted_y
    return residuals

def scatter_plot(x, y, x_label, y_label, title):
    plt.figure(figsize=(10, 6))
    plt.scatter(x, y, color='blue', alpha=0.5)
    slope, intercept = linreg(x, y) #call linreg
    x_range = py.linspace(min(x), max(x), 100)
    plt.plot(x_range, slope * x_range + intercept, color='red', linewidth=2)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.grid(True)
    plt.show()
    return slope, intercept

def residual_plot(x, y, residuals, x_label, title):
    plt.figure(figsize=(10,6))
    plt.scatter(x, residuals, color='blue', alpha=0.5)
    plt.axhline(0, color='red', linewidth=2)
    plt.xlabel(x_label)
    plt.ylabel('Residuals')
    plt.title(title)
    plt.grid(True)
    plt.show()


tracks = ["Bangor-on-Dee", "Cheltenham", "Doncaster", "Southwell (AW)", "Cork", "Dundalk (AW)", "Meydan", "San Isidro", "Eagle Farm", "Deauville", "Newcastle", "Wolverhampton (AW)", "Fairyhouse"]
weather_tracks_map = {}

conn = sqlite3.connect(database_path)
cur = conn.cursor()

def main():
    #load data
    data = load_data_from_db()
    print(data.head())

    #convert relevant columns to numeric
    data[['temperature', 'humidity', 'windspeed', 'visibility', 'horse_rating']] = data[['temperature', 'humidity', 'windspeed', 'visibility', 'horse_rating']].apply(pd.to_numeric, errors='coerce')

    #drop NA
    data.dropna(subset=['temperature', 'humidity', 'windspeed', 'visibility', 'horse_rating'], inplace=True)

    #weather calculations
    weather_stats = calculate_weather_info(data)
    print(weather_stats)

    #data for scatterplots
    horse_ratings = data['horse_rating']
    temperatures = data['temperature']
    humidities = data['humidity']
    windspeed = data['windspeed']
    visibility = data['visibility']

    #show scatterplots for regression with horse_ratings as dependent var
    slope, intercept = scatter_plot(temperatures, horse_ratings, 'Temperature', 'Horse Rating', 'Horse Rating vs Temperature')
    residuals = calculate_residuals(temperatures, horse_ratings, slope, intercept)
    residual_plot(temperatures, horse_ratings, residuals, 'Temperature', 'Residuals of Horse Rating vs Temperature')

    slope, intercept = scatter_plot(humidities, horse_ratings, 'Humidity', 'Horse Rating', 'Horse Rating vs Humidity')
    residuals = calculate_residuals(humidities, horse_ratings, slope, intercept)
    residual_plot(humidities, horse_ratings, residuals, 'Humidity', 'Residuals of Horse Rating vs Humidity')

    slope, intercept = scatter_plot(windspeed, horse_ratings, 'Windspeed', 'Horse Rating', 'Horse Rating vs Windspeed')
    residuals = calculate_residuals(windspeed, horse_ratings, slope, intercept)
    residual_plot(windspeed, horse_ratings, residuals, 'Windspeed', 'Residuals of Horse Rating vs Windspeed')

    slope, intercept = scatter_plot(visibility, horse_ratings, 'Visibility', 'Horse Rating', 'Horse Rating vs Visibility')
    residuals = calculate_residuals(visibility, horse_ratings, slope, intercept)
    residual_plot(visibility, horse_ratings, residuals, 'Visibility', 'Residuals of Horse Rating vs Visibility')

if __name__ == "__main__":
    main()