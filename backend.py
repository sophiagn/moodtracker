import eel
import sqlite3
import json
from datetime import datetime
import os

#--------------------------FUNCTIONS--------------------------

# converting 12 hour time to 24 hour time, sql needs it to be in this format
def convertTimeFormat(timeString):
    return datetime.strptime(timeString, "%I:%M %p").strftime("%H:%M:%S")
#--------------

@eel.expose
def saveToJson(moodJSON):
    conn = sqlite3.connect("emotion.db")
    cursor = conn.cursor()
    try:
        moodEntry = json.loads(moodJSON) #json.load() is a JSON parsing method in python

        if not os.path.exists("jsonSample.txt"):
            with open("jsonSample.txt", "w") as file:
                json.dump({"emotionLog": []}, file)

        #make sure current jsonSample.txt is readable
        with open("jsonSample.txt", "r") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = {"emotionLog": []} # initialize if the file is missing
   
        data["emotionLog"].append(moodEntry)
        with open("jsonSample.txt", "w") as file: #open and write into the jsonSample.txt file
            json.dump(data, file, indent=4)
        

        for entry in data.get("emotionLog", []): #iterates through the emotionLog key and retrieves a list of dictionaries [] so no error occurs if emotionlog doesn't exist
            reasons_str = ", ".join(entry.get("reasons", ["null"])) #converts reasons list to a string separating items with commas
            # key lookup, if it doesn't exist, return null

            # READ
            cursor.execute("""
                    INSERT OR IGNORE INTO mood_tracker (day_of_week, date, time, intensity, emotion, category, reasons)
                    VALUES(?, ?, ?, ?, ?, ?, ?)
                    """, (
                        entry["dayOfWeek"], #accessing value from entry dictionary using key
                        entry["date"],
                        convertTimeFormat(entry["time"]),
                        entry["intensity"],
                        entry["emotion"],
                        entry["category"],
                        reasons_str
            ))
            conn.commit()

        print("Data saved successfully!")
        return "Success"
    except Exception as e: # general try catch error block
        print(f"Error saving to JSON: {e}")
        return "Failed"
#--------------

# Returns most frequent day(s) of the week associated with the given emotion
@eel.expose
def highestFreqEmotionDay(emotion):
    conn = sqlite3.connect("emotion.db")
    cursor = conn.cursor()

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


    if result and result[0] is not None:
        return [row[0] for row in result]
    else:
        return["No corresponding data"]
#--------------

#SQLite built in function strftime('%m, date_column) lets you extract month from a date
#strftime expects to parse date time object that is YYYY MM and DD format
# SQL CASE Statements are similar to if then statements WHEN/THEN
# EX. 09, 10, 11 is Fall and etc
# Count(*) counts the total occurrences for each season
# Filtering with rows that contain the input emotion
# Group By combines all rows containing the same seasons into one count
@eel.expose
def highestFreqEmotionSeason(emotion):
    conn = sqlite3.connect("emotion.db")
    cursor = conn.cursor()
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
    if result and result[0] is not None:
        return [row[0] for row in result]
    else:
        return ["No corresponding data"]
#--------------

@eel.expose
def highestFreqEmotionTime(emotion):
    conn = sqlite3.connect("emotion.db")
    cursor = conn.cursor() 
    query = """ WITH TimeCounts AS (
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
            COUNT(*) AS count
        FROM mood_tracker
        WHERE emotion = ?
        GROUP BY time_category
    )
    SELECT time_category
    FROM TimeCounts
    WHERE count = (SELECT MAX(count) FROM TimeCounts);
    """
    cursor.execute(query, (emotion,) )
    result = cursor.fetchall()
   
    if result and result[0] is not None:
        return [row[0] for row in result]
    else:
        return ["No corresponding data"]
#--------------

@eel.expose
def intensityOverall():
    conn = sqlite3.connect("emotion.db")
    cursor = conn.cursor() 
    query = """
        SELECT
            AVG(intensity)
        FROM mood_tracker
    """
    cursor.execute(query)
    result = cursor.fetchone()

    if result and result[0] is not None:
        return round(result[0], 4) #rounding values in the list
    else:
        return [0.0]
#--------------

@eel.expose
def intensityOverallDay(day_of_week):
    conn = sqlite3.connect("emotion.db")
    cursor = conn.cursor()
    query = """
        SELECT
            AVG(intensity)
    FROM mood_tracker
    WHERE day_of_week = ?    
    """
    cursor.execute(query, (day_of_week,) )
    result = cursor.fetchone()


    if result and result[0] is not None:
        return round(result[0], 4)
    else:
        return "No data available "
#--------------

