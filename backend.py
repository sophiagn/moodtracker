import eel
import sqlite3
import json

#created an empty database - CREATE
conn = sqlite3.connect("emotion.db")
cursor = conn.cursor() # cursor object that allows us to traverse our database, and cursor.execute to interact with database via sql request

#only creates table when it doesn't exist
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
            """)  #Table contains 7 columns, day of week, date, time, (emotion) intensity, emotion, category, reasons

#opens and reads the JSON file
with open("jsonSample.txt", "r") as input:
    inputFile = json.load(input)

for entry in inputFile.get("emotionLog", []): #iterates through the emotionLog key and retrieves a list of dictionaries [] so no error occurs if emotionlog doesn't exist
    reasons_str = ", ".join(entry.get("reasons", ["null"])) #converts reasons list to a string separating items with commas
    # key lookup, if it doesn't exist, return null

    # READ
    cursor.execute("""
               INSERT INTO mood_tracker (day_of_week, date, time, intensity, emotion, category, reasons)
               VALUES(?, ?, ?, ?, ?, ?, ?)
               """, (
                   entry["dayOfWeek"], #accessing value from entry dictionary using key
                   entry["date"],
                   entry["time"],
                   entry["intensity"],
                   entry["emotion"],
                   entry["category"],
                   reasons_str
    ))

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

