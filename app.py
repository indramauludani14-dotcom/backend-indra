from flask import Flask
from flask_cors import CORS
import os

# Import configuration
from config import Config

# Import database
from database.connection import Database

# Import routes
from routes.api import api

# ===== FLASK APP INITIALIZATION =====
app = Flask(__name__)
CORS(app, supports_credentials=True)

# Load configuration
app.config["SECRET_KEY"] = Config.SECRET_KEY
app.config["UPLOAD_FOLDER"] = Config.UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = Config.MAX_CONTENT_LENGTH

# Ensure upload directory exists
os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)

# ===== INITIALIZE DATABASE =====
try:
    Database.init_database()
    print(" Database initialized successfully")
except Exception as e:
    print(f" DB init skipped: {e}")

# ===== REGISTER BLUEPRINTS (ROUTES) =====
app.register_blueprint(api)

# ===== LEGACY ROUTES (BACKWARD COMPATIBILITY) =====
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

# ===== MAIN =====
if __name__ == "__main__":
    print("=" * 60)
    print(" FurniLayout API Server")
    print("=" * 60)
    print(" Running at: http://localhost:5000")
    print(" API Status: http://localhost:5000/api/status")
    print(" Documentation: See BACKEND_STRUCTURE.md")
    print("=" * 60)
    print()
    app.run(debug=True, host="0.0.0.0", port=5000)
