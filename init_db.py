import sqlite3

# Connect to the database
connection = sqlite3.connect('database/booking.db')
cursor = connection.cursor()

# Create tables if they don't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS shows (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    date TEXT NOT NULL,
    time TEXT NOT NULL,
    total_seats INTEGER
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    show_id INTEGER,
    name TEXT,
    email TEXT,
    seats INTEGER,
    FOREIGN KEY (show_id) REFERENCES shows (id)
)
''')

# ✅ Clear old data (for development/testing)
cursor.execute('DELETE FROM bookings')
cursor.execute('DELETE FROM shows')
connection.commit()

# Insert 7 sample shows
shows = [
    ("Movie Night", "2025-08-01", "18:00", 50),
    ("Stand-up Comedy", "2025-08-03", "20:00", 100),
    ("Music Concert", "2025-08-05", "19:00", 150),
    ("Theatre Drama", "2025-08-07", "18:30", 60),
    ("Tech Talk", "2025-08-10", "14:00", 80),
    ("Magic Show", "2025-08-12", "17:00", 70),
    ("Dance Festival", "2025-08-15", "20:00", 120)
]

cursor.executemany('INSERT INTO shows (name, date, time, total_seats) VALUES (?, ?, ?, ?)', shows)
connection.commit()
connection.close()

print("Database reset and 7 sample shows inserted.")