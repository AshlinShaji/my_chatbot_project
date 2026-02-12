"""
Database connection and management.
This handles all communication with MySQL.
"""

import mysql.connector
from mysql.connector import Error
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

class DatabaseConnector:
    """
    A class to manage database connections.
    """
    
    def __init__(self):
        """Initialize database connection"""
        self.connection = None
        self.cursor = None
        self.connect()
    
    def connect(self):
        """Create connection to MySQL database."""
        try:
            self.connection = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME
            )
            self.cursor = self.connection.cursor()
            print(f"✅ Connected to {DB_NAME}")
            
        except Error as err:
            if err.errno == 2003:
                print("❌ Cannot connect to MySQL!")
                print("   Make sure MySQL is running")
            elif err.errno == 1049:
                print("❌ Database doesn't exist!")
                print(f"   Create it first")
            else:
                print(f"❌ Database error: {err}")
            
            self.connection = None
    
    def query(self, sql):
        """
        Execute a SELECT query and return results.
        """
        if not self.connection:
            print("❌ Not connected to database!")
            return []
        
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            return results
            
        except Error as err:
            print(f"Query error: {err}")
            return []
    
    def insert_or_update(self, sql, data=None):
        """Execute INSERT or UPDATE statements."""
        if not self.connection:
            print("❌ Not connected to database!")
            return False
        
        try:
            if data:
                self.cursor.execute(sql, data)
            else:
                self.cursor.execute(sql)
            
            self.connection.commit()
            print(f"✅ Query executed. Rows affected: {self.cursor.rowcount}")
            return True
            
        except Error as err:
            print(f"Error: {err}")
            return False
    
    def close(self):
        """Close the database connection"""
        if self.connection:
            self.connection.close()
            print("✅ Database connection closed")

# TEST
if __name__ == "__main__":
    print("Testing database connection...\n")
    
    db = DatabaseConnector()
    
    # Try a simple query
    results = db.query("SHOW TABLES")
    print(f"Tables in database: {results}\n")
    
    db.close()