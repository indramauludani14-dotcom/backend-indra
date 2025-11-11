"""
FAQ Controller
Menangani semua request terkait FAQ
"""
from flask import jsonify, request
from app.models.FAQ import FAQ

class FAQController:
    """Controller untuk FAQ endpoints"""
    
    @staticmethod
    def index():
        """Get all FAQs (for admin)"""
        faqs = FAQ.get_all()
        return jsonify({
            "status": "success",
            "faqs": faqs
        })
    
    @staticmethod
    def get_active():
        """Get only active FAQs (for public)"""
        faqs = FAQ.get_active()
        return jsonify({
            "status": "success",
            "faqs": faqs
        })
    
    @staticmethod
    def get_by_category(category):
        """Get FAQs by category"""
        faqs = FAQ.get_by_category(category)
        return jsonify({
            "status": "success",
            "category": category,
            "faqs": faqs
        })
    
    @staticmethod
    def show(faq_id):
        """Get single FAQ by ID"""
        faq = FAQ.find_by_id(faq_id)
        if faq:
            return jsonify({
                "status": "success",
                "faq": faq
            })
        return jsonify({
            "status": "error",
            "message": "FAQ not found"
        }), 404
    
    @staticmethod
    def store():
        """Create new FAQ"""
        data = request.json or {}
        if not data.get("question") or not data.get("answer"):
            return jsonify({
                "status": "error",
                "message": "Question and answer are required"
            }), 400
        
        new_id = FAQ.create(data)
        return jsonify({
            "status": "success",
            "message": "FAQ created",
            "id": new_id
        }), 201
    
    @staticmethod
    def update(faq_id):
        """Update FAQ"""
        data = request.json or {}
        success = FAQ.update(faq_id, data)
        if success:
            return jsonify({
                "status": "success",
                "message": "FAQ updated"
            })
        return jsonify({
            "status": "error",
            "message": "FAQ not found or no changes made"
        }), 404
    
    @staticmethod
    def destroy(faq_id):
        """Delete FAQ"""
        success = FAQ.delete_by_id(faq_id)
        if success:
            return jsonify({
                "status": "success",
                "message": "FAQ deleted"
            })
        return jsonify({
            "status": "error",
            "message": "FAQ not found"
        }), 404
