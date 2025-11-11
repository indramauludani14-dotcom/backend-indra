"""
ActivityLog Model
For logging user activities
"""
from datetime import datetime
from app.models.BaseModel import BaseModel

class ActivityLog(BaseModel):
    table_name = 'activity_logs'
    
    @classmethod
    def create(cls, user_id, action, entity_type=None, entity_id=None, description=None, ip_address=None):
        """Create new activity log"""
        query = """
            INSERT INTO activity_logs (user_id, action, entity_type, entity_id, description, ip_address, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, NOW())
        """
        return cls.execute(query, (user_id, action, entity_type, entity_id, description, ip_address))
    
    @classmethod
    def get_all(cls, limit=100):
        """Get all activity logs"""
        query = """
            SELECT al.*, u.username, u.email
            FROM activity_logs al
            LEFT JOIN users u ON al.user_id = u.id
            ORDER BY al.created_at DESC
            LIMIT %s
        """
        return cls.fetch_all(query, (limit,))
    
    @classmethod
    def get_by_user(cls, user_id, limit=50):
        """Get logs by user"""
        query = """
            SELECT * FROM activity_logs
            WHERE user_id = %s
            ORDER BY created_at DESC
            LIMIT %s
        """
        return cls.fetch_all(query, (user_id, limit))
    
    @classmethod
    def get_by_entity(cls, entity_type, entity_id, limit=50):
        """Get logs by entity"""
        query = """
            SELECT al.*, u.username
            FROM activity_logs al
            LEFT JOIN users u ON al.user_id = u.id
            WHERE al.entity_type = %s AND al.entity_id = %s
            ORDER BY al.created_at DESC
            LIMIT %s
        """
        return cls.fetch_all(query, (entity_type, entity_id, limit))
    
    @classmethod
    def delete_old_logs(cls, days=30):
        """Delete logs older than X days"""
        query = """
            DELETE FROM activity_logs
            WHERE created_at < DATE_SUB(NOW(), INTERVAL %s DAY)
        """
        return cls.execute(query, (days,))
