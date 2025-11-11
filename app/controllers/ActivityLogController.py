"""
Activity Log Controller
Handle activity logging and retrieval
"""
from flask import request, jsonify
from app.models.ActivityLog import ActivityLog

class ActivityLogController:
    
    @staticmethod
    def index():
        """Get all activity logs (admin)"""
        try:
            limit = request.args.get('limit', 100, type=int)
            logs = ActivityLog.get_all(limit)
            return jsonify({
                'status': 'success',
                'data': logs
            }), 200
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500
    
    @staticmethod
    def get_by_user(user_id):
        """Get logs by user"""
        try:
            limit = request.args.get('limit', 50, type=int)
            logs = ActivityLog.get_by_user(user_id, limit)
            return jsonify({
                'status': 'success',
                'data': logs
            }), 200
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500
    
    @staticmethod
    def get_by_entity(entity_type, entity_id):
        """Get logs by entity"""
        try:
            limit = request.args.get('limit', 50, type=int)
            logs = ActivityLog.get_by_entity(entity_type, entity_id, limit)
            return jsonify({
                'status': 'success',
                'data': logs
            }), 200
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500
    
    @staticmethod
    def cleanup():
        """Delete old logs"""
        try:
            days = request.args.get('days', 30, type=int)
            ActivityLog.delete_old_logs(days)
            return jsonify({
                'status': 'success',
                'message': f'Logs older than {days} days deleted'
            }), 200
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500
