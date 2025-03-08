import eel
import sqlite3
import json
import os
from datetime import datetime


conn = sqlite3.connect("emotion.db")
cursor = conn.cursor() # cursor object that allows us to traverse our database, and cursor.execute to interact with database via sql request


# Create table if it doesn't exist already
# cursor.execute to interact with database via sql request
cursor.execute("""
               CREATE TABLE IF NOT EXISTS mood_tracker ( 
                    day_of_week TEXT, 
                    date TEXT, 
                    time TEXT, 
                    intensity INTEGER, 
                    emotion TEXT,
                    category TEXT, 
                    reasons TEXT
               )
            """)

# Opens and reads the sample JSON file
with open("jsonSample.txt", "r") as input:
    inputFile = json.load(input)

# Iterate thru emotionLog key and retrieve a list of dictionaries so no error occurs if emotionlog doesn't exist
for entry in inputFile.get("emotionLog", []): 

    # Convert reasons list to a string separating items with commas
    # Key lookup, if it doesn't exist, return null
    reasons_str = ", ".join(entry.get("reasons", ["null"])) 

    #--------CREATE---------
    cursor.execute("""
               INSERT INTO mood_tracker (day_of_week, date, time, intensity, emotion, category, reasons)
               VALUES(?, ?, ?, ?, ?, ?, ?)
               """, (
                   entry["dayOfWeek"], # Accessing value from entry dictionary using key
                   entry["date"],
                   entry["time"],
                   entry["intensity"],
                   entry["emotion"],
                   entry["category"],
                   reasons_str
    ))


#-------------------------------------SEARCH-------------------------------------------

# Returns most frequent day(s) of the week associated with the given emotion
def highestFreqEmotionDay(emotion):
    query = """
    WITH EmotionCounts AS (
        SELECT
            day_of_week,
            COUNT(*) AS count
        FROM mood_tracker
        WHERE emotion = ?
        GROUP BY day_of_week
    )
    SELECT day_of_week
    FROM EmotionCounts
    WHERE count = (SELECT MAX(count) FROM EmotionCounts);
    """
    # EmotionCounts = a temporary table that exists only for query
    # selects day_of_week and counting occurences of each day and storing in count column
    # data comes from mood_tracker table
    # filtering only the rows that match the input (?) emotion
    # Group By day_of_week - combines all the rows that have same day_of_week value (counting how often each day appears)
    
    cursor.execute(query, (emotion, ))
    result = cursor.fetchall()

    if result:
        return [row[0] for row in result]
    else:
        return["No matching data"]
    
emotion = "Content"
mostFrequentDays = highestFreqEmotionDay(emotion)
print(mostFrequentDays)

#---------------------------------------
#SQLite built in function strftime('%m, date_column) lets you extract month from a date
#strftime expects to parse date time object that is YYYY MM and DD format
# SQL CASE Statements are similar to if then statements WHEN/THEN
# EX. 09, 10, 11 is Fall and etc
# Count(*) counts the total occurrences for each season
# Filtering with rows that contain the input emotion
# Group By combines all rows containing the same seasons into one count
def highestFreqEmotionSeason(emotion):
    query = """
    WITH SeasonCounts AS (
        SELECT
            CASE
                WHEN strftime('%m', date) IN ('09', '10', '11') THEN 'Fall'
                WHEN strftime('%m', date) IN ('12', '01', '02') THEN 'Winter'
                WHEN strftime('%m', date) IN ('03', '04', '05') THEN 'Spring'
                WHEN strftime('%m', date) IN ('06', '07', '08') THEN 'Summer'
            END AS season,
            COUNT(*) AS count
        FROM mood_tracker
        WHERE emotion = ?
        GROUP BY season
    )
    SELECT season
    FROM SeasonCounts
    WHERE count = (SELECT MAX(count) FROM SeasonCounts);
    """
    cursor.execute(query, (emotion, ))
    result = cursor.fetchall()
    if result:
        return [row[0] for row in result]
    else:
        return ["No matching data"]

emotion = "Content"
mostFrequentSeason = highestFreqEmotionSeason(emotion)
print(mostFrequentSeason)


# ------------------------------
#commented out SQL testing code
#def highestDayFreqEmotion():
#    query = """
#    SELECT day_of_week FROM mood_tracker
#    WHERE emotion = 'Content'
#    """
#    return query

#SQlite cursor.execute() requires a tuple or list for query paramaters, so , after emotion
#mostFrequentDay = cursor.execute(highestDayFreqEmotion()).fetchall() #fetchone() returns a tuple with a single value from the first matching row
#if mostFrequentDay:
#    for day in mostFrequentDay:
#        print(day[0]) # index 0 accesses the first element in the tuple
#else:
#    print("No data found") # error handling in the case that there isn't a match
# ---------------------------------

# --------------------------------------
# Intensity Overall Time 

def intensityOverallTime(time):
    query = """
    WITH TimeCounts AS (
        SELECT
            CASE 
                WHEN strftime('%H:%M', time) BETWEEN '06:00' AND '09:59' THEN 'Morning'
                WHEN strftime('%H:%M', time) BETWEEN '10:00' AND '11:59' THEN 'Late Morning'
                WHEN strftime('%H:%M', time) BETWEEN '12:00' AND '15:59' THEN 'Afternoon'
                WHEN strftime('%H:%M', time) BETWEEN '16:00' AND '17:59' THEN 'Early Evening'
                WHEN strftime('%H:%M', time) BETWEEN '18:00' AND '20:59' THEN 'Evening'
                WHEN strftime('%H:%M', time) BETWEEN '21:00' AND '23:59' THEN 'Night'
                WHEN strftime('%H:%M', time) BETWEEN '00:00' AND '03:59' THEN 'Late Night'
                WHEN strftime('%H:%M', time) BETWEEN '04:00' AND '05:59' THEN 'Early Morning'
            END AS time_category,
            intensity
        FROM mood_tracker
    )
    SELECT AVG(intensity)
    FROM TimeCounts
    WHERE time_category = ?;
    """
    cursor.execute(query, (time,))  
    result = cursor.fetchone()
    
    if result and result[0] is not None:
        print(f"Average intensity during {time}: {round(result[0], 2)}")
    else:
        print(f"No data available for {time}.")

