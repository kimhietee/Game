import json
import os
import sqlite3, hashlib



def loadFile(filePath):
    #Loads the playlist from a JSON file. Returns an empty list if file missing.
    if not os.path.exists(filePath):
        return {}

    try:
        with open(filePath, "r") as file:
            return json.load(file)
    except (json.JSONDecodeError, IOError):
        print("Error loading playlist. Returning empty list.")
        return {}


def saveFile(filePath, data):
    # Saves the playlist to a JSON file.
    try:
        with open(filePath, "w") as file:
            json.dump(data, file, indent=4)
        print(f"saved {filePath} successfully.")
    except IOError:
        print("Error saving.")







os.makedirs("database/user_data", exist_ok=True)
os.makedirs("database/user_info", exist_ok=True)


conn = sqlite3.connect("database/user_data/user.db")  # creates file if not exists
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")
conn.commit()


conn2 = sqlite3.connect("database/user_info/user_info_store.db")

cursor2 = conn2.cursor()

cursor2.execute("""
CREATE TABLE IF NOT EXISTS user_info (
    id INTEGER PRIMARY KEY,                   -- primary key is good practice
    volume REAL DEFAULT 1.0,                  -- default volume 1.0
    hero_health_bar INTEGER DEFAULT 100,      -- default full health
    hero_mana_bar INTEGER DEFAULT 0,          -- default full mana
    hero_special_bar INTEGER DEFAULT 0,       -- default no special
    text_anti_aliasing INTEGER DEFAULT 0,     -- boolean 1 = True
    smooth_background INTEGER DEFAULT 0,      -- boolean 1 = True
    show_distance INTEGER DEFAULT 0,          -- boolean 0 = False
    show_hitbox INTEGER DEFAULT 0,            -- new boolean column
    show_ground INTEGER DEFAULT 0             -- new boolean column
)
""")
conn2.commit()







def login_check(username):
    cursor.execute(
    "SELECT * FROM users WHERE username = ?",
    (username,)
    )

    user = cursor.fetchone()
    print(user)
    
    
    return user


def register(username, password):
    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )
        conn.commit()
        print("User registered successfully")

        user_id = cursor.lastrowid
        cursor2.execute(
            "INSERT INTO user_info (id) VALUES (?)",
            (user_id,)

        )

        
    except sqlite3.IntegrityError:
        print("Username already exists")

def show_all_user():
    cursor.execute("SELECT * FROM users")
    print(cursor.fetchall())
    
    cursor2.execute("SELECT * FROM user_info")
    print(cursor2.fetchall())
    

def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()


print(cursor.fetchall)