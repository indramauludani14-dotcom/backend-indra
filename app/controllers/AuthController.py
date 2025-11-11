"""
Auth Controller
Menangani authentication
"""
from flask import jsonify, request
from config import Config

class AuthController:
    """Controller untuk authentication"""
    
    @staticmethod
    def login():
        """Admin login"""
        data = request.json or {}
        username = data.get("username")
        password = data.get("password")
        
        if username == Config.ADMIN_USERNAME and password == Config.ADMIN_PASSWORD:
            return jsonify({
                "status": "success",
                "message": "Login successful 🎉",
                "token": "admin-token-123"
            })
        
        return jsonify({
            "status": "error",
            "message": "Invalid credentials"
        }), 401
