import pymysql

# Connect to MySQL server
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='database@123'
)

cursor = conn.cursor()

# Create database if it doesn't exist
cursor.execute("CREATE DATABASE IF NOT EXISTS student_erp")
print("✓ Database 'student_erp' created successfully")

cursor.close()
conn.close()
