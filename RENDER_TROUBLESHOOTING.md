# 🔧 Render.com Deployment Troubleshooting Guide (বাংলা)

## ❌ Common Errors এবং Solutions

### 1. Build Failures

#### Error: `ERROR: Could not find a version that satisfies the requirement sqlite3`
**Solution:**
```txt
# Remove sqlite3 from requirements.txt (it's a built-in module)
# Remove these built-in modules:
# - sqlite3
# - hashlib
# - hmac
# - logging
# - datetime
# - time
# - threading
# - pathlib
# - os
# - sys
# - json
# - webbrowser
```

#### Error: `ModuleNotFoundError: No module named 'xxx'`
**Solution:**
```bash
# Check if module is in requirements.txt
# Add missing module to requirements.txt
# Make sure module name is correct
```

### 2. Runtime Errors

#### Error: `Port already in use`
**Solution:**
```python
# Use PORT environment variable
port = int(os.environ.get("PORT", 10000))
host = os.environ.get("HOST", "0.0.0.0")
```

#### Error: `Database connection failed`
**Solution:**
```python
# Create data directory
import os
from pathlib import Path

data_dir = Path("data")
data_dir.mkdir(exist_ok=True)

# Update database path
DATABASE_PATH = data_dir / "trading_bot.db"
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"
```

### 3. Environment Variable Issues

#### Error: `Environment variable not found`
**Solution:**
```env
# Add these to Render dashboard Environment tab:
PIONEX_API_KEY=your_actual_pionex_api_key
PIONEX_SECRET_KEY=your_actual_pionex_secret_key
SECRET_KEY=your_secure_random_secret_key_here
RENDER=true
```

### 4. Import Errors

#### Error: `ImportError: No module named 'gui_app'`
**Solution:**
```python
# Make sure gui_app.py exists in root directory
# Check file permissions
# Verify import path
```

## 🔧 Debug Commands

### 1. Check Render Logs
```bash
# Render Dashboard → Your Service → Logs
# Look for error messages
# Check build logs
```

### 2. Test Locally
```bash
# Test requirements.txt
pip install -r requirements.txt

# Test application
python main.py

# Test imports
python -c "import gui_app; print('Import successful')"
```

### 3. Check Environment Variables
```python
# Add this to your code to debug
import os
print("Environment variables:")
for key, value in os.environ.items():
    if 'PIONEX' in key or 'SECRET' in key:
        print(f"{key}: {value[:10]}...")
```

## 📋 Fixed Requirements.txt

```txt
# Core Flask Framework
Flask==2.3.3
Flask-SocketIO==5.3.6
python-socketio==5.8.0
python-engineio==4.7.1

# Environment and Configuration
python-dotenv==1.0.0
PyYAML==6.0.1

# Database
SQLAlchemy==2.0.21

# HTTP Requests
requests==2.31.0
urllib3==2.0.4

# Cryptography and Security
cryptography==41.0.4

# Data Processing
pandas==2.0.3
numpy==1.24.3

# Technical Analysis
ta==0.10.2
scipy==1.11.1

# WebSocket Support
websocket-client==1.6.1

# Additional Utilities
schedule==1.2.0
psutil==5.9.5

# Production Server
gunicorn==21.2.0
eventlet==0.33.3
```

## 🔧 Fixed main.py

```python
#!/usr/bin/env python3
"""
Pionex Trading Bot GUI - Main Entry Point for Render.com
"""

import os
import sys
from pathlib import Path

def main():
    """Main entry point for the GUI on Render.com"""
    print("🚀 Starting Pionex Trading Bot GUI on Render.com...")
    
    # Render.com specific setup
    if os.environ.get('RENDER'):
        print("📦 Running on Render.com environment")
        
        # Create necessary directories
        data_dir = Path("data")
        logs_dir = Path("logs")
        
        data_dir.mkdir(exist_ok=True)
        logs_dir.mkdir(exist_ok=True)
        
        print(f"📁 Data directory: {data_dir.absolute()}")
        print(f"📁 Logs directory: {logs_dir.absolute()}")
    
    # Import and run the GUI
    try:
        from gui_app import main as gui_main
        gui_main()
        return 0
    except Exception as e:
        print(f"❌ Error starting GUI: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
```

## 🔧 Fixed gui_app.py

```python
# Render.com configuration
import os
from pathlib import Path

# Render.com environment setup
if os.environ.get('RENDER'):
    # Render.com specific paths
    DATA_DIR = Path("data")
    LOGS_DIR = Path("logs")
    
    DATA_DIR.mkdir(exist_ok=True)
    LOGS_DIR.mkdir(exist_ok=True)
    
    # Update database path
    DATABASE_PATH = DATA_DIR / "trading_bot.db"
    DATABASE_URL = f"sqlite:///{DATABASE_PATH}"
    
    # Render.com port configuration
    PORT = int(os.environ.get("PORT", 10000))
    HOST = os.environ.get("HOST", "0.0.0.0")
else:
    # Local development configuration
    PORT = int(os.environ.get("PORT", 5000))
    HOST = os.environ.get("HOST", "127.0.0.1")

# Update the main function
def main():
    """Main function for Render.com deployment"""
    print(f"🚀 Starting Pionex Trading Bot GUI on {HOST}:{PORT}")
    
    # Start the application
    socketio.run(app, host=HOST, port=PORT, debug=False)

if __name__ == "__main__":
    main()
```

## 📋 Deployment Checklist

### Before Deployment:
- ✅ **requirements.txt** fixed (no built-in modules)
- ✅ **main.py** Render compatible
- ✅ **gui_app.py** Render compatible
- ✅ **Environment variables** prepared
- ✅ **GitHub repository** updated

### During Deployment:
- ✅ **Build successful** (green checkmark)
- ✅ **No import errors**
- ✅ **Port configuration** correct
- ✅ **Database setup** working

### After Deployment:
- ✅ **Service status** Active
- ✅ **Application loads** correctly
- ✅ **API connections** working
- ✅ **Logs** showing normal activity

## 🚨 Emergency Fixes

### If Build Still Fails:
1. **Delete and recreate service** in Render dashboard
2. **Clear cache** and redeploy
3. **Check GitHub repository** for latest changes
4. **Verify environment variables**

### If Runtime Errors:
1. **Check logs** for specific error messages
2. **Test locally** first
3. **Update code** and redeploy
4. **Contact support** if needed

## 📞 Support

যদি কোন সমস্যা হয়:

1. **Check Render logs** for specific error messages
2. **Test requirements.txt** locally
3. **Verify environment variables**
4. **Update code** and redeploy

এই guide follow করে আপনি Render.com deployment issues fix করতে পারবেন! 