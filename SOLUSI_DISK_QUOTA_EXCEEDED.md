# ⚠️ SOLUSI: Disk Quota Exceeded saat Install Dependencies

## 🔴 Problem
```
ERROR: Could not install packages due to an OSError: [Errno 122] Disk quota exceeded
```

**Penyebab:** Package ML terlalu besar untuk shared hosting:
- `xgboost==3.0.5` → 94.9 MB
- `nvidia-nccl-cu12` → 296.8 MB (CUDA dependency)
- `pandas==2.2.2` → 13 MB
- `numpy==2.0.2` → 19.5 MB
- `scikit-learn==1.6.1` → 13.5 MB
- **Total:** ~450+ MB (melebihi quota hosting)

---

## ✅ SOLUSI 1: Gunakan Versi Ringan (RECOMMENDED)

File `requirements_hosting.txt` sudah dibuat dengan versi lebih ringan:

```txt
# Flask Web Framework
Flask==3.0.0
flask-cors==4.0.0
Werkzeug==3.0.0

# Database
mysql-connector-python==8.2.0

# Machine Learning (Versi ringan)
pandas==2.1.4
numpy==1.26.4
scikit-learn==1.4.2
joblib==1.4.2

# Utilities
python-dotenv==1.0.0
```

**Install di hosting:**
```bash
# Di terminal cPanel
source /home/virtuali/virtualenv/furnilayout/3.9/bin/activate
cd ~/furnilayout

# Hapus requirements.txt lama
rm requirements.txt

# Upload requirements_hosting.txt dan rename
# atau langsung install
pip install Flask==3.0.0 flask-cors==4.0.0 Werkzeug==3.0.0 mysql-connector-python==8.2.0 pandas==2.1.4 numpy==1.26.4 scikit-learn==1.4.2 joblib==1.4.2 python-dotenv==1.0.0
```

**Estimasi size:** ~150 MB (hemat 300+ MB)

---

## ✅ SOLUSI 2: Install Tanpa XGBoost (PALING RINGAN)

Jika masih disk quota exceeded, skip XGBoost karena aplikasi Flask tidak menggunakannya:

```bash
pip install Flask==3.0.0 flask-cors==4.0.0 Werkzeug==3.0.0
pip install mysql-connector-python==8.2.0
pip install pandas==2.1.4 numpy==1.26.4
pip install scikit-learn==1.4.2 joblib==1.4.2
pip install python-dotenv==1.0.0
```

**Estimasi size:** ~120 MB

---

## ✅ SOLUSI 3: Install Step-by-Step

Install satu per satu untuk monitor quota:

```bash
source /home/virtuali/virtualenv/furnilayout/3.9/bin/activate
cd ~/furnilayout

# Core Flask (kecil)
pip install Flask==3.0.0 flask-cors==4.0.0 Werkzeug==3.0.0 python-dotenv==1.0.0

# Database (kecil)
pip install mysql-connector-python==8.2.0

# ML Core (sedang) - SKIP jika masih error
pip install numpy==1.26.4
pip install pandas==2.1.4
pip install joblib==1.4.2
pip install scikit-learn==1.4.2

# Check disk usage
du -sh ~/.local
```

---

## ✅ SOLUSI 4: Upgrade Hosting Plan

Jika fitur AI Layout **benar-benar diperlukan**:

1. **Upgrade cPanel hosting** ke plan dengan disk space lebih besar
2. Atau **gunakan VPS/Cloud** (DigitalOcean, AWS, Heroku, Railway)
3. Atau **pisahkan AI Service** ke server terpisah (microservices)

---

## 🔧 SOLUSI 5: Disable AI Features di Hosting

Jika AI tidak kritikal, disable service yang butuh ML:

### Edit `app/services/AutoLayoutService.py`:

```python
class AutoLayoutService:
    @staticmethod
    def generate_auto_layout(room_data, furniture_list):
        # Disable AI - return simple layout
        return {
            "status": "error",
            "message": "AI Layout service disabled on hosting (disk quota limitation)",
            "fallback": "Use SimpleLayoutService instead"
        }
```

### Edit `routes/api.py`:

```python
# Disable AI endpoints
@api.route('/layout/predict_batch', methods=['POST'])
def predict_batch():
    return jsonify({
        "status": "disabled",
        "message": "AI prediction disabled on hosting"
    }), 503
```

Aplikasi tetap jalan tapi tanpa AI features.

---

## 📊 Package Size Comparison

| Package | Version (Old) | Size | Version (New) | Size | Saving |
|---------|---------------|------|---------------|------|--------|
| xgboost | 3.0.5 | 94.9 MB | **REMOVED** | 0 MB | 94.9 MB |
| nvidia-nccl-cu12 | - | 296.8 MB | **REMOVED** | 0 MB | 296.8 MB |
| pandas | 2.2.2 | 13 MB | 2.1.4 | 10 MB | 3 MB |
| numpy | 2.0.2 | 19.5 MB | 1.26.4 | 16 MB | 3.5 MB |
| scikit-learn | 1.6.1 | 13.5 MB | 1.4.2 | 11 MB | 2.5 MB |
| scipy | - | 35.9 MB | (dependency) | ~30 MB | 5.9 MB |
| **TOTAL** | | **~470 MB** | | **~120 MB** | **~350 MB** |

---

## 🎯 RECOMMENDED ACTION

**Untuk hosting cPanel dengan quota terbatas:**

1. **Upload `requirements_hosting.txt`** (sudah dibuat)
2. **Install versi ringan:**
   ```bash
   pip install -r requirements_hosting.txt
   ```
3. **Jika masih error**, install manual tanpa ML packages:
   ```bash
   pip install Flask==3.0.0 flask-cors==4.0.0 Werkzeug==3.0.0 mysql-connector-python==8.2.0 python-dotenv==1.0.0
   ```
4. **Test aplikasi** - CMS, FAQ, News, Contact tetap jalan
5. **Disable AI endpoints** jika perlu

**Untuk fitur AI penuh:**
- Upgrade hosting plan dengan disk space > 1GB
- Atau deploy ke platform cloud (Railway, Heroku, DigitalOcean)

---

## ✅ Quick Fix Commands

**Di cPanel Terminal:**
```bash
# Activate venv
source /home/virtuali/virtualenv/furnilayout/3.9/bin/activate
cd ~/furnilayout

# Clear pip cache
pip cache purge

# Install minimal packages
pip install --no-cache-dir Flask==3.0.0 flask-cors==4.0.0 Werkzeug==3.0.0
pip install --no-cache-dir mysql-connector-python==8.2.0
pip install --no-cache-dir python-dotenv==1.0.0

# Install ML (jika masih ada quota)
pip install --no-cache-dir numpy==1.26.4 pandas==2.1.4
pip install --no-cache-dir scikit-learn==1.4.2 joblib==1.4.2

# Restart app
touch ~/furnilayout/tmp/restart.txt
```

**Test API:**
```bash
curl https://api.virtualign.my.id/api/status
```

---

## 📝 Notes

- **Flask + MySQL works** tanpa ML packages (CMS, FAQ, News, dll)
- **AI Layout features** butuh scikit-learn (~100 MB total)
- **XGBoost tidak diperlukan** untuk aplikasi ini (bisa diremove)
- **Shared hosting** biasanya punya limit 500 MB - 1 GB
- **Check quota:** `du -sh ~/.local` atau `quota -s`

---

**Pilih solusi yang sesuai dengan kebutuhan!** 🚀
