"""
Import Database Schema ke Hosting MySQL
Jalankan script ini untuk setup tabel-tabel yang diperlukan
"""
import mysql.connector
from mysql.connector import Error

def import_schema():
    """Import schema ke hosting database"""
    
    # Database connection config
    config = {
        'host': 'virtualign.my.id',
        'user': 'virtuali_virtualuser',
        'password': 'indra140603',
        'database': 'virtuali_virtualign',
        'port': 3306
    }
    
    # SQL schema untuk tabel-tabel yang dibutuhkan
    schema_queries = [
        # Table: furniture
        """
        CREATE TABLE IF NOT EXISTS `furniture` (
          `id` INT NOT NULL AUTO_INCREMENT,
          `name` VARCHAR(255) NOT NULL,
          `category` VARCHAR(100),
          `width` DECIMAL(10,2) NOT NULL,
          `height` DECIMAL(10,2) NOT NULL,
          `depth` DECIMAL(10,2),
          `image_url` VARCHAR(255),
          `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
          `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
          PRIMARY KEY (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """,
        
        # Table: house_layouts
        """
        CREATE TABLE IF NOT EXISTS `house_layouts` (
          `id` INT NOT NULL AUTO_INCREMENT,
          `user_id` INT,
          `layout_name` VARCHAR(100) NOT NULL,
          `room_width` DECIMAL(10,2) NOT NULL,
          `room_height` DECIMAL(10,2) NOT NULL,
          `layout_data` JSON,
          `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
          `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
          PRIMARY KEY (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """,
        
        # Table: news
        """
        CREATE TABLE IF NOT EXISTS `news` (
          `id` INT NOT NULL AUTO_INCREMENT,
          `title` VARCHAR(255) NOT NULL,
          `content` TEXT NOT NULL,
          `image_url` VARCHAR(255),
          `author` VARCHAR(100),
          `published_at` DATETIME,
          `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
          `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
          PRIMARY KEY (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """,
        
        # Table: faqs
        """
        CREATE TABLE IF NOT EXISTS `faqs` (
          `id` INT NOT NULL AUTO_INCREMENT,
          `question` TEXT NOT NULL,
          `answer` TEXT NOT NULL,
          `category` VARCHAR(100),
          `display_order` INT DEFAULT 0,
          `is_active` TINYINT(1) DEFAULT 1,
          `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
          `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
          PRIMARY KEY (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """,
        
        # Table: questions
        """
        CREATE TABLE IF NOT EXISTS `questions` (
          `id` INT NOT NULL AUTO_INCREMENT,
          `name` VARCHAR(100) NOT NULL,
          `email` VARCHAR(100) NOT NULL,
          `question` TEXT NOT NULL,
          `answer` TEXT,
          `status` ENUM('pending', 'answered') DEFAULT 'pending',
          `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
          `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
          PRIMARY KEY (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """,
        
        # Table: contact_messages
        """
        CREATE TABLE IF NOT EXISTS `contact_messages` (
          `id` INT NOT NULL AUTO_INCREMENT,
          `name` VARCHAR(100) NOT NULL,
          `email` VARCHAR(100) NOT NULL,
          `phone` VARCHAR(20),
          `message` TEXT NOT NULL,
          `status` ENUM('new', 'read', 'replied') DEFAULT 'new',
          `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
          PRIMARY KEY (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """,
        
        # Table: cms
        """
        CREATE TABLE IF NOT EXISTS `cms` (
          `id` INT NOT NULL AUTO_INCREMENT,
          `section` VARCHAR(50) NOT NULL,
          `content_key` VARCHAR(100) NOT NULL,
          `content_value` TEXT,
          `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
          `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
          PRIMARY KEY (`id`),
          UNIQUE KEY `section_key` (`section`, `content_key`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """,
        
        # Table: social_media
        """
        CREATE TABLE IF NOT EXISTS `social_media` (
          `id` INT NOT NULL AUTO_INCREMENT,
          `platform` VARCHAR(50) NOT NULL,
          `url` VARCHAR(255) NOT NULL,
          `icon` VARCHAR(100),
          `display_order` INT DEFAULT 0,
          `is_active` TINYINT(1) DEFAULT 1,
          PRIMARY KEY (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """,
        
        # Table: activity_logs
        """
        CREATE TABLE IF NOT EXISTS `activity_logs` (
          `id` INT NOT NULL AUTO_INCREMENT,
          `user_id` VARCHAR(50),
          `action` VARCHAR(100) NOT NULL,
          `target` VARCHAR(255),
          `ip_address` VARCHAR(45),
          `user_agent` TEXT,
          `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
          PRIMARY KEY (`id`),
          INDEX `idx_created_at` (`created_at`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """
    ]
    
    try:
        print("="*60)
        print("IMPORT DATABASE SCHEMA")
        print("="*60)
        print(f"\nConnecting to: {config['host']}/{config['database']}")
        
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        
        print(f"\n✓ Connected successfully")
        print(f"\nCreating tables...")
        
        for i, query in enumerate(schema_queries, 1):
            try:
                cursor.execute(query)
                table_name = query.split('`')[1]
                print(f"  [{i}/{len(schema_queries)}] ✓ Table '{table_name}' created")
            except Error as e:
                if e.errno == 1050:  # Table already exists
                    table_name = query.split('`')[1]
                    print(f"  [{i}/{len(schema_queries)}] ⚠ Table '{table_name}' already exists")
                else:
                    print(f"  [{i}/{len(schema_queries)}] ✗ Error: {e}")
        
        connection.commit()
        
        # Show created tables
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        print(f"\n✓ Schema import completed!")
        print(f"\nTables in database ({len(tables)}):")
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
            count = cursor.fetchone()[0]
            print(f"  - {table[0]}: {count} rows")
        
        cursor.close()
        connection.close()
        
        print("\n" + "="*60)
        print("✓ DATABASE READY TO USE!")
        print("="*60)
        print("\nNext steps:")
        print("1. Jalankan aplikasi: python app.py")
        print("2. Import data furniture jika diperlukan")
        print("3. Setup admin login")
        
        return True
        
    except Error as e:
        print(f"\n✗ Error: {e}")
        return False

if __name__ == "__main__":
    import_schema()
