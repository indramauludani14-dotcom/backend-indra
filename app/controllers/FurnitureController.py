"""
Furniture Controller
Menangani semua request terkait furniture
"""
from flask import jsonify
from app.models.Furniture import Furniture

class FurnitureController:
    """Controller untuk furniture endpoints"""
    
    @staticmethod
    def index():
        """Get all furniture"""
        furnitures = Furniture.get_all()
        return jsonify({
            "status": "success",
            "count": len(furnitures),
            "data": furnitures
        })
    
    @staticmethod
    def show(furniture_id):
        """Get single furniture by ID"""
        furniture = Furniture.get_by_id(furniture_id)
        if furniture:
            return jsonify({
                "status": "success",
                "data": furniture
            })
        return jsonify({
            "status": "error",
            "message": "Furniture not found"
        }), 404
