import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'healthconnect')
}

print("Testing database connection...")
print(f"Config: {DB_CONFIG['user']}@{DB_CONFIG['host']}/{DB_CONFIG['database']}")

try:
    conn = mysql.connector.connect(**DB_CONFIG)
    print("✅ Connected to database!")
    
    cursor = conn.cursor(dictionary=True)
    
    # Check if doctors table exists
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    print(f"\n📋 Tables in database: {[list(t.values())[0] for t in tables]}")
    
    # Check total doctors
    cursor.execute("SELECT COUNT(*) as total FROM doctors")
    result = cursor.fetchone()
    print(f"\n👨‍⚕️ Total doctors: {result['total']}")
    
    # Check dentists specifically
    cursor.execute("""
        SELECT COUNT(*) as total 
        FROM doctors d
        JOIN specialties s ON d.specialty_id = s.specialty_id
        WHERE s.name = 'Dentistry'
    """)
    result = cursor.fetchone()
    print(f"🦷 Total dentists: {result['total']}")
    
    # Show all specialties
    cursor.execute("SELECT specialty_id, name FROM specialties")
    specialties = cursor.fetchall()
    print(f"\n🏥 Specialties in database:")
    for spec in specialties:
        print(f"   - {spec['name']} (ID: {spec['specialty_id']})")
    
    # Show first 3 doctors
    cursor.execute("""
        SELECT 
            d.first_name,
            d.last_name,
            s.name as specialty,
            d.is_active
        FROM doctors d
        JOIN specialties s ON d.specialty_id = s.specialty_id
        LIMIT 3
    """)
    doctors = cursor.fetchall()
    print(f"\n👥 Sample doctors:")
    for doc in doctors:
        print(f"   - {doc['first_name']} {doc['last_name']} ({doc['specialty']}) - Active: {doc['is_active']}")
    
    cursor.close()
    conn.close()
    
except mysql.connector.Error as err:
    print(f"❌ Error: {err}")