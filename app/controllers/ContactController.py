"""
Contact Controller
Handle contact form submissions
"""
from flask import request, jsonify
from app.models.ContactMessage import ContactMessage

class ContactController:
    
    @staticmethod
    def index():
        """Get all contact messages"""
        try:
            messages = ContactMessage.get_all()
            return jsonify({
                'status': 'success',
                'data': messages
            }), 200
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500
    
    @staticmethod
    def get_unread():
        """Get unread messages"""
        try:
            messages = ContactMessage.get_unread()
            return jsonify({
                'status': 'success',
                'data': messages
            }), 200
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500
    
    @staticmethod
    def store():
        """Submit new contact message"""
        try:
            data = request.get_json()
            
            # Validation
            if not all(k in data for k in ['name', 'email', 'subject', 'message']):
                return jsonify({
                    'status': 'error',
                    'message': 'Missing required fields'
                }), 400
            
            # Create message
            ContactMessage.create(
                data['name'],
                data['email'],
                data['subject'],
                data['message']
            )
            
            return jsonify({
                'status': 'success',
                'message': 'Contact message sent successfully'
            }), 201
            
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500
    
    @staticmethod
    def mark_read(message_id):
        """Mark message as read"""
        try:
            ContactMessage.mark_as_read(message_id)
            return jsonify({
                'status': 'success',
                'message': 'Message marked as read'
            }), 200
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500
    
    @staticmethod
    def destroy(message_id):
        """Delete contact message"""
        try:
            ContactMessage.delete(message_id)
            return jsonify({
                'status': 'success',
                'message': 'Message deleted successfully'
            }), 200
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500
