"""
Base Model
Parent class untuk semua models
"""
from database.connection import Database

class BaseModel:
    """Base model dengan helper methods"""
    
    table_name = None
    
    @classmethod
    def get_connection(cls):
        """Get database connection"""
        from config import Config
        return Database.get_connection(Config.DB_NAME)
    
    @classmethod
    def execute(cls, query, params=None):
        """Execute query and return last insert id"""
        conn = cls.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        last_id = cursor.lastrowid
        conn.commit()
        cursor.close()
        conn.close()
        return last_id
    
    @classmethod
    def fetch_all(cls, query, params=None):
        """Fetch all results"""
        conn = cls.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results
    
    @classmethod
    def fetch_one(cls, query, params=None):
        """Fetch single result"""
        conn = cls.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result
    
    @classmethod
    def find_all(cls):
        """Get all records"""
        conn = cls.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM {cls.table_name}")
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results
    
    @classmethod
    def find_by_id(cls, id):
        """Find record by ID"""
        conn = cls.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM {cls.table_name} WHERE id = %s", (id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result
    
    @classmethod
    def delete_by_id(cls, id):
        """Delete record by ID"""
        conn = cls.get_connection()
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM {cls.table_name} WHERE id = %s", (id,))
        affected = cursor.rowcount
        cursor.close()
        conn.close()
        return affected > 0
