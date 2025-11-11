"""
HouseLayout Model
For saving user's house layouts
"""
from app.models.BaseModel import BaseModel

class HouseLayout(BaseModel):
    table_name = 'house_layouts'
    
    @classmethod
    def create(cls, user_id, layout_name, house_type, layout_data, thumbnail=None, is_public=0):
        """Create new house layout"""
        import json
        layout_json = json.dumps(layout_data) if isinstance(layout_data, (dict, list)) else layout_data
        
        query = """
            INSERT INTO house_layouts 
            (user_id, layout_name, house_type, layout_data, thumbnail, is_public, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, NOW())
        """
        return cls.execute(query, (user_id, layout_name, house_type, layout_json, thumbnail, is_public))
    
    @classmethod
    def get_all(cls, limit=100):
        """Get all layouts"""
        query = """
            SELECT hl.*, u.username, u.email
            FROM house_layouts hl
            LEFT JOIN users u ON hl.user_id = u.id
            ORDER BY hl.created_at DESC
            LIMIT %s
        """
        return cls.fetch_all(query, (limit,))
    
    @classmethod
    def get_public(cls, limit=50):
        """Get public layouts"""
        query = """
            SELECT hl.*, u.username
            FROM house_layouts hl
            LEFT JOIN users u ON hl.user_id = u.id
            WHERE hl.is_public = 1
            ORDER BY hl.created_at DESC
            LIMIT %s
        """
        return cls.fetch_all(query, (limit,))
    
    @classmethod
    def get_by_user(cls, user_id):
        """Get layouts by user ID"""
        query = """
            SELECT * FROM house_layouts
            WHERE user_id = %s
            ORDER BY created_at DESC
        """
        return cls.fetch_all(query, (user_id,))
    
    @classmethod
    def get_by_id(cls, layout_id):
        """Get layout by ID"""
        query = """
            SELECT hl.*, u.username, u.email
            FROM house_layouts hl
            LEFT JOIN users u ON hl.user_id = u.id
            WHERE hl.id = %s
        """
        return cls.fetch_one(query, (layout_id,))
    
    @classmethod
    def update(cls, layout_id, layout_name, house_type, layout_data, thumbnail=None, is_public=None):
        """Update layout"""
        import json
        layout_json = json.dumps(layout_data) if isinstance(layout_data, (dict, list)) else layout_data
        
        if is_public is not None:
            query = """
                UPDATE house_layouts
                SET layout_name = %s, house_type = %s, layout_data = %s, 
                    thumbnail = %s, is_public = %s, updated_at = NOW()
                WHERE id = %s
            """
            return cls.execute(query, (layout_name, house_type, layout_json, thumbnail, is_public, layout_id))
        else:
            query = """
                UPDATE house_layouts
                SET layout_name = %s, house_type = %s, layout_data = %s, 
                    thumbnail = %s, updated_at = NOW()
                WHERE id = %s
            """
            return cls.execute(query, (layout_name, house_type, layout_json, thumbnail, layout_id))
    
    @classmethod
    def delete(cls, layout_id):
        """Delete layout"""
        query = "DELETE FROM house_layouts WHERE id = %s"
        return cls.execute(query, (layout_id,))
    
    @classmethod
    def toggle_public(cls, layout_id):
        """Toggle public status"""
        query = """
            UPDATE house_layouts
            SET is_public = NOT is_public, updated_at = NOW()
            WHERE id = %s
        """
        return cls.execute(query, (layout_id,))
