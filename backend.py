import eel
import sqlite3
import json
import datetime
from datetime import datetime


#created an empty database - CREATE
conn = sqlite3.connect("emotion.db")
cursor = conn.cursor() # cursor object that allows us to traverse our database, and cursor.execute to interact with database via sql request


#unique only adds unique values to the table
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


# fixed error here
@eel.expose #exposing the function to main.js
def saveToJson(moodJSON):
    try:
        moodEntry = json.loads(moodJSON) #json.load() is a JSON parsing method in python


        #make sure current jsonSample.txt is readable
        try:
            with open("jsonSample.txt", "r") as file:
                data = json.load(file)
        except (FileNotFoundError):
            data = {"emotionLog": []} # initialize if the file is missing
   
        data["emotionLog"].append(moodEntry)
        with open("jsonSample.txt", "w") as file: #open and write into the jsonSample.txt file
            json.dump(data, file, indent=4)
       
        print("Data saved successfully!")
        return "Success"
    except Exception as e: # general try catch error block
        print(f"Error saving to JSON: {e}")
        return "Failed"


#converting 12 hour time to 24 hour time, sql needs it to be in this format
def convertTimeFormat(timeString):
    return datetime.strptime(timeString, "%I:%M %p").strftime("%H:%M:%S")


#opens and reads the JSON file
with open("jsonSample.txt", "r") as input:
    inputFile = json.load(input)


for entry in inputFile.get("emotionLog", []): #iterates through the emotionLog key and retrieves a list of dictionaries [] so no error occurs if emotionlog doesn't exist
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

@eel.expose
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
    #EmotionCounts = a temporary table that exists only for query
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


emotion = "Stressed"
mostFrequentSeason = highestFreqEmotionSeason(emotion)
print(mostFrequentSeason)


#-------------------------------


def highestFreqEmotionTime(emotion):
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
            END AS time_categories,
            COUNT(*) AS count
        FROM mood_tracker
        WHERE emotion = ?
        GROUP BY time_categories
    )
    SELECT time_categories
    FROM TimeCounts
    WHERE count = (SELECT MAX(count) FROM TimeCounts);
    """
    cursor.execute(query, (emotion,) )
    result = cursor.fetchall()
   
    if result:
        return [row[0] for row in result]
    else:
        return ["No matching data"]


emotion = 'Content'
mostFrequentTimeCategory = highestFreqEmotionTime(emotion)
print(mostFrequentTimeCategory)


# ------------------------------


def intensityOverall():
    query = """
        SELECT
            AVG(intensity)
        FROM mood_tracker
    """
    cursor.execute(query)
    result = cursor.fetchall()


    if result:
        return [round(row[0], 4) for row in result] #rounding values in the list
    else:
        return 0


averageIntensity = intensityOverall()
print(averageIntensity)


#-------------------------------


def intensityOverallDay(day_of_week):
    query = """
        SELECT
            AVG(intensity)
    FROM mood_tracker
    WHERE day_of_week = ?    
    """
    cursor.execute(query, (day_of_week,) )
    result = cursor.fetchone()


    if result:
        return [round(result[0], 4)]
    else:
        return 0
   
day_of_week = 'Monday'
dayIntensity = intensityOverallDay(day_of_week)
print(dayIntensity)




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




#testing
#cursor.execute("SELECT * from mood_tracker")
#entries = cursor.fetchall()
#print(f"Number of records inserted: {len(entries)}")
#for row in entries:
    #print(row)


# committing and closing database
conn.commit()
conn.close()


eel.init('frontend')
eel.start('main.html')








