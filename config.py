"""
Configuration file for Furniture Auto Layout
"""
import os
from datetime import timedelta

class Config:
    """Base configuration"""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = False
    TESTING = False
    
    # Model paths
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    MODEL_PATH = os.path.join(BASE_DIR, 'model_auto_layout.pkl')
    FEATURE_COLS_PATH = os.path.join(BASE_DIR, 'feature_columns.pkl')
    METADATA_PATH = os.path.join(BASE_DIR, 'model_metadata.pkl')
    
    # Upload settings
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
    NEWS_UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads', 'news')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'csv', 'xlsx', 'xls'}
    
    # Database settings - Environment variables first, fallback to defaults
    DB_HOST = os.environ.get('DB_HOST', "virtualign.my.id")
    DB_USER = os.environ.get('DB_USER', "virtuali_virtualuser")
    DB_PASSWORD = os.environ.get('DB_PASSWORD', "indra140603")
    DB_NAME = os.environ.get('DB_NAME', "virtuali_virtualign")
    DB_PORT = int(os.environ.get('DB_PORT', 3306))
    
    # Database settings - Local Development (Laragon) - Backup
    # DB_HOST = "localhost"
    # DB_USER = "root"
    # DB_PASSWORD = ""
    # DB_NAME = "virtualtour1"
    # DB_PORT = 3306
    
    # Auth settings
    ADMIN_USERNAME = "admin"
    ADMIN_PASSWORD = "admin123"
    
    # Excel path
    EXCEL_PATH = "LIST FURNITURE.xlsx"
    
    # Canvas settings
    CANVAS_WIDTH = 800
    CANVAS_HEIGHT = 800
    CANVAS_PADDING = 50
    MARGIN = 50  # Canvas margin for furniture placement
    
    # Collision detection
    COLLISION_PADDING = 20
    MAX_COLLISION_ATTEMPTS = 50
    
    # API settings
    API_RATE_LIMIT = "100 per hour"
    API_TIMEOUT = 30  # seconds
    
    # CORS settings
    CORS_ORIGINS = ['http://localhost:3000', 'http://localhost:5000']
    
    # Session settings
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True
    
    # Override with environment variables if available
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'prod-secret-key-please-change'

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config(env=None):
    """Get configuration based on environment"""
    if env is None:
        env = os.environ.get('FLASK_ENV', 'development')
    return config.get(env, config['default'])