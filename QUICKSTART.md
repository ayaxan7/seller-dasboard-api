# 🚀 Quick Start Guide - Running in Virtual Environment

## Complete Setup Steps

### 1️⃣ Create Virtual Environment (One Time Setup)
```bash
cd /Users/ayaan/development/seller-dashboard
python3 -m venv venv
```

### 2️⃣ Activate Virtual Environment

**For Fish Shell (your current shell):**
```bash
source venv/bin/activate.fish
```

**For Bash/Zsh:**
```bash
source venv/bin/activate
```

After activation, you should see `(venv)` at the beginning of your prompt.

### 3️⃣ Install Dependencies (One Time Setup)
```bash
pip install -r requirements.txt
```

### 4️⃣ Run the Server

**Option A: With virtual environment activated:**
```bash
uvicorn main:app --reload --port 8000
```

**Option B: Without activating (using full path):**
```bash
venv/bin/uvicorn main:app --reload --port 8000
```

**Option C: Using Python directly:**
```bash
python main.py
```

## ✅ Server Status

When the server starts successfully, you'll see:
```
INFO: Uvicorn running on http://127.0.0.1:8000
INFO: Firebase Admin SDK initialized successfully
INFO: Firebase connection established
INFO: Application startup complete.
```

## 🌐 Access Your API

Once the server is running:

- **API Root:** http://localhost:8000/
- **Interactive Docs (Swagger):** http://localhost:8000/docs
- **Alternative Docs (ReDoc):** http://localhost:8000/redoc
- **Health Check:** http://localhost:8000/health

## 📊 Test API Endpoints

### Using Browser or curl

```bash
# Get all products
curl http://localhost:8000/products

# Get product by ID
curl http://localhost:8000/products/YOUR_PRODUCT_ID

# Get products by vendor
curl http://localhost:8000/products/vendor/YOUR_VENDOR_ID

# Health check
curl http://localhost:8000/health
```

### Using Interactive Documentation

1. Open http://localhost:8000/docs in your browser
2. Click on any endpoint
3. Click "Try it out"
4. Fill in parameters (if needed)
5. Click "Execute"

## 🛑 Stop the Server

Press `CTRL + C` in the terminal where the server is running.

## 🔧 Common Issues & Solutions

### Issue: `uvicorn: command not found`
**Solution:** Either activate the virtual environment first, or use the full path:
```bash
venv/bin/uvicorn main:app --reload --port 8000
```

### Issue: Port already in use
**Solution:** Use a different port:
```bash
uvicorn main:app --reload --port 8001
```

### Issue: Firebase connection error
**Solution:** Make sure `serviceAccountKey.json` has your actual Firebase credentials.

## 💡 Development Tips

### Auto-reload is enabled
The `--reload` flag means the server automatically restarts when you make code changes.

### Deactivate Virtual Environment
When you're done working:
```bash
deactivate
```

### Reinstall Dependencies
If you add new packages:
```bash
pip install -r requirements.txt
```

### Update Requirements
If you install a new package:
```bash
pip freeze > requirements.txt
```

## 🎯 Current Configuration

- **Python Version:** 3.13.5
- **Virtual Environment:** `/Users/ayaan/development/seller-dashboard/venv`
- **Server:** Uvicorn (ASGI)
- **Port:** 8000
- **Firebase Project:** bazaar-c4e05
- **Auto-reload:** Enabled

## 📝 Quick Commands Reference

```bash
# Create virtual environment
python3 -m venv venv

# Activate (Fish shell)
source venv/bin/activate.fish

# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn main:app --reload --port 8000

# Run in background
venv/bin/uvicorn main:app --reload --port 8000 &

# Deactivate virtual environment
deactivate
```

---

**Your server is currently running at: http://localhost:8000** ✨

Check out the interactive documentation at: http://localhost:8000/docs
