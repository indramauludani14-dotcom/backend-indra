-- ============================================
-- Database Schema - Interior Design AI App
-- Complete with User Management & Admin Panel
-- ============================================

CREATE DATABASE IF NOT EXISTS interior_design_ai 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE interior_design_ai;

-- ============================================
-- TABLE: users (Core Authentication)
-- ============================================

CREATE TABLE `users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(50) NOT NULL,
  `email` VARCHAR(100) NOT NULL,
  `password` VARCHAR(255) NOT NULL COMMENT 'Hashed password (bcrypt)',
  `full_name` VARCHAR(100) NOT NULL,
  `phone` VARCHAR(20),
  
  -- Role & Status
  `role` ENUM('admin', 'user') DEFAULT 'user',
  `is_active` TINYINT(1) DEFAULT 1,
  `email_verified` TINYINT(1) DEFAULT 0,
  
  -- Timestamps
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `last_login` DATETIME,
  
  PRIMARY KEY (`id`),
  UNIQUE INDEX `idx_username` (`username`),
  UNIQUE INDEX `idx_email` (`email`),
  INDEX `idx_role` (`role`),
  INDEX `idx_login` (`email`, `password`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='User accounts - Admin & Regular Users';

-- ============================================
-- TABLE: user_sessions
-- ============================================

CREATE TABLE `user_sessions` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `session_token` VARCHAR(255) NOT NULL,
  `ip_address` VARCHAR(45),
  `user_agent` TEXT,
  `expires_at` DATETIME NOT NULL,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  
  PRIMARY KEY (`id`),
  UNIQUE INDEX `idx_session_token` (`session_token`),
  INDEX `idx_session_user` (`user_id`),
  INDEX `idx_session_expires` (`expires_at`),
  
  CONSTRAINT `fk_session_user`
    FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
    ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='User login sessions';

-- ============================================
-- TABLE: cms
-- ============================================

CREATE TABLE `cms` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `section` VARCHAR(50) NOT NULL,
  `content_key` VARCHAR(100) NOT NULL,
  `content_value` TEXT NOT NULL,
  `content_type` VARCHAR(20) DEFAULT 'text',
  `display_order` INT DEFAULT 0,
  `is_active` TINYINT(1) DEFAULT 1,
  
  -- Tracking
  `created_by` INT,
  `updated_by` INT,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  
  PRIMARY KEY (`id`),
  INDEX `idx_cms_section` (`section`),
  INDEX `idx_cms_key` (`content_key`),
  INDEX `idx_cms_order` (`section`, `display_order`),
  
  CONSTRAINT `fk_cms_created_by` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_cms_updated_by` FOREIGN KEY (`updated_by`) REFERENCES `users` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- TABLE: theme
-- ============================================

CREATE TABLE `theme` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `theme_name` VARCHAR(50) NOT NULL DEFAULT 'default',
  
  `navbar_color` VARCHAR(7) DEFAULT '#0a0a0a',
  `navbar_text_color` VARCHAR(7) DEFAULT '#ffffff',
  `font_family` VARCHAR(100) DEFAULT "'Inter', 'Poppins', 'Segoe UI', sans-serif",
  
  `is_active` TINYINT(1) DEFAULT 1,
  `updated_by` INT,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  
  PRIMARY KEY (`id`),
  INDEX `idx_theme_active` (`is_active`),
  
  CONSTRAINT `fk_theme_updated_by` FOREIGN KEY (`updated_by`) REFERENCES `users` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- TABLE: furniture_categories
-- ============================================

