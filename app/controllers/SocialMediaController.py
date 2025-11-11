"""
Social Media Controller
Handle social media links management
"""
from flask import request, jsonify
from app.models.SocialMedia import SocialMedia

class SocialMediaController:
    
    @staticmethod
    def index():
        """Get all social media links"""
        try:
            links = SocialMedia.get_all()
            return jsonify({
                'status': 'success',
                'data': links
            }), 200
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500
    
    @staticmethod
    def get_active():
        """Get active social media links"""
        try:
            links = SocialMedia.get_active()
            return jsonify({
                'status': 'success',
                'data': links
            }), 200
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500
    
    @staticmethod
    def store():
        """Create new social media link"""
        try:
            data = request.get_json()
            
            new_id = SocialMedia.create(
                data.get('platform', ''),
                data.get('platform_name', ''),
                data.get('url', ''),
                data.get('icon', ''),
                data.get('display_order', 0)
            )
            
            return jsonify({
                'status': 'success',
                'message': 'Social media link created successfully',
                'id': new_id
            }), 201
            
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500
    
    @staticmethod
    def update(social_id):
        """Update social media link"""
        try:
            data = request.get_json()
            
            SocialMedia.update(
                social_id,
                data.get('platform', ''),
                data.get('platform_name', ''),
                data.get('url', ''),
                data.get('icon', ''),
                data.get('display_order', 0),
                data.get('is_active', 1)
            )
            
            return jsonify({
                'status': 'success',
                'message': 'Social media link updated successfully'
            }), 200
            
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500
    
    @staticmethod
    def destroy(social_id):
        """Delete social media link"""
        try:
            SocialMedia.delete(social_id)
            return jsonify({
                'status': 'success',
                'message': 'Social media link deleted successfully'
            }), 200
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500
