# Solusi Error: Host is not allowed to connect to MariaDB server

## Error yang Terjadi
```
DB init skipped: 1130 (HY000): Host '31.58.158.192' is not allowed to connect to this MariaDB server
```

## Penyebab
Server hosting MySQL/MariaDB di virtualign.my.id tidak mengizinkan koneksi dari IP eksternal Anda (31.58.158.192).

---

## SOLUSI 1: Whitelist IP di cPanel (RECOMMENDED)

### Langkah-langkah:

1. **Login ke cPanel hosting Anda**
   - Buka: https://virtualign.my.id:2083 atau https://cpanel.virtualign.my.id
   - Login dengan kredensial hosting

2. **Buka Remote MySQL**
   - Cari menu "Remote MySQL" atau "Remote Database Access"
   - Biasanya di bagian "Databases"

3. **Add Access Host**
   - Masukkan IP Anda: `31.58.158.192`
   - Atau gunakan wildcard: `%` (TIDAK AMAN, hanya untuk testing)
   - Klik "Add Host"

4. **Restart Aplikasi Flask**
   ```bash
   python app.py
   ```

### Screenshot yang Harus Dicari di cPanel:
```
┌─────────────────────────────────────┐
│ Remote MySQL                         │
├─────────────────────────────────────┤
│ Add Access Host                      │
│ Host: [31.58.158.192        ] [Add] │
│                                      │
│ Current Hosts:                       │
│ • localhost                          │
│ • 31.58.158.192          [Delete]   │
└─────────────────────────────────────┘
```

---

## SOLUSI 2: Gunakan SSH Tunnel (Jika Remote MySQL Tidak Tersedia)

Jika hosting tidak support remote MySQL, gunakan SSH tunnel:

### Langkah-langkah:

1. **Install SSH Client** (sudah ada di Windows 10+)

2. **Buat SSH Tunnel**
   ```powershell
   ssh -L 3307:localhost:3306 virtuali@virtualign.my.id -N
   ```
   
   Parameter:
   - `3307`: Port lokal (bisa diganti)
   - `localhost:3306`: MySQL di server hosting
   - `virtuali@virtualign.my.id`: User SSH Anda

3. **Update config.py**
   ```python
   DB_HOST = "localhost"  # Gunakan localhost karena tunnel
   DB_PORT = 3307         # Port tunnel lokal
   DB_USER = "virtuali_virtualuser"
   DB_PASSWORD = "indra140603"
   DB_NAME = "virtuali_virtualign"
   ```

4. **Jalankan Aplikasi**
   Di terminal baru (biarkan SSH tunnel tetap jalan):
   ```bash
   python app.py
   ```

---

## SOLUSI 3: Deploy Backend ke Hosting yang Sama

**Cara Terbaik untuk Production:**

### Option A: Deploy Flask ke Shared Hosting

1. **Upload semua file backend ke hosting**
   - Via FTP/cPanel File Manager
   - Upload ke folder: `public_html/api/` atau `backend/`

2. **Setup Python di hosting**
   - cPanel → Setup Python App
   - Python version: 3.8+
   - Application root: `/home/virtuali/backend`
   - Application URL: `virtualign.my.id/api`

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Update config.py di hosting**
   ```python
   DB_HOST = "localhost"  # Di hosting yang sama
   DB_USER = "virtuali_virtualuser"
   DB_PASSWORD = "indra140603"
   DB_NAME = "virtuali_virtualign"
   ```

5. **Restart Python App**

### Option B: Deploy ke VPS/Cloud

- Deploy ke DigitalOcean, AWS, Heroku, dll
- Database dan Backend di server yang sama
- Whitelist IP VPS di hosting MySQL

---

## SOLUSI 4: Gunakan Database Lokal untuk Development

Untuk development sementara, gunakan database lokal:

### File: `config_local.py`