# Example usage
emotion = "Stressed"
time = "Afternoon"
average_intensity = intensityOverallTime(emotion, time)
print(average_intensity)

    # ----------------------------------------

def intensityOverallSeason(season):
    # Map seasons to their corresponding months
    season_months = {
        "Fall": ["09", "10", "11"],
        "Winter": ["12", "01", "02"],
        "Spring": ["03", "04", "05"],
        "Summer": ["06", "07", "08"]
    }

    # Get the months for the specified season
    months = season_months.get(season, [])
    if not months:
        print(f"Invalid season: {season}")
        return

    # Create a SQL query to calculate the average intensity for the emotion during the season
    query = """
        SELECT AVG(intensity)
        FROM mood_tracker
        WHERE strftime('%m', date) IN ({});
    """.format(",".join("?" * 3))

    # Execute the query with the emotion and months as parameters
    cursor.execute(query, (months))
    result = cursor.fetchone()

    # Display the result
    if result and result[0] is not None:
        print(f"Average intensity for {emotion} during {season}: {round(result[0], 2)}")
    else:
        print(f"No data available for {emotion} during {season}")

    # ------------------------------
def intensityByDay(emotion, day_of_week):
    # Map day of the week to its corresponding SQLite strftime format
    day_mapping = {
        "Monday": "1",
        "Tuesday": "2",
        "Wednesday": "3",
        "Thursday": "4",
        "Friday": "5",
        "Saturday": "6",
        "Sunday": "0"
    }

    # Get the numeric representation of the day of the week
    day_number = day_mapping.get(day_of_week.capitalize())
    if day_number is None:
        print(f"Invalid day of the week: {day_of_week}")
        return

    # Create a SQL query to calculate the average intensity for the emotion on the specified day
    query = """
        SELECT AVG(intensity)
        FROM mood_tracker
        WHERE emotion = ?
        AND strftime('%w', time) = ?;
    """

    # Execute the query with the emotion and day number as parameters
    cursor.execute(query, (emotion, day_number))
    result = cursor.fetchone()

    # Display the result
    if result and result[0] is not None:
        print(f"Average intensity for {emotion} on {day_of_week}: {round(result[0], 2)}")
    else:
        print(f"No data available for {emotion} on {day_of_week}")

# -------------------
def intensityByTimeWithCase(emotion, time_of_day):
    # Create a SQL query to calculate the average intensity for the emotion during the specified time category
    query = """
        WITH TimeCategories AS (
            SELECT
                CASE 
                    WHEN strftime('%H:%M', time) BETWEEN '06:00' AND '09:59' THEN 'Morning'
                    WHEN strftime('%H:%M', time) BETWEEN '10:00' AND '11:59' THEN 'Late Morning'
                    WHEN strftime('%H:%M', time) BETWEEN '12:00' AND '15:59' THEN 'Afternoon'
                    WHEN strftime('%H:%M', time) BETWEEN '16:00' AND '17:59' THEN 'Early Evening'
                    WHEN strftime('%H:%M', time) BETWEEN '18:00' AND '20:59' THEN 'Evening'
                    WHEN strftime('%H:%M', time) BETWEEN '21:00' AND '23:59' THEN 'Night'
                    WHEN strftime('%H:%M', time) BETWEEN '00:00' AND '03:59' THEN 'Late Night'
                    WHEN strftime('%H:%M', time) BETWEEN '04:00' AND '05:59' THEN 'Early Morning'
                END AS time_category,
                intensity
            FROM mood_tracker
            WHERE emotion = ?
        )
        SELECT AVG(intensity)
        FROM TimeCategories
        WHERE time_category = ?;
    """

    # Execute the query with the emotion and time of day as parameters
    cursor.execute(query, (emotion, time_of_day))
    result = cursor.fetchone()

    # Display the result
    if result and result[0] is not None:
        print(f"Average intensity for {emotion} during {time_of_day}: {round(result[0], 2)}")
    else:
        print(f"No data available for {emotion} during {time_of_day}")

# -------------------

def intensityBySeason(emotion, season):
    # Map seasons to their corresponding months
    season_months = {
        "Fall": ["09", "10", "11"],
        "Winter": ["12", "01", "02"],
        "Spring": ["03", "04", "05"],
        "Summer": ["06", "07", "08"]
    }

    # Get the months for the specified season
    months = season_months.get(season)
    if not months:
        print(f"Invalid season: {season}")
        return

    # Create a SQL query to calculate the average intensity for the emotion during the season
    query = """
        SELECT AVG(intensity)
        FROM mood_tracker
        WHERE emotion = ?
        AND strftime('%m', time) IN ({});
    """.format(",".join("?" * len(months)))

    # Execute the query with the emotion and months as parameters
    cursor.execute(query, (emotion, *months))
    result = cursor.fetchone()

    # Display the result
    if result and result[0] is not None:
        print(f"Average intensity for {emotion} during {season}: {round(result[0], 2)}")
    else:
        print(f"No data available for {emotion} during {season}")


#testing
#cursor.execute("SELECT * from mood_tracker")
#entries = cursor.fetchall()
#print(f"Number of records inserted: {len(entries)}")
#for row in entries:
    #print(row)



# Commit and close database
conn.commit()

conn.close()

eel.init('frontend')
eel.start('main.html')

