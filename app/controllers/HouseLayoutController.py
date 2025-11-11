"""
House Layout Controller
Handle user layout saving and retrieval
"""
from flask import request, jsonify
from app.models.HouseLayout import HouseLayout
from app.models.ActivityLog import ActivityLog

class HouseLayoutController:
    
    @staticmethod
    def index():
        """Get all layouts (admin)"""
        try:
            limit = request.args.get('limit', 100, type=int)
            layouts = HouseLayout.get_all(limit)
            return jsonify({
                'status': 'success',
                'data': layouts
            }), 200
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500
    
    @staticmethod
    def get_public():
        """Get public layouts"""
        try:
            limit = request.args.get('limit', 50, type=int)
            layouts = HouseLayout.get_public(limit)
            return jsonify({
                'status': 'success',
                'data': layouts
            }), 200
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500
    
    @staticmethod
    def get_by_user(user_id):
        """Get layouts by user ID"""
        try:
            layouts = HouseLayout.get_by_user(user_id)
            return jsonify({
                'status': 'success',
                'data': layouts
            }), 200
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500
    
    @staticmethod
    def show(layout_id):
        """Get single layout"""
        try:
            layout = HouseLayout.get_by_id(layout_id)
            if not layout:
                return jsonify({
                    'status': 'error',
                    'message': 'Layout not found'
                }), 404
            
            return jsonify({
                'status': 'success',
                'data': layout
            }), 200
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500
    
    @staticmethod
    def store():
        """Save new layout"""
        try:
            data = request.get_json()
            
            # Validation
            if not data.get('user_id') or not data.get('layout_name'):
                return jsonify({
                    'status': 'error',
                    'message': 'user_id and layout_name are required'
                }), 400
            
            layout_id = HouseLayout.create(
                data['user_id'],
                data['layout_name'],
                data.get('house_type', 'Custom'),
                data.get('layout_data', {}),
                data.get('thumbnail'),
                data.get('is_public', 0)
            )
            
            # Log activity
            try:
                ActivityLog.create(
                    user_id=data['user_id'],
                    action='create_layout',
                    entity_type='house_layout',
                    entity_id=layout_id,
                    description=f"Created layout: {data['layout_name']}",
                    ip_address=request.remote_addr
                )
            except:
                pass  # Don't fail if logging fails
            
            return jsonify({
                'status': 'success',
                'message': 'Layout saved successfully',
                'id': layout_id
            }), 201
            
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500
    
    @staticmethod
    def update(layout_id):
        """Update existing layout"""
        try:
            data = request.get_json()
            
            HouseLayout.update(
                layout_id,
                data.get('layout_name'),
                data.get('house_type'),
                data.get('layout_data'),
                data.get('thumbnail'),
                data.get('is_public')
            )
            
            # Log activity
            try:
                if data.get('user_id'):
                    ActivityLog.create(
                        user_id=data['user_id'],
                        action='update_layout',
                        entity_type='house_layout',
                        entity_id=layout_id,
                        description=f"Updated layout: {data.get('layout_name', 'N/A')}",
                        ip_address=request.remote_addr
                    )
            except:
                pass
            
            return jsonify({
                'status': 'success',
                'message': 'Layout updated successfully'
            }), 200
            
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500
    
    @staticmethod
    def toggle_public(layout_id):
        """Toggle public status"""
        try:
            HouseLayout.toggle_public(layout_id)
            return jsonify({
                'status': 'success',
                'message': 'Layout visibility toggled'
            }), 200
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500
    
    @staticmethod
    def destroy(layout_id):
        """Delete layout"""
        try:
            # Get layout info for logging
            layout = HouseLayout.get_by_id(layout_id)
            
            HouseLayout.delete(layout_id)
            
            # Log activity
            try:
                if layout and layout.get('user_id'):
                    ActivityLog.create(
                        user_id=layout['user_id'],
                        action='delete_layout',
                        entity_type='house_layout',
                        entity_id=layout_id,
                        description=f"Deleted layout: {layout.get('layout_name', 'N/A')}",
                        ip_address=request.remote_addr
                    )
            except:
                pass
            
            return jsonify({
                'status': 'success',
                'message': 'Layout deleted successfully'
            }), 200
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500
