import sqlite3

def create_dummy_farmer():
    conn = sqlite3.connect("krishi.db")
    c = conn.cursor()
    
    # Insert a dummy farmer named Ramesh
    try:
        c.execute("""
            INSERT INTO farmers (user_id, name, district, lat_long, soil_details, attributes_json)
            VALUES (
                'farmer_001', 
                'Ramesh Patil', 
                'Nashik', 
                '20.0,73.7', 
                'Black Cotton Soil, pH 7.5, Good drainage', 
                '{}'
            )
        """)
        conn.commit()
        print("Dummy farmer 'Ramesh Patil' added successfully!")
    except sqlite3.IntegrityError:
        print("Dummy farmer already exists.")
        
    conn.close()

if __name__ == "__main__":
    create_dummy_farmer()