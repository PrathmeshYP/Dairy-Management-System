import mysql.connector
import bcrypt

print("🔄 Connecting to MySQL...")

try:
    # ✅ Connect to MySQL
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # Add your MySQL root password if needed
        database="dairy_management",
        port=4306,  # Change this if your MySQL uses a different port
        connection_timeout=10  # Optional: prevents the script from hanging indefinitely
    )
    print("✅ Successfully connected to MySQL!")

    # ✅ Create cursor
    cursor = conn.cursor()

    # ✅ Check if 'admin' table exists
    cursor.execute("SHOW TABLES;")
    tables = cursor.fetchall()

    if ("admin",) in tables:
        print("✅ 'admin' table found!")
    else:
        print("⚠️ 'admin' table NOT found! Please check your database setup.")
        exit()

    # ✅ Hash the password
    password = "admin123"
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode('utf-8')

    print(f"🔐 Hashed Password: {hashed_password}")

    # ✅ Delete existing 'admin' user if exists
    cursor.execute("DELETE FROM admin WHERE username = 'admin'")
    print("🗑️ Deleted existing admin user (if any)")

    # ✅ Insert new admin user
    cursor.execute("INSERT INTO admin (username, password_hash) VALUES (%s, %s)", ("admin", hashed_password))
    print("✅ Inserted new admin user")

    # ✅ Commit and close connection
    conn.commit()
    conn.close()
    print("🚀 Admin User Created Successfully!")

except mysql.connector.Error as err:
    print(f"❌ MySQL Error: {err}")
except Exception as e:
    print(f"❌ Unexpected Error: {e}")