CREATE TABLE `furniture_categories` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(100) NOT NULL,
  `slug` VARCHAR(100) NOT NULL,
  `description` TEXT,
  `icon_url` VARCHAR(255),
  `display_order` INT DEFAULT 0,
  `is_active` TINYINT(1) DEFAULT 1,
  
  `created_by` INT,
  `updated_by` INT,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  
  PRIMARY KEY (`id`),
  UNIQUE INDEX `idx_fcat_slug` (`slug`),
  INDEX `idx_fcat_active` (`is_active`),
  
  CONSTRAINT `fk_fcat_created_by` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_fcat_updated_by` FOREIGN KEY (`updated_by`) REFERENCES `users` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- TABLE: furniture
-- ============================================

CREATE TABLE `furniture` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `category_id` INT NOT NULL,
  
  `name` VARCHAR(255) NOT NULL,
  `slug` VARCHAR(255) NOT NULL,
  `description` TEXT,
  
  -- Dimensions
  `width` DECIMAL(10,2) NOT NULL,
  `height` DECIMAL(10,2) NOT NULL,
  `depth` DECIMAL(10,2) NOT NULL,
  `weight` DECIMAL(10,2),
  
  -- Pricing
  `price` DECIMAL(12,2),
  `currency` VARCHAR(3) DEFAULT 'IDR',
  `discount_percentage` DECIMAL(5,2) DEFAULT 0,
  
  -- Visual
  `image_url` VARCHAR(255),
  `thumbnail_url` VARCHAR(255),
  `model_3d_url` VARCHAR(255),
  
  -- Attributes
  `color` VARCHAR(50),
  `material` VARCHAR(100),
  `style` VARCHAR(50),
  `brand` VARCHAR(100),
  `model_number` VARCHAR(50),
  
  -- Stock
  `stock_quantity` INT DEFAULT 0,
  `is_available` TINYINT(1) DEFAULT 1,
  `is_featured` TINYINT(1) DEFAULT 0,
  
  -- SEO
  `tags` VARCHAR(255),
  `view_count` INT DEFAULT 0,
  
  -- Tracking
  `created_by` INT,
  `updated_by` INT,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  
  PRIMARY KEY (`id`),
  UNIQUE INDEX `idx_furniture_slug` (`slug`),
  INDEX `idx_furniture_cat` (`category_id`),
  INDEX `idx_furniture_available` (`is_available`),
  
  CONSTRAINT `fk_furniture_category` FOREIGN KEY (`category_id`) REFERENCES `furniture_categories` (`id`) ON DELETE RESTRICT,
  CONSTRAINT `fk_furniture_created_by` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_furniture_updated_by` FOREIGN KEY (`updated_by`) REFERENCES `users` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- TABLE: user_rooms
-- ============================================

CREATE TABLE `user_rooms` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  
  `room_name` VARCHAR(100) NOT NULL,
  `room_type` ENUM('bedroom', 'living_room', 'kitchen', 'bathroom', 'office', 'other') DEFAULT 'bedroom',
  
  `width` DECIMAL(10,2) NOT NULL,
  `length` DECIMAL(10,2) NOT NULL,
  `height` DECIMAL(10,2) DEFAULT 3.0,
  
  `description` TEXT,
  `is_public` TINYINT(1) DEFAULT 0,
  
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  
  PRIMARY KEY (`id`),
  INDEX `idx_room_user` (`user_id`),
  INDEX `idx_room_type` (`room_type`),
  
  CONSTRAINT `fk_room_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- TABLE: user_layouts
-- ============================================

CREATE TABLE `user_layouts` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `room_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  
  `layout_name` VARCHAR(100) NOT NULL,
  `layout_data` JSON,
  `thumbnail_url` VARCHAR(255),
  
  `style` VARCHAR(50),
  `color_scheme` VARCHAR(50),
  `budget_range` ENUM('low', 'medium', 'high', 'luxury'),
  
  `is_favorite` TINYINT(1) DEFAULT 0,
  `is_public` TINYINT(1) DEFAULT 0,
  
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  
  PRIMARY KEY (`id`),
  INDEX `idx_layout_room` (`room_id`),
  INDEX `idx_layout_user` (`user_id`),
  INDEX `idx_user_favorites` (`user_id`, `is_favorite`),
  
  CONSTRAINT `fk_layout_room` FOREIGN KEY (`room_id`) REFERENCES `user_rooms` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_layout_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- TABLE: layout_furniture
-- ============================================

