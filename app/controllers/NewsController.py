"""
News Controller
Menangani semua request terkait berita
"""
from flask import jsonify, request
from werkzeug.utils import secure_filename
from datetime import datetime
import os
from app.models.News import News
from config import Config

class NewsController:
    """Controller untuk news endpoints"""
    
    @staticmethod
    def allowed_file(filename):
        """Check if file extension is allowed"""
        ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
    @staticmethod
    def index():
        """Get all news"""
        news = News.get_all()
        return jsonify({
            "status": "success",
            "news": news
        })
    
    @staticmethod
    def show(news_id):
        """Get single news by ID"""
        news = News.find_by_id(news_id)
        if news:
            return jsonify({
                "status": "success",
                "news": news
            })
        return jsonify({
            "status": "error",
            "message": "News not found"
        }), 404
    
    @staticmethod
    def store():
        """Create new news"""
        data = request.json or {}
        if not data.get("title"):
            return jsonify({
                "status": "error",
                "message": "Title required"
            }), 400
        
        new_id = News.create(data)
        return jsonify({
            "status": "success",
            "message": "News created",
            "id": new_id
        }), 201
    
    @staticmethod
    def update(news_id):
        """Update news"""
        data = request.json or {}
        success = News.update(news_id, data)
        if success:
            return jsonify({
                "status": "success",
                "message": "News updated"
            })
        return jsonify({
            "status": "error",
            "message": "News not found or no changes made"
        }), 404
    
    @staticmethod
    def destroy(news_id):
        """Delete news"""
        success = News.delete_by_id(news_id)
        if success:
            return jsonify({
                "status": "success",
                "message": "News deleted"
            })
        return jsonify({
            "status": "error",
            "message": "News not found"
        }), 404
    
    @staticmethod
    def upload_image():
        """Upload image for news"""
        try:
            if 'image' not in request.files:
                return jsonify({
                    "status": "error",
                    "message": "No file uploaded"
                }), 400
            
            file = request.files['image']
            
            if file.filename == '':
                return jsonify({
                    "status": "error",
                    "message": "No file selected"
                }), 400
            
            if file and NewsController.allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Add timestamp to make filename unique
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"{timestamp}_{filename}"
                
                # Ensure upload folder exists
                upload_folder = Config.NEWS_UPLOAD_FOLDER
                os.makedirs(upload_folder, exist_ok=True)
                
                filepath = os.path.join(upload_folder, filename)
                file.save(filepath)
                
                # Return URL path
                image_url = f"/static/uploads/news/{filename}"
                return jsonify({
                    "status": "success",
                    "image_url": image_url
                })
            
            return jsonify({
                "status": "error",
                "message": "Invalid file type. Allowed: png, jpg, jpeg, gif, webp"
            }), 400
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": str(e)
            }), 500
