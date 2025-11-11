"""
ContactMessage Model
For contact form submissions
"""
from app.models.BaseModel import BaseModel

class ContactMessage(BaseModel):
    table_name = 'contact_messages'
    
    @classmethod
    def create(cls, name, email, subject, message, phone=None):
        """Create new contact message"""
        query = """
            INSERT INTO contact_messages (name, email, phone, subject, message, status, created_at)
            VALUES (%s, %s, %s, %s, %s, 'new', NOW())
        """
        return cls.execute(query, (name, email, phone, subject, message))
    
    @classmethod
    def get_all(cls):
        """Get all contact messages"""
        query = """
            SELECT * FROM contact_messages
            ORDER BY created_at DESC
        """
        return cls.fetch_all(query)
    
    @classmethod
    def get_unread(cls):
        """Get unread messages"""
        query = """
            SELECT * FROM contact_messages
            WHERE status = 'new'
            ORDER BY created_at DESC
        """
        return cls.fetch_all(query)
    
    @classmethod
    def mark_as_read(cls, message_id):
        """Mark message as read"""
        query = """
            UPDATE contact_messages
            SET status = 'read', updated_at = NOW()
            WHERE id = %s
        """
        return cls.execute(query, (message_id,))
    
    @classmethod
    def delete(cls, message_id):
        """Delete message"""
        query = "DELETE FROM contact_messages WHERE id = %s"
        return cls.execute(query, (message_id,))
