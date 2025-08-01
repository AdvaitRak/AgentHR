import sqlite3

conn = sqlite3.connect("db/hr_agent_demo.sqlite")
cursor = conn.cursor()

# ✅ List all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("📦 Tables in your database:")
for table in tables:
    print("-", table[0])