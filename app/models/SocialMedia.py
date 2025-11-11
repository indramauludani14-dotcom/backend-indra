"""
SocialMedia Model
For managing social media links
"""
from app.models.BaseModel import BaseModel

class SocialMedia(BaseModel):
    table_name = 'social_media'
    
    @classmethod
    def create(cls, platform, platform_name, url, icon, display_order=0):
        """Create new social media link"""
        query = """
            INSERT INTO social_media (platform, platform_name, url, icon, display_order, is_active, created_at)
            VALUES (%s, %s, %s, %s, %s, 1, NOW())
        """
        return cls.execute(query, (platform, platform_name, url, icon, display_order))
    
    @classmethod
    def get_all(cls):
        """Get all social media links"""
        query = """
            SELECT * FROM social_media
            ORDER BY display_order ASC
        """
        return cls.fetch_all(query)
    
    @classmethod
    def get_active(cls):
        """Get active social media links"""
        query = """
            SELECT * FROM social_media
            WHERE is_active = 1
            ORDER BY display_order ASC
        """
        return cls.fetch_all(query)
    
    @classmethod
    def update(cls, social_id, platform, platform_name, url, icon, display_order, is_active):
        """Update social media link"""
        query = """
            UPDATE social_media
            SET platform = %s, platform_name = %s, url = %s, icon = %s,
                display_order = %s, is_active = %s, updated_at = NOW()
            WHERE id = %s
        """
        return cls.execute(query, (platform, platform_name, url, icon, display_order, is_active, social_id))
    
    @classmethod
    def delete(cls, social_id):
        """Delete social media link"""
        query = "DELETE FROM social_media WHERE id = %s"
        return cls.execute(query, (social_id,))
