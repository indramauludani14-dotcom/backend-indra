"""
Furniture Model
Mengelola data furniture
"""
from app.models.BaseModel import BaseModel

class Furniture(BaseModel):
    """Furniture model"""
    
    table_name = "furniture"
    
    @classmethod
    def get_all(cls):
        """Get all furniture"""
        return cls.find_all()
    
    @classmethod
    def get_by_id(cls, furniture_id):
        """Get furniture by ID"""
        return cls.find_by_id(furniture_id)
    
    @classmethod
    def get_by_category(cls, category):
        """Get furniture by category"""
        conn = cls.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM {cls.table_name} WHERE category = %s", (category,))
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results
