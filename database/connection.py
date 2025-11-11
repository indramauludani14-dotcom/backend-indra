"""
Database Connection Manager
Mengelola koneksi ke MySQL database
"""
import mysql.connector
from mysql.connector import Error
from config import Config
import os

class Database:
    """Database connection singleton"""
    
    @staticmethod
    def get_connection(database=None):
        """Get MySQL connection with error handling"""
        try:
            cfg = {
                "host": os.environ.get("DB_HOST", Config.DB_HOST),
                "user": os.environ.get("DB_USER", Config.DB_USER),
                "password": os.environ.get("DB_PASSWORD", Config.DB_PASSWORD),
                "autocommit": True,
                "connect_timeout": 10,  # 10 second timeout
            }
            if database:
                cfg["database"] = database
            
            conn = mysql.connector.connect(**cfg)
            return conn
        except Error as e:
            print(f"Database connection error: {e}")
            raise
    
    @staticmethod
    def init_database():
        """Initialize database and tables - safe for Vercel"""
        try:
            # Create database if not exists
            conn = Database.get_connection()
            cursor = conn.cursor()
            
            db_name = os.environ.get("DB_NAME", Config.DB_NAME)
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}` DEFAULT CHARACTER SET 'utf8mb4'")
            cursor.close()
            conn.close()
            
            # Connect to database and create tables
            conn = Database.get_connection(db_name)
            cursor = conn.cursor()
            
            # CMS Content table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS cms_content (
              section VARCHAR(64) PRIMARY KEY,
              content JSON
            ) CHARACTER SET = utf8mb4;
            """)
            
            # Theme table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS theme (
              id INT PRIMARY KEY,
              theme_json JSON
            ) CHARACTER SET = utf8mb4;
            """)
            
            # News table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS news (
              id INT AUTO_INCREMENT PRIMARY KEY,
              title VARCHAR(255),
              excerpt TEXT,
              content TEXT,
              image VARCHAR(255),
              category VARCHAR(100),
              author VARCHAR(100),
              date DATETIME,
              published BOOLEAN DEFAULT TRUE
            ) CHARACTER SET = utf8mb4;
            """)
            
            # Furniture table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS furniture (
              id INT AUTO_INCREMENT PRIMARY KEY,
              nama VARCHAR(255),
              dimensi VARCHAR(255),
              panjang INT,
              lebar INT
            ) CHARACTER SET = utf8mb4;
            """)
            
            # Questions table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS questions (
              id INT AUTO_INCREMENT PRIMARY KEY,
              name VARCHAR(255) NOT NULL,
              email VARCHAR(255) NOT NULL,
              question TEXT NOT NULL,
              answer TEXT,
              status VARCHAR(20) DEFAULT 'pending',
              created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
              answered_at DATETIME,
              answered_by VARCHAR(255)
            ) CHARACTER SET = utf8mb4;
            """)
            
            # FAQ table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS faqs (
              id INT AUTO_INCREMENT PRIMARY KEY,
              category VARCHAR(100) NOT NULL,
              question TEXT NOT NULL,
              answer TEXT NOT NULL,
              is_active BOOLEAN DEFAULT TRUE,
              order_index INT DEFAULT 0,
              created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
              updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            ) CHARACTER SET = utf8mb4;
            """)
            
            # Contact Messages table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS contact_messages (
              id INT AUTO_INCREMENT PRIMARY KEY,
              name VARCHAR(255) NOT NULL,
              email VARCHAR(255) NOT NULL,
              subject VARCHAR(255),
              message TEXT NOT NULL,
              is_read BOOLEAN DEFAULT FALSE,
              created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            ) CHARACTER SET = utf8mb4;
            """)
            
            # House Layouts table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS house_layouts (
              id INT AUTO_INCREMENT PRIMARY KEY,
              user_id INT,
              layout_name VARCHAR(255) NOT NULL,
              layout_data JSON NOT NULL,
              is_public BOOLEAN DEFAULT FALSE,
              thumbnail VARCHAR(255),
              created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
              updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            ) CHARACTER SET = utf8mb4;
            """)
            
            # Social Media table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS social_media (
              id INT AUTO_INCREMENT PRIMARY KEY,
              platform VARCHAR(50) NOT NULL,
              url VARCHAR(255) NOT NULL,
              icon VARCHAR(100),
              is_active BOOLEAN DEFAULT TRUE,
              order_index INT DEFAULT 0
            ) CHARACTER SET = utf8mb4;
            """)
            
            # Activity Logs table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS activity_logs (
              id INT AUTO_INCREMENT PRIMARY KEY,
              user_id INT,
              action VARCHAR(100) NOT NULL,
              entity_type VARCHAR(50),
              entity_id INT,
              description TEXT,
              ip_address VARCHAR(45),
              created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            ) CHARACTER SET = utf8mb4;
            """)
            
            cursor.close()
            conn.close()
            
            print("✓ Database tables created successfully")
            return True
            
        except Error as e:
            print(f"✗ Database initialization error: {e}")
            # Don't crash - let app run without database
            return False
        except Exception as e:
            print(f"✗ Unexpected error during database init: {e}")
            return False
