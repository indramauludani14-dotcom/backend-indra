"""
News Model
Mengelola data berita/artikel
"""
from app.models.BaseModel import BaseModel

class News(BaseModel):
    """News model"""
    
    table_name = "news"
    
    @classmethod
    def get_all(cls):
        """Get all news articles ordered by date"""
        conn = cls.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"""
            SELECT id, title, excerpt, content, image, category, author, 
                   DATE_FORMAT(date, '%Y-%m-%d') as date, published 
            FROM {cls.table_name} 
            ORDER BY date DESC
        """)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results
    
    @classmethod
    def get_published(cls):
        """Get only published news"""
        conn = cls.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"""
            SELECT id, title, excerpt, content, image, category, author,
                   DATE_FORMAT(date, '%Y-%m-%d') as date, published
            FROM {cls.table_name}
            WHERE published = TRUE
            ORDER BY date DESC
        """)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results
    
    @classmethod
    def create(cls, data):
        """Create new news article"""
        conn = cls.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO news (title, excerpt, content, image, category, author, date, published)
            VALUES (%s, %s, %s, %s, %s, %s, NOW(), %s)
        """, (
            data.get('title'),
            data.get('excerpt', ''),
            data.get('content', ''),
            data.get('image', ''),
            data.get('category', 'General'),
            data.get('author', 'Admin'),
            data.get('published', True)
        ))
        new_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return new_id
    
    @classmethod
    def update(cls, news_id, data):
        """Update news article"""
        fields = []
        values = []
        for k in ("title", "excerpt", "content", "image", "category", "author", "published"):
            if k in data:
                fields.append(f"{k} = %s")
                values.append(data[k])
        
        if not fields:
            return False
        
        values.append(news_id)
        conn = cls.get_connection()
        cursor = conn.cursor()
        cursor.execute(f"UPDATE {cls.table_name} SET {', '.join(fields)} WHERE id = %s", tuple(values))
        affected = cursor.rowcount
        cursor.close()
        conn.close()
        return affected > 0
