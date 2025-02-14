import eel
import sqlite3
import json

#created an empty database - CREATE
conn = sqlite3.connect("emotion.db")
cursor = conn.cursor()

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