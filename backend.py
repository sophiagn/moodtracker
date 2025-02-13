import eel
import sqlite3

#created an empty database
connection = sqlite3.connect("emotion.db")
cursor = connection.cursor()

#Table contains 6 columns, day of week, date, time, emotion intensity level, emotion description, reason
#only creating table when it doesn't exist
cursor.execute("""
               CREATE TABLE IF NOT EXISTS mood_tracker (
               day_of_week TEXT, 
               date TEXT, time TEXT, 
               emotion_intensity_level INTEGER, 
               emotion_descriptor TEXT, 
               reason TEXT
               )
            """)

# checking if table is empty first before inserting sample data
cursor.execute("SELECT COUNT(*) FROM mood_tracker")
row_count = cursor.fetchone()[0] # fetching the result of the first column

if row_count == 0: # only inserting the sample data values if the table is empty
    mood_sample_values = [
    ("Monday", "8-10-2025", "10:00 AM", 1, "Bored", "Nothing to do"),
    ("Friday", "8-14-2025", "6:00 PM", 4, "Excited", "Friends")
    ]
    cursor.executemany("insert into mood_tracker values(?, ?, ?, ?, ?, ?)", mood_sample_values)

for row in cursor.execute("select * from mood_tracker"):
    print(row)

# committing and closing database
connection.commit()
connection.close()

eel.init('frontend')
eel.start('main.html')