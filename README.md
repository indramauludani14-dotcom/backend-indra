# FurniLayout Backend API

Backend API untuk aplikasi Virtual Tour & Furniture Layout System menggunakan Flask dan MySQL.

## 📋 Daftar Isi

- [Teknologi](#teknologi)
- [Struktur Project](#struktur-project)
- [Setup & Installation](#setup--installation)
- [API Endpoints](#api-endpoints)
- [Component Documentation](#component-documentation)
- [Database Schema](#database-schema)
- [Configuration](#configuration)

---

## 🛠 Teknologi

- **Python 3.x**
- **Flask** - Web framework
- **MySQL** - Database
- **Joblib/Scikit-learn** - Machine Learning model
- **Pandas & NumPy** - Data processing
- **Flask-CORS** - Cross-Origin Resource Sharing

---

## 📁 Struktur Project

```
TA/
├── app.py                      # Main application entry point
├── config.py                   # Configuration file
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git ignore file
│
├── app/
│   ├── __init__.py
│   ├── controllers/            # Request handlers
│   │   ├── AuthController.py
│   │   ├── CMSController.py
│   │   ├── FurnitureController.py
│   │   ├── LayoutController.py
│   │   ├── NewsController.py
│   │   └── QuestionController.py
│   │
│   ├── models/                 # Database models
│   │   ├── BaseModel.py
│   │   ├── CMS.py
│   │   ├── Furniture.py
│   │   ├── News.py
│   │   └── Question.py
│   │
│   └── services/               # Business logic
│       └── LayoutService.py
│
├── database/
│   ├── connection.py           # Database connection manager
│   └── schema_official.sql     # Database schema
│
├── routes/
│   └── api.py                  # API route definitions
│
├── static/
│   └── uploads/
│       └── news/               # Uploaded news images
│
└── frontend/                   # React frontend (separate)
```

---

## 🚀 Setup & Installation

### 1. Prerequisites

- Python 3.8+
- MySQL Server (via Laragon/XAMPP/Standalone)
- Node.js (untuk frontend)

### 2. Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt
```

### 3. Database Setup

1. **Start MySQL Server** (Laragon):
   - Buka Laragon
   - Klik "Start All"
   - MySQL akan berjalan di `localhost:3306`

2. **Database akan otomatis dibuat** saat pertama kali run aplikasi

### 4. Configuration

Edit `config.py` jika perlu mengubah:
- Database credentials
- Upload folder path
- Admin username/password
- API settings

### 5. Run Application

```bash
python app.py
```

Server akan berjalan di: `http://localhost:5000`

---

## 📡 API Endpoints

### Status

#### GET `/api/status`
Cek status API server

**Response:**
```json
{
  "status": "success",
  "service": "FurniLayout API",
  "version": "2.0.0"
}
```

---

### 🪑 Furniture Endpoints

#### GET `/api/furnitures`
Get semua furniture

**Response:**
```json
{
  "status": "success",
  "count": 50,
  "data": [
    {
      "id": 1,
      "nama": "Sofa Modern",
      "dimensi": "200x90",
      "panjang": 200,
      "lebar": 90
    }
  ]
}
```

#### GET `/api/furnitures/:id`
Get detail furniture by ID

---

### 📰 News Endpoints

#### GET `/api/news`
Get semua berita

**Response:**
```json
{
  "status": "success",
  "news": [
    {
      "id": 1,
      "title": "New Furniture Collection",
      "excerpt": "Check our latest collection...",
      "content": "Full article content...",
      "image": "http://localhost:5000/static/uploads/news/image.jpg",
      "category": "Product",
      "author": "Admin",
      "date": "2025-10-25 10:00:00",
      "published": true
    }
  ]
}
```

#### GET `/api/news/:id`
Get detail berita

#### POST `/api/news`
Create berita baru

**Body:**
```json
{
  "title": "News Title",
  "excerpt": "Short description",
  "content": "Full content",
  "image": "image_url",
  "category": "Product",
  "author": "Admin"
}
```

#### PUT `/api/news/:id`
Update berita

#### DELETE `/api/news/:id`
Hapus berita

---

### 🎨 CMS Endpoints

#### GET `/api/cms/content`
Get semua CMS content (About, Contact, FAQ, dll)

**Response:**
```json
{
  "status": "success",
  "content": {
    "about": {
      "title": "About Us",
      "description": "We are...",
      "mission": "Our mission..."
    },
    "contact": {
      "email": "info@example.com",
      "phone": "+62123456789",
      "address": "Jakarta, Indonesia"
    }
  }
}
```

#### PUT `/api/cms/content`
Update CMS content section

**Body:**
```json
{
  "section": "about",
  "content": {
    "title": "About Us",
    "description": "Updated description"
  }
}
```

#### GET `/api/cms/theme`
Get theme configuration

**Response:**
```json
{
  "status": "success",
  "theme": {
    "colors": {
      "primary": "#667eea",
      "secondary": "#764ba2",
      "accent": "#f093fb",
      "text": "#333333",
      "background": "#ffffff"
    },
    "fontFamily": "Segoe UI, sans-serif"
  }
}
```

#### PUT `/api/cms/theme`
Update theme

**Body:**
```json
{
  "theme": {
    "colors": {
      "primary": "#667eea",
      "secondary": "#764ba2"
    },
    "fontFamily": "Arial, sans-serif"
  }
}
```

---

### ❓ Q&A Endpoints

#### POST `/api/questions`
Submit pertanyaan baru (public)

**Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "question": "How to use the layout tool?"
}
```

#### GET `/api/questions/answered`
Get pertanyaan yang sudah dijawab (public)

**Response:**
```json
{
  "status": "success",
  "data": [
    {
      "id": 1,
      "name": "John Doe",
      "email": "john@example.com",
      "question": "How to use?",
      "answer": "You can start by...",
      "status": "answered",
      "created_at": "2025-10-25 10:00:00",
      "answered_at": "2025-10-25 11:00:00",
      "answered_by": "Admin"
    }
  ],
  "total": 5
}
```

#### GET `/api/questions/all`
Get semua pertanyaan (admin only)

**Response:**
```json
{
  "status": "success",
  "data": [...],
  "summary": {
    "total": 10,
    "pending": 3,
    "answered": 7
  }
}
```

#### PUT `/api/questions/:id/answer`
Jawab pertanyaan (admin only)

**Body:**
```json
{
  "answer": "Thank you for your question...",
  "answered_by": "Admin"
}
```

#### DELETE `/api/questions/:id`
Hapus pertanyaan

---

### 🔐 Auth Endpoints

#### POST `/api/cms/login`
Admin login

**Body:**
```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Login successful 🎉",
  "token": "admin-token-123"
}
```

---

### 🏗️ Layout Prediction Endpoints

#### POST `/api/layout/predict`
Predict posisi furniture menggunakan ML model

**Body:**
```json
{
  "items": [
    {
      "id": 1,
      "name": "Sofa",
      "panjang": 200,
      "lebar": 90
    },
    {
      "id": 2,
      "name": "Coffee Table",
      "panjang": 100,
      "lebar": 60
    }
  ],
  "room_type": "living_room",
  "floor_data": {
    "rooms": [...],
    "obstacles": [...]
  }
}
```

**Response:**
```json
{
  "status": "success",
  "data": [
    {
      "id": 1,
      "name": "Sofa",
      "x": 150,
      "y": 200,
      "panjang": 200,
      "lebar": 90,
      "placed": true
    },
    {
      "id": 2,
      "name": "Coffee Table",
      "x": 250,
      "y": 350,
      "panjang": 100,
      "lebar": 60,
      "placed": true
    }
  ],
  "room_type": "living_room",
  "total_placed": 2,
  "model_used": true
}
```

#### POST `/api/layout/recommendations`
Get rekomendasi furniture untuk lantai tertentu

**Body:**
```json
{
  "floor": 1,
  "floor_data": {}
}
```

#### POST `/api/layout/reset`
Reset layout

---

### 📤 Upload Endpoints

#### POST `/api/news/upload-image`
Upload gambar untuk berita

**Form Data:**
- `image`: File (png, jpg, jpeg, gif, webp)

**Response:**
```json
{
  "status": "success",
  "image_url": "http://localhost:5000/static/uploads/news/20251025_120000_image.jpg"
}
```

#### GET `/api/news/images/:filename`
Serve uploaded image

---

## 📦 Component Documentation

### Controllers

Controllers menangani HTTP requests dan responses.

#### 1. **AuthController**
- `login()` - Handle admin authentication
- Simple hardcoded authentication via config

#### 2. **CMSController**
- `get_content()` - Get all CMS content
- `update_content()` - Update specific section
- `get_theme()` - Get theme configuration
- `update_theme()` - Update theme colors & fonts

#### 3. **FurnitureController**
- `index()` - Get all furniture
- `show(id)` - Get single furniture

#### 4. **LayoutController**
- `predict_batch()` - ML-based furniture positioning
- `get_floor_recommendations()` - Furniture suggestions per floor
- `reset_layout()` - Reset layout state
- `upload_news_image()` - Handle image upload
- `serve_news_image()` - Serve static images

#### 5. **NewsController**
- `index()` - List all news
- `show(id)` - Get news detail
- `store()` - Create news
- `update(id)` - Update news
- `destroy(id)` - Delete news

#### 6. **QuestionController**
- `index()` - Get all questions (admin)
- `get_answered()` - Get answered questions (public)
- `store()` - Submit new question
- `answer(id)` - Answer question (admin)
- `destroy(id)` - Delete question

---

### Models

Models mengelola database operations.

#### 1. **BaseModel**
Base class untuk semua models dengan:
- `get_connection()` - Database connection
- `get_all()` - Get all records
- `find_by_id()` - Get by ID
- `delete_by_id()` - Delete record

#### 2. **CMS**
- `get_all_content()` - Get semua sections
- `get_section()` - Get specific section
- `upsert_section()` - Insert/update section
- `get_theme()` - Get theme JSON
- `upsert_theme()` - Insert/update theme

#### 3. **Furniture**
- `get_all()` - Get all furniture
- `get_by_id()` - Get by ID
- `get_by_category()` - Filter by category

#### 4. **News**
- `get_all()` - Get all news
- `find_by_id()` - Get by ID
- `create()` - Create news
- `update()` - Update news
- `delete_by_id()` - Delete news

#### 5. **Question**
- `get_all()` - Get all questions
- `get_answered()` - Get answered only
- `get_pending()` - Get pending only
- `create()` - Create question
- `answer()` - Answer question
- `delete_by_id()` - Delete question

---

### Services

Services berisi business logic dan algoritma.

#### **LayoutService**

Service untuk ML-based furniture layout prediction dengan collision detection.

**Key Features:**
- Load ML model (Joblib)
- Predict furniture positions
- Collision detection
- Obstacle avoidance (tangga, kolom, dinding)
- Room boundary constraints
- Automatic fallback positioning

**Methods:**
```python
predict_batch(items, room_type, floor_data)
- Input: List furniture, room type, floor layout
- Output: Furniture dengan koordinat X, Y
- Fitur: ML prediction + collision detection + obstacle avoidance

check_collision(item, placed_items)
- Cek overlap antar furniture
- Return: True jika collision

avoid_obstacles(x, y, width, height, obstacles)
- Geser furniture dari obstacles
- Return: Adjusted (x, y)

find_safe_position(width, height, rooms, obstacles, placed_items)
- Cari posisi aman otomatis
- Fallback jika ML prediction collision
```

**Collision Detection:**
- Padding: 20px antar furniture
- Max attempts: 50
- Obstacle avoidance: Aggressive mode
- Room boundary: Respect constraints

---

## 🗄️ Database Schema

### Tables

#### `cms_content`
```sql
section VARCHAR(64) PRIMARY KEY
content JSON
```
Stores: About, Contact, FAQ, Home content

#### `theme`
```sql
id INT PRIMARY KEY
theme_json JSON
```
Stores: Colors, fonts configuration

#### `news`
```sql
id INT AUTO_INCREMENT PRIMARY KEY
title VARCHAR(255)
excerpt TEXT
content TEXT
image VARCHAR(255)
category VARCHAR(100)
author VARCHAR(100)
date DATETIME
published BOOLEAN DEFAULT TRUE
```

#### `furniture`
```sql
id INT AUTO_INCREMENT PRIMARY KEY
nama VARCHAR(255)
dimensi VARCHAR(255)
panjang INT
lebar INT
```

#### `questions`
```sql
id INT AUTO_INCREMENT PRIMARY KEY
name VARCHAR(255) NOT NULL
email VARCHAR(255) NOT NULL
question TEXT NOT NULL
answer TEXT
status VARCHAR(20) DEFAULT 'pending'
created_at DATETIME DEFAULT CURRENT_TIMESTAMP
answered_at DATETIME
answered_by VARCHAR(255)
```

---

## ⚙️ Configuration

File: `config.py`

### Database Settings
```python
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = ""
DB_NAME = "virtualtour1"
```

### Upload Settings
```python
UPLOAD_FOLDER = "static/uploads/news"
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
```

### Admin Credentials
```python
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"
```

### Canvas/Layout Settings
```python
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 800
CANVAS_PADDING = 50
MARGIN = 50
COLLISION_PADDING = 20
MAX_COLLISION_ATTEMPTS = 50
```

### CORS Settings
```python
CORS_ORIGINS = ['http://localhost:3000', 'http://localhost:5000']
```

---

## 🔄 Workflow

### 1. Request Flow
```
Client Request
    ↓
Flask Route (routes/api.py)
    ↓
Controller (app/controllers/)
    ↓
Model/Service (app/models/ or app/services/)
    ↓
Database (MySQL)
    ↓
JSON Response
```

### 2. Furniture Layout Process
```
1. Client kirim list furniture
2. LayoutController.predict_batch()
3. LayoutService load ML model
4. Predict posisi X, Y untuk setiap item
5. Check collision dengan furniture lain
6. Check collision dengan obstacles
7. Adjust posisi jika collision
8. Return final positions
```

---

## 🐛 Troubleshooting

### MySQL Connection Error
```
Error: Can't connect to MySQL server on 'localhost:3306' (10061)
```
**Solusi:**
1. Buka Laragon
2. Klik "Start All"
3. Pastikan MySQL indicator hijau

### Module Not Found
```
Error: No module named 'flask'
```
**Solusi:**
```bash
pip install -r requirements.txt
```

### Upload Folder Error
```
Error: [Errno 2] No such file or directory: 'static/uploads/news'
```
**Solusi:**
```bash
mkdir -p static/uploads/news
```
(Auto-created saat app.py run)

---

## 📝 Development Notes

### Adding New Endpoint

1. **Create Controller Method**
   ```python
   # app/controllers/YourController.py
   @staticmethod
   def your_method():
       return jsonify({"status": "success"})
   ```

2. **Add Route**
   ```python
   # routes/api.py
   @api.route('/your-route', methods=['GET'])
   def your_route():
       return YourController.your_method()
   ```

3. **Test**
   ```bash
   curl http://localhost:5000/api/your-route
   ```

---

## 🧪 Load Testing with K6

Project ini dilengkapi dengan **K6 Load Testing Suite** - modern load testing tool untuk performance testing.

### Quick Start

```powershell
# 1. Install K6
winget install k6

# 2. Start backend
python app.py

# 3. Run quick test
.\quick-start-k6.bat
```

### Test Types Available

| Test | Duration | Purpose | Command |
|------|----------|---------|---------|
| **Smoke** | 30s | Quick check | `k6 run k6-tests/smoke-test.js` |
| **Load** | 4min | Normal load | `k6 run k6-tests/api-load-test.js` |
| **Stress** | 14min | Find limits | `k6 run k6-tests/stress-test.js` |
| **Spike** | 4min | Traffic surge | `k6 run k6-tests/spike-test.js` |
| **Soak** | 30min+ | Memory leaks | `k6 run k6-tests/soak-test.js` |
| **Browser** | 2min | Frontend | `k6 run k6-tests/browser-test.js` |

### Documentation

- **Quick Start:** [K6_README.md](K6_README.md)
- **Complete Guide:** [K6_TESTING_GUIDE.md](K6_TESTING_GUIDE.md)
- **Setup Summary:** [K6_SETUP_COMPLETE.md](K6_SETUP_COMPLETE.md)
- **Quick Reference:** [K6_QUICK_REFERENCE.md](K6_QUICK_REFERENCE.md)

### Example Results

**Good Performance:**
```
✓ checks................: 100.00% ✓ 300  ✗ 0
✓ http_req_duration.....: avg=1.2s   p(95)=2.4s
✓ http_req_failed.......: 0.00%
```

**For more details, see [K6_README.md](K6_README.md)**

---

### Adding New Model

1. **Create Model Class**
   ```python
   # app/models/YourModel.py
   from app.models.BaseModel import BaseModel
   
   class YourModel(BaseModel):
       table_name = "your_table"
   ```

2. **Add to Database**
   ```sql
   CREATE TABLE your_table (
       id INT AUTO_INCREMENT PRIMARY KEY,
       name VARCHAR(255)
   );
   ```

3. **Register in __init__.py**
   ```python
   # app/models/__init__.py
   from app.models.YourModel import YourModel
   ```

---

## 📞 Support

Untuk pertanyaan atau issue, silakan contact developer atau buat issue di repository.

---

## 📄 License

Private project untuk Tugas Akhir.

---

**Version:** 2.0.0  
**Last Updated:** October 25, 2025  
**Author:** [Your Name]
