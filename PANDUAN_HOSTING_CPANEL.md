# 📘 Panduan Hosting Flask Backend ke cPanel

## 📋 Persyaratan
- cPanel hosting dengan support Python (Passenger)
- Akses SSH atau File Manager cPanel
- Domain/subdomain untuk backend (contoh: api.virtualign.my.id)

---

## 🚀 Step-by-Step Hosting Flask ke cPanel

### **STEP 1: Setup Python Application di cPanel**

1. **Login ke cPanel** → `virtualign.my.id/cpanel`
   - Username: `virtuali`
   - Password: `indra140603`

2. **Buka "Setup Python App"** (di kategori Software)
   
3. **Create Application:**
   ```
   Python version: 3.9.x (pilih yang tersedia)
   Application root: furnilayout
   Application URL: api.virtualign.my.id (atau subdomain/folder)
   Application startup file: passenger_wsgi.py
   Application Entry point: application
   ```

4. **Klik "CREATE"**

5. **Copy Virtual Environment Path** yang muncul, contoh:
   ```
   source /home/virtuali/virtualenv/furnilayout/3.9/bin/activate && cd /home/virtuali/furnilayout
   ```

---

### **STEP 2: Upload File Backend**

#### **Opsi A: Via File Manager (Mudah)**

1. **Compress project** di local jadi ZIP:
   ```powershell
   # Di E:\TA, exclude folder yang tidak perlu
   Compress-Archive -Path .\* -DestinationPath backend.zip -Exclude frontend,__pycache__,.git,venv
   ```

2. **Upload via File Manager:**
   - Login cPanel → File Manager
   - Navigasi ke folder `furnilayout/`
   - Upload `backend.zip`
   - Extract di server

#### **Opsi B: Via FTP (Alternatif)**

1. Download FileZilla
2. Connect ke:
   ```
   Host: virtualign.my.id
   Username: virtuali
   Password: indra140603
   Port: 21
   ```
3. Upload semua file ke folder `furnilayout/`

#### **Opsi C: Via SSH (Advanced)**

```bash
# Connect via SSH (jika tersedia)
ssh virtuali@virtualign.my.id

# Navigate to directory
cd ~/furnilayout

# Upload files using scp/rsync from local
```

---

### **STEP 3: Install Dependencies**

1. **Buka Terminal di cPanel:**
   - cPanel → Terminal (Advanced)
   
2. **Activate Virtual Environment:**
   ```bash
   source /home/virtuali/virtualenv/furnilayout/3.9/bin/activate
   cd ~/furnilayout
   ```

3. **Install requirements:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify installation:**
   ```bash
   pip list
   ```

---

### **STEP 4: Setup Environment & Config**

1. **Check config.py** sudah benar:
   ```python
   # Database (sudah OK ✓)
   DB_HOST = "virtualign.my.id"
   DB_USER = "virtuali_virtualuser"
   DB_PASSWORD = "indra140603"
   DB_NAME = "virtuali_virtualign"
   ```

2. **Set permissions untuk upload folder:**
   ```bash
   chmod 755 ~/furnilayout/static/uploads
   chmod 755 ~/furnilayout/static/uploads/news
   ```

3. **Check passenger_wsgi.py path** sesuai dengan virtual env:
   - Edit line `INTERP` jika perlu sesuaikan path Python

---

### **STEP 5: Setup Subdomain untuk API (Opsional)**

Jika ingin pakai subdomain `api.virtualign.my.id`:

1. **cPanel → Subdomains**
2. **Create Subdomain:**
   ```
   Subdomain: api
   Domain: virtualign.my.id
   Document Root: /home/virtuali/furnilayout
   ```
3. **Klik Create**

---

### **STEP 6: Restart Application**

1. **Via cPanel Setup Python App:**
   - Buka "Setup Python App"
   - Klik nama aplikasi (furnilayout)
   - Scroll bawah → Klik "RESTART"

2. **Via Terminal:**
   ```bash
   touch ~/furnilayout/tmp/restart.txt
   # atau
   mkdir -p ~/furnilayout/tmp && touch ~/furnilayout/tmp/restart.txt
   ```

3. **Via .htaccess (automatic):**
   - Setiap edit `passenger_wsgi.py` otomatis restart

---

### **STEP 7: Testing**

1. **Test API Status:**
   ```bash
   curl https://api.virtualign.my.id/api/status
   # atau
   curl https://virtualign.my.id/api/status
   ```

   **Expected Response:**
   ```json
   {
     "status": "OK",
     "message": "FurniLayout API Server is running",
     "version": "1.0.0",
     "database": "Connected"
   }
   ```

2. **Test Database Connection:**
   ```bash
   curl https://api.virtualign.my.id/api/cms/content
   ```

