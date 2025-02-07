import eel
import sqlite3

#created an empty database
connection = sqlite3.connect("emotion.db")
cursor = connection.cursor()

#Table contains 6 columns, day of week, date, time, emotion intensity level, emotion description, reason
cursor.execute("create table mood_tracker (day_of_week TEXT, date TEXT, time TEXT, emotion_intensity_level INTEGER, emotion_descriptor TEXT, reason TEXT)")

mood_sample_values = [
    ("Monday", "8-10-2025", "10:00 AM", 1, "Bored", "Nothing to do"),
    ("Friday", "8-14-2025", "6:00 PM", 4, "Excited", "Friends")
]

cursor.executemany("insert into mood_tracker values(?, ?, ?, ?, ?, ?)", mood_sample_values)

for row in cursor.execute("select * from mood_tracker"):
    print(row)

connection.commit()
connection.close()

eel.init('frontend')
eel.start('main.html')