import mysql.connector

print("🔄 Connecting to MySQL...")

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # Replace with your actual MySQL password
        database="dairy_management",
        port=4306,  # Change to the correct MySQL port
        connection_timeout=10  # Prevents script from hanging indefinitely
    )
    print("✅ Successfully connected to MySQL!")

    # Check if the `admin` table exists
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES;")
    tables = cursor.fetchall()

    if ("admin",) in tables:
        print("✅ 'admin' table found!")
    else:
        print("⚠️ 'admin' table NOT found! Please check your database setup.")

    conn.close()
except mysql.connector.Error as err:
    print(f"❌ Connection failed: {err}")
except Exception as e:
    print(f"❌ Unexpected error: {e}")