3. **Test di Browser:**
   - `https://api.virtualign.my.id/api/status`
   - `https://api.virtualign.my.id/api/faqs`
   - `https://api.virtualign.my.id/api/news`

---

## 📂 Struktur File di Server

```
/home/virtuali/furnilayout/
├── passenger_wsgi.py          # ← WSGI entry point (WAJIB)
├── .htaccess                  # ← Passenger config (WAJIB)
├── app.py                     # ← Flask application
├── config.py                  # ← Configuration
├── requirements.txt           # ← Dependencies
├── app/
│   ├── controllers/
│   ├── models/
│   └── services/
├── database/
│   ├── connection.py
│   └── schema.sql
├── routes/
│   └── api.py
├── static/
│   └── uploads/
│       └── news/
└── tmp/
    └── restart.txt            # ← Touch untuk restart
```

---

## ⚠️ Troubleshooting

### **Error 1: Application Error (500)**
```bash
# Check error logs
cat ~/logs/furnilayout_error_log

# Restart aplikasi
touch ~/furnilayout/tmp/restart.txt
```

### **Error 2: Module Not Found**
```bash
# Pastikan virtual env aktif
source /home/virtuali/virtualenv/furnilayout/3.9/bin/activate

# Install ulang requirements
pip install -r requirements.txt
```

### **Error 3: Database Connection Failed**
```bash
# Test koneksi database
python test_db_connection.py

# Pastikan IP server sudah di-whitelist di Remote MySQL cPanel
```

### **Error 4: Permission Denied (Upload)**
```bash
# Set permissions
chmod -R 755 ~/furnilayout/static/uploads
chown -R virtuali:virtuali ~/furnilayout/static/uploads
```

### **Error 5: Passenger Not Starting**
```bash
# Check passenger_wsgi.py path Python interpreter
# Edit INTERP variable sesuai output dari Setup Python App

# Check .htaccess path
# Pastikan PassengerAppRoot dan PassengerPython benar
```

---

## 🔧 Update Backend di Production

Setiap kali update code:

```bash
# 1. Login SSH/Terminal
ssh virtuali@virtualign.my.id

# 2. Activate venv
source /home/virtuali/virtualenv/furnilayout/3.9/bin/activate
cd ~/furnilayout

# 3. Pull/upload code terbaru
# (upload via File Manager atau git pull)

# 4. Install dependencies baru (jika ada)
pip install -r requirements.txt

# 5. Restart aplikasi
touch tmp/restart.txt
```

---

## 🌐 Update Frontend untuk Connect ke Backend

Di `frontend/src/services/api.js`:

```javascript
// Development
// const API_BASE_URL = 'http://localhost:5000';

// Production
const API_BASE_URL = 'https://api.virtualign.my.id';

export default API_BASE_URL;
```

---

## 📊 Monitoring

1. **Check Application Status:**
   - cPanel → Setup Python App → View aplikasi
   - Lihat status: Running/Stopped

2. **View Logs:**
   ```bash
   # Error logs
   tail -f ~/logs/furnilayout_error_log
   
   # Access logs
   tail -f ~/logs/furnilayout_access_log
   ```

3. **Resource Usage:**
   - cPanel → CPU and Concurrent Connection Usage

---

## ✅ Checklist Deployment

- [ ] Python app created di cPanel
- [ ] Virtual environment setup
- [ ] Files uploaded ke `~/furnilayout/`
- [ ] `passenger_wsgi.py` ada dan path benar
- [ ] `.htaccess` ada dengan config Passenger
- [ ] `requirements.txt` installed
- [ ] `config.py` menggunakan hosting database ✓
- [ ] Database imported (46 rows) ✓
- [ ] Upload folder permissions (755)
- [ ] Application restarted
- [ ] API `/api/status` response OK
- [ ] Frontend `api.js` updated ke production URL
- [ ] DNS/Subdomain configured (jika pakai subdomain)

---

## 🎯 Next Steps Setelah Backend Live

1. **Build & Deploy Frontend:**
   ```bash
   cd frontend
   npm run build
   # Upload folder build/ ke public_html/
   ```

2. **Setup SSL Certificate:**
   - cPanel → SSL/TLS Status
   - Enable AutoSSL untuk domain

3. **Configure CORS jika perlu:**
   - Sudah dihandle di `app.py` dengan `flask-cors`

4. **Test End-to-End:**
   - Frontend → Backend → Database
   - All features working

---

## 📞 Support

- **cPanel Login:** https://virtualign.my.id:2083
- **Documentation:** cPanel Python Documentation
- **Logs Location:** `~/logs/`

---

**Good luck! 🚀**
