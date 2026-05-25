import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

print("Connecting to postgres database to create tutOne...")
conn = psycopg2.connect(
    user='postgres', 
    password='iamgroot', 
    host='localhost', 
    port='5432', 
    database='postgres'
)
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur = conn.cursor()

try:
    cur.execute('CREATE DATABASE "tutOne"')
    print('Database "tutOne" created successfully!')
except Exception as e:
    print(f"Error creating database: {e}")
finally:
    cur.close()
    conn.close()
