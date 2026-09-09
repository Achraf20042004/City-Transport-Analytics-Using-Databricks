import sqlite3
import hashlib

def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

conn = sqlite3.connect("auth.db")
conn.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('manager','city_responsible')),
    city TEXT
)
""")
conn.commit()

try:
    conn.execute(
        "INSERT INTO users (username, password_hash, role, city) VALUES (?, ?, ?, ?)",
        ("admin", hash_pw("admin"), "manager", None)
    )
    conn.commit()
    print("Manager account created: manager1 / changeme123")
except sqlite3.IntegrityError:
    print("manager1 already exists, skipping.")

conn.close()