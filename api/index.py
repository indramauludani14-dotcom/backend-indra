"""
Vercel Serverless Function Entry Point
"""
from flask import Flask, jsonify
from flask_cors import CORS
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

try:
    # Import configuration
    from config import Config
    
    # Import routes
    from routes.api import api
    
    # ===== FLASK APP INITIALIZATION =====
    app = Flask(__name__)
    CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": "*"}})
    
    # Load configuration
    app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY', Config.SECRET_KEY)
    app.config["UPLOAD_FOLDER"] = Config.UPLOAD_FOLDER
    app.config["MAX_CONTENT_LENGTH"] = Config.MAX_CONTENT_LENGTH
    
    # ===== INITIALIZE DATABASE (Optional) =====
    try:
        from database.connection import Database
        Database.init_database()
        print("✓ Database initialized")
    except Exception as db_error:
        print(f"⚠ DB init skipped: {db_error}")
        # Continue without database - some endpoints will work
    
    # ===== REGISTER BLUEPRINTS (ROUTES) =====
    app.register_blueprint(api)
    
    # ===== LEGACY ROUTES (BACKWARD COMPATIBILITY) =====
    try:
        from app.controllers.LayoutController import LayoutController
        
        @app.route('/predict_batch', methods=['POST'])
        def legacy_predict():
            """Legacy endpoint for prediction"""
            return LayoutController.predict_batch()
        
        @app.route('/get_floor_recommendations', methods=['POST'])
        def legacy_recommendations():
            """Legacy endpoint for floor recommendations"""
            return LayoutController.get_floor_recommendations()
        
        @app.route('/reset', methods=['POST'])
        def legacy_reset():
            """Legacy endpoint for reset"""
            return LayoutController.reset_layout()
        
        @app.route('/static/uploads/news/<filename>')
        def legacy_serve_image(filename):
            """Legacy endpoint for serving images"""
            return LayoutController.serve_news_image(filename)
    except Exception as legacy_error:
        print(f"⚠ Legacy routes skipped: {legacy_error}")
    
    # ===== ROOT ENDPOINT =====
    @app.route('/')
    def index():
        """Root endpoint"""
        return jsonify({
            "status": "success",
            "service": "FurniLayout API",
            "version": "2.0.0",
            "message": "Backend is running on Vercel",
            "endpoints": {
                "status": "/api/status",
                "news": "/api/news",
                "faqs": "/api/faqs",
                "contact": "/api/contact",
                "cms": "/api/cms/content",
                "furniture": "/api/furniture",
                "layouts": "/api/layouts"
            }
        })
    
    # ===== ERROR HANDLERS =====
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "status": "error",
            "message": "Endpoint not found",
            "code": 404
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            "status": "error",
            "message": "Internal server error",
            "code": 500,
            "detail": str(error)
        }), 500
    
    print("✓ Flask app initialized successfully")

except Exception as init_error:
    print(f"✗ CRITICAL ERROR during app initialization: {init_error}")
    import traceback
    traceback.print_exc()
    
    # Create minimal fallback app
    app = Flask(__name__)
    CORS(app)
    
    @app.route('/')
    @app.route('/api/status')
    def error_status():
        return jsonify({
            "status": "error",
            "message": "Backend initialization failed",
            "error": str(init_error)
        }), 500

# Export for Vercel
handler = app
