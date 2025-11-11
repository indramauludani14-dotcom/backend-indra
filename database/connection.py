"""
Database Connection Manager
Mengelola koneksi ke MySQL database
"""
import mysql.connector
from config import Config

class Database:
    """Database connection singleton"""
    
    @staticmethod
    def get_connection(database=None):
        """Get MySQL connection"""
        cfg = {
            "host": Config.DB_HOST,
            "user": Config.DB_USER,
            "password": Config.DB_PASSWORD,
            "autocommit": True,
        }
        if database:
            cfg["database"] = database
        return mysql.connector.connect(**cfg)
    
    @staticmethod
    def init_database():
        """Initialize database and tables"""
        # Create database if not exists
        conn = Database.get_connection()
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{Config.DB_NAME}` DEFAULT CHARACTER SET 'utf8mb4'")
        cursor.close()
        conn.close()
        
        # Connect to database and create tables
        conn = Database.get_connection(Config.DB_NAME)
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
        
        cursor.close()
        conn.close()
        
        return True