# Intensity Overall Time 
@eel.expose
def intensityOverallTime(time):
    conn = sqlite3.connect("emotion.db")
    cursor = conn.cursor()
    query = """ WITH TimeCounts AS (
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
    cursor.execute(query, (time,) )
    result = cursor.fetchone()
    
    if result and result[0] is not None:
       return round(result[0], 2)
    else:
        return [0.0]
#--------------

@eel.expose
def intensityOverallSeason(season):
    conn = sqlite3.connect("emotion.db")
    cursor = conn.cursor()

    season_months = {
        "Fall": ["09", "10", "11"],
        "Winter": ["12", "01", "02"],
        "Spring": ["03", "04", "05"],
        "Summer": ["06", "07", "08"]
    }

    months = season_months.get(season, [])
    if not months:
        return f"Invalid season: {season}"

    query = f"""
        SELECT AVG(intensity)
        FROM mood_tracker
        WHERE strftime('%m', date) IN ({','.join(['?'] * len(months))});
    """

    cursor.execute(query, tuple(months))
    result = cursor.fetchone()

    if result and result[0] is not None:
        return round(result[0], 2)
    else:
        return 0.0  
#--------------

@eel.expose
def intensityByDay(emotion, day_of_week):
    conn = sqlite3.connect("emotion.db")
    cursor = conn.cursor()

    # Create a SQL query to calculate the average intensity for the emotion on the specified day
    query = """
        SELECT AVG(intensity)
        FROM mood_tracker
        WHERE LOWER(emotion) = LOWER(?)
        AND day_of_week = ?;
    """

    # Execute the query with the emotion and day number as parameters
    cursor.execute(query, (emotion, day_of_week))
    result = cursor.fetchone()

    # Display the result
    if result and result[0] is not None:
        return round(result[0], 2)
    else:
        return 0.0
#--------------

@eel.expose
def intensityByTime(emotion, time):
    conn = sqlite3.connect("emotion.db")
    cursor = conn.cursor()
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
    cursor.execute(query, (emotion, time))
    result = cursor.fetchone()

    # Display the result
    if result and result[0] is not None:
        return round(result[0], 2)
    else:
        return 0.0
#--------------

@eel.expose
def intensityBySeason(emotion, season):
    conn = sqlite3.connect("emotion.db")
    cursor = conn.cursor()
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
        return (f"Invalid season: {season}")

    # Create a SQL query to calculate the average intensity for the emotion during the season
    query = f"""
        SELECT AVG(intensity)
        FROM mood_tracker
        WHERE LOWER(emotion) = LOWER(?)
        AND strftime('%m', date) IN ({','.join(['?'] * len(months))});
    """
    # Execute the query with the emotion and months as parameters
    cursor.execute(query, tuple([emotion] + months))
    result = cursor.fetchone()

    # Display the result
    if result and result[0] is not None:
        return round(result[0], 2)
    else:
        return 0.0
#--------------

@eel.expose
def highestFreqReason(emotion):
    conn = sqlite3.connect("emotion.db")
    cursor = conn.cursor()
    query = """
    WITH ReasonCounts AS (
        SELECT
            CASE
                WHEN reasons IN (
                'Unknown',
                'No reason',
                'Physical health',
                'Mental disorder',
                'Friends',
                'Partner',
                'Family',
                'School',
                'Work',
                'Thoughts about the future',
                'Thoughts about the past',
                'Myself'
            ) THEN reasons
            END AS reasons,
            COUNT(*) AS count
        FROM mood_tracker
        WHERE emotion = ?
        GROUP BY reasons
    )
    SELECT reasons
    FROM ReasonCounts
    WHERE count = (SELECT MAX(count) FROM ReasonCounts);
    """
    cursor.execute(query, (emotion, ))
    result = cursor.fetchall()
    if result and result[0] is not None:
        return "; ".join([row[0] for row in result])
    else:
        return ["No corresponding data"]

#--------------------------MAIN--------------------------

# created an empty database
conn = sqlite3.connect("emotion.db")
cursor = conn.cursor() # cursor object that allows us to traverse our database, and cursor.execute to interact with database via sql request

# unique only adds unique values to the table
cursor.execute("""
               CREATE TABLE IF NOT EXISTS mood_tracker (
                    day_of_week TEXT,
                    date TEXT,
                    time TEXT,
                    intensity INTEGER,
                    emotion TEXT,
                    category TEXT,
                    reasons TEXT,
                    UNIQUE(date, time, emotion)
               );
            """)  #Table contains 7 columns, day of week, date, time, (emotion) intensity, emotion, category, reasons

try:
    os.remove("jsonSample.txt")
    print("jsonSample.txt deleted successfully.")
except FileNotFoundError:
    print("File not found, nothing to delete")

conn.commit()
conn.close()

eel.init('frontend')
eel.start('main.html', size=(800, 600))