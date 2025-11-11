"""
CMS Controller
Menangani CMS content dan theme
"""
from flask import jsonify, request
from app.models.CMS import CMS

class CMSController:
    """Controller untuk CMS endpoints"""
    
    @staticmethod
    def get_content():
        """Get all CMS content"""
        content = CMS.get_all_content()
        return jsonify({
            "status": "success",
            "content": content
        })
    
    @staticmethod
    def update_content():
        """Update CMS content section"""
        data = request.json
        section = data.get("section")
        content = data.get("content")
        
        if not section:
            return jsonify({
                "status": "error",
                "message": "Section is required"
            }), 400
        
        try:
            CMS.upsert_section(section, content)
            all_content = CMS.get_all_content()
            return jsonify({
                "status": "success",
                "content": all_content
            })
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": str(e)
            }), 500
    
    @staticmethod
    def get_theme():
        """Get theme configuration"""
        theme = CMS.get_theme()
        if not theme:
            # Default theme
            theme = {
                "navbarColor": "#0a0a0a",
                "navbarTextColor": "#ffffff",
                "fontFamily": "'Inter', 'Poppins', 'Segoe UI', sans-serif"
            }
        return jsonify({
            "status": "success",
            "theme": theme
        })
    
    @staticmethod
    def update_theme():
        """Update theme"""
        data = request.json.get("theme", {})
        if not data:
            return jsonify({
                "status": "error",
                "message": "Theme object required"
            }), 400
        
        try:
            CMS.upsert_theme(data)
            return jsonify({
                "status": "success",
                "theme": data
            })
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": str(e)
            }), 500