```python
"""Local development configuration"""
from config import Config
from datetime import timedelta

class LocalConfig(Config):
    """Local development with local database"""
    
    # Database settings - Local MySQL (Laragon)
    DB_HOST = "localhost"
    DB_USER = "root"
    DB_PASSWORD = ""
    DB_NAME = "virtualtour1"
    DB_PORT = 3306
    
    DEBUG = True
    TESTING = False
```

### File: `app.py` (Update)

```python
import os
from config import get_config

# Gunakan local config untuk development
env = os.environ.get('FLASK_ENV', 'development')

if env == 'development':
    # Import local config
    from config_local import LocalConfig
    app.config.from_object(LocalConfig)
else:
    # Production config (hosting)
    app.config.from_object(get_config(env))
```

---

## TESTING KONEKSI

### Test 1: Cek IP Anda

```powershell
# Windows PowerShell
Invoke-WebRequest -Uri "https://api.ipify.org" | Select-Object -ExpandProperty Content
```

### Test 2: Test Koneksi MySQL dari Lokal

```powershell
# Install mysql client
# Download dari: https://dev.mysql.com/downloads/mysql/

# Test connection
mysql -h virtualign.my.id -u virtuali_virtualuser -pindra140603 virtuali_virtualign
```

Jika berhasil connect, berarti IP sudah di-whitelist.

### Test 3: Test dari Python

Buat file `test_db_connection.py`:

```python
import mysql.connector
from mysql.connector import Error

def test_connection():
    try:
        connection = mysql.connector.connect(
            host='virtualign.my.id',
            database='virtuali_virtualign',
            user='virtuali_virtualuser',
            password='indra140603',
            connection_timeout=10
        )
        
        if connection.is_connected():
            db_info = connection.get_server_info()
            print(f"✓ Successfully connected to MySQL Server version {db_info}")
            
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            record = cursor.fetchone()
            print(f"✓ You're connected to database: {record}")
            
            cursor.close()
            connection.close()
            print("✓ MySQL connection is closed")
            return True
            
    except Error as e:
        print(f"✗ Error connecting to MySQL: {e}")
        return False

if __name__ == "__main__":
    test_connection()
```

Jalankan:
```bash
python test_db_connection.py
```

---

## REKOMENDASI UNTUK TA ANDA

### Development (Sekarang):
1. Gunakan **database lokal Laragon** untuk development
2. File: `config_local.py` dengan DB_HOST = "localhost"

### Testing & Demo:
1. Gunakan **SSH Tunnel** (Solusi 2) untuk connect ke hosting
2. Atau deploy backend ke subdomain testing

### Production (Deployment Final):
1. **Deploy backend ke hosting yang sama** dengan database
2. Update `config.py` dengan DB_HOST = "localhost"
3. Pastikan HTTPS aktif
4. Environment variables untuk password

---

## QUICK FIX SEKARANG

Pilih salah satu:

### A. Pakai Database Lokal (Cepat)
```bash
# Ganti config.py
DB_HOST = "localhost"
DB_USER = "root"  
DB_PASSWORD = ""
DB_NAME = "virtualtour1"

# Import database
mysql -u root virtualtour1 < backup.sql

# Jalankan
python app.py
```

### B. Whitelist IP (Jika ada akses cPanel)
1. Login cPanel
2. Remote MySQL → Add: `31.58.158.192`
3. Atau add: `%` (semua IP, temporary)

### C. Hubungi Provider Hosting
Minta mereka whitelist IP: `31.58.158.192`

---

## KONTAK SUPPORT HOSTING

Jika tidak bisa akses cPanel, hubungi support hosting Anda dengan pesan:

```
Subject: Request Remote MySQL Access

Halo Support,

Saya memerlukan remote access ke MySQL database untuk aplikasi web saya.

Details:
- Domain: virtualign.my.id
- Database: virtuali_virtualign
- IP yang perlu di-whitelist: 31.58.158.192

Mohon dapat dibantu untuk menambahkan IP tersebut ke Remote MySQL Access Hosts.

Terima kasih.
```

---

Untuk sekarang, saya sarankan gunakan **database lokal** dulu untuk development, lalu deploy ke hosting saat sudah siap production.
