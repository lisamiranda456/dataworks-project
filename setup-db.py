import sqlite3

# Connect to the database (it will create database.db if it doesn't exist)
conn = sqlite3.connect("./data/database.db")
cur = conn.cursor()

# Create the users table
cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT
    )
""")

# Insert sample data
cur.executemany("INSERT INTO users (name, email) VALUES (?, ?)", [
    ("Lisa Miranda", "lisa.miranda@gramener.com"),
    ("John Doe", "john.doe@example.com"),
    ("Jane Smith", "jane.smith@example.com")
])

# Save and close the database connection
conn.commit()
conn.close()

print("✅ Database setup completed!")
