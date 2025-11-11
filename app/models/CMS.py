"""
CMS Model
Mengelola CMS content dan theme
"""
import json
from app.models.BaseModel import BaseModel

class CMS(BaseModel):
    """CMS model untuk content dan theme"""
    
    @classmethod
    def get_all_content(cls):
        """Get all CMS content"""
        conn = cls.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT section, content_data FROM cms_content WHERE is_active = 1")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        
        content = {}
        for r in rows:
            # Skip null or empty content
            if r["content_data"] is None:
                continue
                
            try:
                content[r["section"]] = r["content_data"]
                if isinstance(content[r["section"]], str):
                    content[r["section"]] = json.loads(content[r["section"]])
            except Exception:
                try:
                    content[r["section"]] = json.loads(r["content_data"])
                except Exception:
                    content[r["section"]] = r["content_data"]
        return content
    
    @classmethod
    def upsert_section(cls, section, content_obj):
        """Insert or update CMS section"""
        conn = cls.get_connection()
        cursor = conn.cursor()
        
        # Check if section exists
        cursor.execute("SELECT id FROM cms_content WHERE section = %s", (section,))
        existing = cursor.fetchone()
        
        if existing:
            # Update
            cursor.execute("""
                UPDATE cms_content 
                SET content_data = %s, updated_by = 1, updated_at = NOW()
                WHERE section = %s
            """, (json.dumps(content_obj, ensure_ascii=False), section))
        else:
            # Insert
            cursor.execute("""
                INSERT INTO cms_content (section, content_data, created_by, updated_by)
                VALUES (%s, %s, 1, 1)
            """, (section, json.dumps(content_obj, ensure_ascii=False)))
        
        conn.commit()
        cursor.close()
        conn.close()
        return True
    
    @classmethod
    def get_theme(cls):
        """Get theme configuration from cms_content table"""
        conn = cls.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT content_data 
            FROM cms_content 
            WHERE section = 'theme' AND is_active = 1 
            LIMIT 1
        """)
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if row and row.get("content_data"):
            try:
                return row["content_data"] if isinstance(row["content_data"], dict) else json.loads(row["content_data"])
            except Exception:
                try:
                    return json.loads(row["content_data"])
                except:
                    return {}
        return {}
    
    @classmethod
    def upsert_theme(cls, theme_obj):
        """Insert or update theme in cms_content table"""
        return cls.upsert_section('theme', theme_obj)
