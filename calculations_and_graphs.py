"""Calculations using weather and racing data"""

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as py
import seaborn as sns
import statsmodels.api as sm

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

def multiple_reg(x, y, x_label, y_label, title):
    #multiple regression 
    x = sm.add_constant(x)
    model = sm.OLS(y, x).fit()
    predictions = model.predict(x)

    print(model.summary())
    write_regression_to_file(model.summary().as_text())

    plt.figure(figsize=(10, 6))

    for i, label in enumerate(x_label):
        plt.scatter(x.iloc[:, i + 1], y, label=label, alpha=0.5)   
    
    #regression line
    plt.plot(x.index, predictions, color='red', linewidth=2, label='Regression Line')

    plt.xlabel('Independent Variables')
    plt.ylabel(y_label)
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.show()

    return model

def calculate_residuals(y, predictions):
    residuals = y - predictions
    return residuals

def residual_plot(x, residuals, x_labels, title):
    for label in x_labels:
        plt.figure(figsize=(10, 6))
        plt.scatter(x[label], residuals, alpha=0.5, label=f'Residuals vs {label}')  # Changed to x[label] to match the DataFrame column names
        plt.axhline(0, color='red', linewidth=2)
        plt.xlabel(label)
        plt.ylabel('Residuals')
        plt.title(f'{title} ({label})')
        plt.legend()
        plt.grid(True)
        plt.show()

def histogram(data, column, title):
    plt.figure(figsize=(10, 6))
    plt.hist(data[column].dropna(), bins=20, color='blue', edgecolor='black', alpha=0.7)
    plt.title(title)
    plt.xlabel(column)
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.show()

def scatter_plot(x, y, x_label, y_label, title):
    plt.figure(figsize=(10, 6))
    plt.scatter(x, y, alpha=0.5, color='blue')
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.grid(True)
    plt.show()

def correlation_plot(data):
    plt.figure(figsize=(10, 8))
    corr_matrix = data[['temperature', 'humidity', 'windspeed', 'visibility', 'horse_rating']].corr()
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', square=True)
    plt.title('Correlation Matrix')
    plt.show()

def write_stats_to_file(weather_stats, filename='calculated_stats.txt'):
    with open(filename, 'w') as file:
        file.write("Weather Statistics:\n")
        file.write(weather_stats.to_string())
        file.write("\n\n")

def write_regression_to_file(regression_summary, filename='calculated_stats.txt'):
    with open(filename, 'a') as file:
        file.write('\n')
        file.write(regression_summary)

def main():
    # Load data
    data = load_data_from_db()
    print(data.head())

    # Convert relevant columns to numeric
    data[['temperature', 'humidity', 'windspeed', 'visibility', 'horse_rating']] = data[['temperature', 'humidity', 'windspeed', 'visibility', 'horse_rating']].apply(pd.to_numeric, errors='coerce')

    # Drop NA
    data.dropna(subset=['temperature', 'humidity', 'windspeed', 'visibility', 'horse_rating'], inplace=True)

    # Weather calculations
    weather_stats = calculate_weather_info(data)
    write_stats_to_file(weather_stats)
    print(weather_stats)

    # Vars for regression
    independent_vars = data[['temperature', 'humidity', 'windspeed', 'visibility']]
    dependent_var = data['horse_rating']

    # Multiple regression
    model = multiple_reg(independent_vars, dependent_var, ['temperature', 'humidity', 'windspeed', 'visibility'], 'Horse Rating', 'Multiple Regression for Horse Rating vs Weather Conditions')  # Changed labels to match DataFrame column names

    # Residuals
    residuals = calculate_residuals(dependent_var, model.predict(sm.add_constant(independent_vars)))
    residual_plot(independent_vars, residuals, ['temperature', 'humidity', 'windspeed', 'visibility'], 'Residuals of Horse Rating vs Weather Conditions')  # Changed labels to match DataFrame column names

    # Scatterplots to show relationships
    scatter_plot(data['temperature'], data['horse_rating'], 'Temperature', 'Horse Rating', 'Horse Rating vs Temperature')
    scatter_plot(data['humidity'], data['horse_rating'], 'Humidity', 'Horse Rating', 'Horse Rating vs Humidity')
    scatter_plot(data['windspeed'], data['horse_rating'], 'Windspeed', 'Horse Rating', 'Horse Rating vs Windspeed')
    scatter_plot(data['visibility'], data['horse_rating'], 'Visibility', 'Horse Rating', 'Horse Rating vs Visibility')

    # Histograms to show distributions
    histogram(data, 'temperature', 'Distribution of Temperature')
    histogram(data, 'humidity', 'Distribution of Humidity')
    histogram(data, 'windspeed', 'Distribution of Windspeed')
    histogram(data, 'visibility', 'Distribution of Visibility')
    histogram(data, 'horse_rating', 'Distribution of Horse Ratings')

    # Correlation plot
    correlation_plot(data)
   

if __name__ == "__main__":
    main()