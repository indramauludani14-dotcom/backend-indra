"""
FAQ Model
Mengelola Frequently Asked Questions
"""
from app.models.BaseModel import BaseModel

class FAQ(BaseModel):
    """FAQ model untuk FAQ system"""
    
    table_name = "faqs"
    
    @classmethod
    def get_all(cls):
        """Get all FAQs ordered by display_order"""
        conn = cls.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, category, question, answer, display_order, is_active,
                   DATE_FORMAT(created_at, '%Y-%m-%d %H:%i') as created_at,
                   DATE_FORMAT(updated_at, '%Y-%m-%d %H:%i') as updated_at
            FROM faqs 
            ORDER BY category, display_order ASC
        """)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results
    
    @classmethod
    def get_active(cls):
        """Get only active FAQs"""
        conn = cls.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, category, question, answer, display_order
            FROM faqs 
            WHERE is_active = 1
            ORDER BY category, display_order ASC
        """)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results
    
    @classmethod
    def get_by_category(cls, category):
        """Get FAQs by category"""
        conn = cls.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, question, answer, display_order
            FROM faqs 
            WHERE category = %s AND is_active = 1
            ORDER BY display_order ASC
        """, (category,))
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results
    
    @classmethod
    def create(cls, data):
        """Create new FAQ"""
        conn = cls.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO faqs (category, question, answer, display_order, is_active) 
            VALUES (%s, %s, %s, %s, %s)
        """, (
            data.get('category', 'Umum'),
            data.get('question'),
            data.get('answer'),
            data.get('display_order', 0),
            data.get('is_active', 1)
        ))
        faq_id = cursor.lastrowid
        conn.commit()
        cursor.close()
        conn.close()
        return faq_id
    
    @classmethod
    def update(cls, faq_id, data):
        """Update FAQ"""
        conn = cls.get_connection()
        cursor = conn.cursor()
        
        # Build update query dynamically
        fields = []
        values = []
        
        if 'category' in data:
            fields.append("category = %s")
            values.append(data['category'])
        if 'question' in data:
            fields.append("question = %s")
            values.append(data['question'])
        if 'answer' in data:
            fields.append("answer = %s")
            values.append(data['answer'])
        if 'display_order' in data:
            fields.append("display_order = %s")
            values.append(data['display_order'])
        if 'is_active' in data:
            fields.append("is_active = %s")
            values.append(data['is_active'])
        
        if not fields:
            cursor.close()
            conn.close()
            return False
        
        values.append(faq_id)
        query = f"UPDATE faqs SET {', '.join(fields)} WHERE id = %s"
        
        cursor.execute(query, values)
        affected = cursor.rowcount
        conn.commit()
        cursor.close()
        conn.close()
        return affected > 0
