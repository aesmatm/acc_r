import sqlite3
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

# MySQL connection settings
mysql_config = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'construction_accounting')
}

def transfer_data():
    # Connect to SQLite database
    sqlite_conn = sqlite3.connect('db.sqlite3')
    sqlite_cursor = sqlite_conn.cursor()
    
    # Connect to MySQL database
    mysql_conn = mysql.connector.connect(**mysql_config)
    mysql_cursor = mysql_conn.cursor()
    
    # Get all tables from SQLite
    sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = sqlite_cursor.fetchall()
    
    for table in tables:
        table_name = table[0]
        print(f"Transferring table: {table_name}")
        
        try:
            # Get data from SQLite
            sqlite_cursor.execute(f"SELECT * FROM {table_name}")
            rows = sqlite_cursor.fetchall()
            
            if rows:
                # Get column names
                sqlite_cursor.execute(f"PRAGMA table_info({table_name})")
                columns = sqlite_cursor.fetchall()
                column_names = [column[1] for column in columns]
                
                # Prepare MySQL insert statement
                placeholders = ', '.join(['%s'] * len(column_names))
                columns_str = ', '.join(column_names)
                insert_query = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"
                
                # Insert data into MySQL
                mysql_cursor.executemany(insert_query, rows)
                mysql_conn.commit()
                
                print(f"Successfully transferred {len(rows)} rows from {table_name}")
        except Exception as e:
            print(f"Error transferring {table_name}: {str(e)}")
            continue
    
    # Close connections
    sqlite_cursor.close()
    sqlite_conn.close()
    mysql_cursor.close()
    mysql_conn.close()

if __name__ == '__main__':
    transfer_data()
