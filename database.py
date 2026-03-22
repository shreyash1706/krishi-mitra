import sqlite3
import json


DB_NAME = "krishi.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    #farmer table for profile info 
    c.execute('''
    CREATE TABLE IF NOT EXISTS farmers
    (
    user_id TEXT PRIMARY KEY,
    name TEXT,
    village TEXT,
    district TEXT,
    lat REAL,
    lon REAL,
    soil_details TEXT,
    attributes_json TEXT
    )'''
    )

    #extracted logic for faster inference and token saving -- contains crop details
    #TODO: implement extraction function and features- will do after MVP
    c.execute('''
    CREATE TABLE IF NOT EXISTS crop_cycles (
        cycle_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT, 
        crop_name TEXT,
        variety TEXT,
        season TEXT,
        year INTEGER,
        sowing_date TEXT,
        status INTEGER CHECK (status IN (0,1)),
        yield TEXT,
        issues_log_json TEXT,
        FOREIGN KEY (user_id) REFERENCES farmers (user_id)
    )''')
    
    #sessions/tabs for different chats 
    c.execute('''
    CREATE TABLE IF NOT EXISTS sessions (
        session_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        agent_mode TEXT,
        title TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES farmers(user_id)
    )''')

    #chat history of each tab 
    #TODO:Create a column for tools used in a query as well 
    c.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id INTEGER,
        role TEXT,
        content TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(session_id) REFERENCES sessions(session_id)
    )''')

    conn.commit()
    conn.close()
    print("Database Initialized")

def get_farmer_context(user_id):
    pass

if __name__ == "__main__":
    init_db()