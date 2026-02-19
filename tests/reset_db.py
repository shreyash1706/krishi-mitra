import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import database # This imports your database.py file


def reset():
    if os.path.exists("krishi.db"):
        os.remove("krishi.db")
        print("🗑️ Old database wiped.")
    
    # Rebuild the empty tables
    database.init_db()
    print("✨ Fresh database ready for testing!")

if __name__ == "__main__":
    reset()