CREATE TABLE `layout_furniture` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `layout_id` INT NOT NULL,
  `furniture_id` INT NOT NULL,
  
  `position_x` DECIMAL(10,2) NOT NULL,
  `position_y` DECIMAL(10,2) NOT NULL,
  `rotation` DECIMAL(10,2) DEFAULT 0,
  
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  
  PRIMARY KEY (`id`),
  INDEX `idx_lf_layout` (`layout_id`),
  INDEX `idx_lf_furniture` (`furniture_id`),
  
  CONSTRAINT `fk_lf_layout` FOREIGN KEY (`layout_id`) REFERENCES `user_layouts` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_lf_furniture` FOREIGN KEY (`furniture_id`) REFERENCES `furniture` (`id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- TABLE: news_categories
-- ============================================

CREATE TABLE `news_categories` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(100) NOT NULL,
  `slug` VARCHAR(100) NOT NULL,
  `description` TEXT,
  `display_order` INT DEFAULT 0,
  `is_active` TINYINT(1) DEFAULT 1,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  
  PRIMARY KEY (`id`),
  UNIQUE INDEX `idx_ncat_slug` (`slug`),
  INDEX `idx_ncat_active` (`is_active`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- TABLE: news
-- ============================================

CREATE TABLE `news` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `category_id` INT,
  `author_id` INT,
  
  `title` VARCHAR(255) NOT NULL,
  `slug` VARCHAR(255) NOT NULL,
  `excerpt` TEXT,
  `content` TEXT NOT NULL,
  
  `image_url` VARCHAR(255),
  `thumbnail_url` VARCHAR(255),
  
  -- SEO
  `meta_title` VARCHAR(255),
  `meta_description` TEXT,
  `meta_keywords` VARCHAR(255),
  
  -- Status
  `status` ENUM('draft', 'published', 'archived') DEFAULT 'draft',
  `is_featured` TINYINT(1) DEFAULT 0,
  `published_at` DATETIME,
  
  `view_count` INT DEFAULT 0,
  
  -- Tracking
  `created_by` INT,
  `updated_by` INT,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  
  PRIMARY KEY (`id`),
  UNIQUE INDEX `idx_news_slug` (`slug`),
  INDEX `idx_news_cat` (`category_id`),
  INDEX `idx_news_author` (`author_id`),
  INDEX `idx_news_status` (`status`),
  INDEX `idx_published` (`status`, `published_at`),
  
  CONSTRAINT `fk_news_category` FOREIGN KEY (`category_id`) REFERENCES `news_categories` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_news_author` FOREIGN KEY (`author_id`) REFERENCES `users` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_news_created_by` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_news_updated_by` FOREIGN KEY (`updated_by`) REFERENCES `users` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- TABLE: faq_categories
-- ============================================

CREATE TABLE `faq_categories` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(100) NOT NULL,
  `slug` VARCHAR(100) NOT NULL,
  `description` TEXT,
  `icon` VARCHAR(100),
  `display_order` INT DEFAULT 0,
  `is_active` TINYINT(1) DEFAULT 1,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  
  PRIMARY KEY (`id`),
  UNIQUE INDEX `idx_faqcat_slug` (`slug`),
  INDEX `idx_faqcat_active` (`is_active`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- TABLE: faqs
-- ============================================

CREATE TABLE `faqs` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `category_id` INT,
  
  `question` TEXT NOT NULL,
  `answer` TEXT NOT NULL,
  
  `display_order` INT DEFAULT 0,
  `is_active` TINYINT(1) DEFAULT 1,
  
  `view_count` INT DEFAULT 0,
  `helpful_count` INT DEFAULT 0,
  `not_helpful_count` INT DEFAULT 0,
  
  `created_by` INT,
  `updated_by` INT,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  
  PRIMARY KEY (`id`),
  INDEX `idx_faq_cat` (`category_id`),
  INDEX `idx_faq_active` (`is_active`),
  
  CONSTRAINT `fk_faq_category` FOREIGN KEY (`category_id`) REFERENCES `faq_categories` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_faq_created_by` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_faq_updated_by` FOREIGN KEY (`updated_by`) REFERENCES `users` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- TABLE: questions
-- ============================================

CREATE TABLE `questions` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT,
  
  `name` VARCHAR(100) NOT NULL,
  `email` VARCHAR(100) NOT NULL,
  
  `question` TEXT NOT NULL,
  `category_id` INT,
  
  `answer` TEXT,
  `answered_by` INT,
  `answered_at` DATETIME,
  
  `status` ENUM('pending', 'answered', 'closed') DEFAULT 'pending',
  `is_public` TINYINT(1) DEFAULT 0,
  
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  
  PRIMARY KEY (`id`),
  INDEX `idx_q_user` (`user_id`),
  INDEX `idx_q_answered_by` (`answered_by`),
  INDEX `idx_q_status` (`status`),
  INDEX `idx_pending_q` (`status`, `created_at`),
  
  CONSTRAINT `fk_question_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_question_category` FOREIGN KEY (`category_id`) REFERENCES `faq_categories` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_question_answered_by` FOREIGN KEY (`answered_by`) REFERENCES `users` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- TABLE: contact_messages
-- ============================================

CREATE TABLE `contact_messages` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT,
  
  `name` VARCHAR(100) NOT NULL,
  `email` VARCHAR(100) NOT NULL,
  `phone` VARCHAR(20),
  
  `subject` VARCHAR(255) NOT NULL,
  `message` TEXT NOT NULL,
  
  `status` ENUM('new', 'read', 'replied', 'closed') DEFAULT 'new',
  
  `reply` TEXT,
  `replied_by` INT,
  `replied_at` DATETIME,
  
  `ip_address` VARCHAR(45),
  `user_agent` TEXT,
  
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  
  PRIMARY KEY (`id`),
  INDEX `idx_contact_user` (`user_id`),
  INDEX `idx_contact_replied_by` (`replied_by`),
  INDEX `idx_contact_status` (`status`),
  
  CONSTRAINT `fk_contact_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_contact_replied_by` FOREIGN KEY (`replied_by`) REFERENCES `users` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- TABLE: activity_logs
-- ============================================

CREATE TABLE `activity_logs` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  
  `action` VARCHAR(100) NOT NULL,
  `entity_type` VARCHAR(50),
  `entity_id` INT,
  
  `description` TEXT,
  `ip_address` VARCHAR(45),
  `user_agent` TEXT,
  
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  
  PRIMARY KEY (`id`),
  INDEX `idx_log_user` (`user_id`),
  INDEX `idx_log_entity` (`entity_type`),
  INDEX `idx_log_time` (`created_at`),
  
  CONSTRAINT `fk_log_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Activity logs for audit trail';

-- ============================================
-- INITIAL DATA
-- ============================================

-- Default Admin User (password: admin123)
INSERT INTO `users` (`username`, `email`, `password`, `full_name`, `role`, `is_active`, `email_verified`) VALUES
('admin', 'admin@interior.ai', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqYGYqYGYq', 'System Administrator', 'admin', 1, 1);

-- Default Theme
INSERT INTO `theme` (`theme_name`, `is_active`) VALUES ('default', 1);

-- Sample CMS Content
INSERT INTO `cms` (`section`, `content_key`, `content_value`, `content_type`, `display_order`, `created_by`) VALUES
('hero', 'hero_title', 'Design Your Dream Space with AI', 'text', 1, 1),
('hero', 'hero_subtitle', 'Transform your living space with intelligent interior design', 'text', 2, 1),
('hero', 'hero_button_text', 'Get Started', 'text', 3, 1);

-- Sample Furniture Categories
INSERT INTO `furniture_categories` (`name`, `slug`, `description`, `display_order`, `created_by`) VALUES
('Living Room', 'living-room', 'Furniture untuk ruang tamu', 1, 1),
('Bedroom', 'bedroom', 'Furniture untuk kamar tidur', 2, 1),
('Dining Room', 'dining-room', 'Furniture untuk ruang makan', 3, 1);

-- Sample FAQ Categories
INSERT INTO `faq_categories` (`name`, `slug`, `description`, `icon`, `display_order`) VALUES
('Getting Started', 'getting-started', 'Panduan memulai', '🚀', 1),
('Features', 'features', 'Tentang fitur aplikasi', '⭐', 2);

-- ============================================
-- END OF SCHEMA
-- ============================================
