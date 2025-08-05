# 🚀 Render.com এ Quick Deployment Guide (বাংলা)

## ⚡ দ্রুত Deployment (10 মিনিটে)

### Step 1: Render.com এ Account Create করুন

#### 1.1 Sign Up করুন
- [Render.com](https://render.com) এ visit করুন
- "Get Started for Free" click করুন
- GitHub, Google, বা Email দিয়ে sign up করুন

#### 1.2 GitHub Connect করুন
- GitHub account connect করুন
- আপনার repository access দিন: `Telegram-Airdrop-Bot/pionex-trading-bot`

### Step 2: New Web Service Create করুন

#### 2.1 Service Setup
1. **Render Dashboard এ যান**
2. **"New" → "Web Service" click করুন**
3. **GitHub repository connect করুন**

#### 2.2 Service Configuration
```
Service Name: pionex-trading-bot-gui
Environment: Python 3
Region: Singapore (Asia)
Branch: main
Root Directory: . (leave empty)
```

### Step 3: Build Configuration Setup করুন

#### 3.1 Build Commands
```
Build Command: pip install -r requirements.txt
Start Command: python main.py
```

#### 3.2 Environment Variables Add করুন
Render Dashboard এ "Environment" tab এ যান এবং এই variables add করুন:

```env
# Required Variables
PIONEX_API_KEY=your_actual_pionex_api_key
PIONEX_SECRET_KEY=your_actual_pionex_secret_key
SECRET_KEY=your_secure_random_secret_key_here
RENDER=true

# Optional Variables
DATABASE_URL=sqlite:///data/trading_bot.db
LOG_LEVEL=INFO
GUI_HOST=0.0.0.0
GUI_PORT=10000
GUI_DEBUG=false
```

### Step 4: Deploy করুন

#### 4.1 Create Service
- **"Create Web Service" click করুন**
- **Build process wait করুন** (5-10 minutes)
- **Deployment URL copy করুন**

#### 4.2 Verify Deployment
- **Service URL visit করুন**
- **Logs check করুন**
- **Health check করুন**

## 🔧 Manual Configuration (যদি প্রয়োজন হয়)

### Step 1: Application Code Update

#### 1.1 main.py Update করুন
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

#### 1.2 gui_app.py Update করুন
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

### Step 2: Requirements.txt Update করুন
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

### Step 3: Render.yaml Configuration
```yaml
services:
  - type: web
    name: pionex-trading-bot-gui
    env: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: python main.py
    envVars:
      - key: PIONEX_API_KEY
        value: your_actual_pionex_api_key
      - key: PIONEX_SECRET_KEY
        value: your_actual_pionex_secret_key
      - key: SECRET_KEY
        value: your_secure_random_secret_key_here
      - key: DATABASE_URL
        value: sqlite:///data/trading_bot.db
      - key: LOG_LEVEL
        value: INFO
      - key: GUI_HOST
        value: 0.0.0.0
      - key: GUI_PORT
        value: 10000
      - key: GUI_DEBUG
        value: false
      - key: RENDER
        value: true
```

## 📋 Deployment Checklist

### Before Deployment:
- ✅ **GitHub repository** ready
- ✅ **requirements.txt** updated
- ✅ **main.py** Render compatible
- ✅ **Environment variables** prepared
- ✅ **Pionex API credentials** ready

### During Deployment:
- ✅ **Build successful** (green checkmark)
- ✅ **Service status** Active
- ✅ **Logs** no errors
- ✅ **URL accessible**

### After Deployment:
- ✅ **Application loads** correctly
- ✅ **API connections** working
- ✅ **Database** initialized
- ✅ **Logs** showing normal activity

## 🔧 Troubleshooting

### Common Issues:

#### 1. Build Failures
```bash
# Check requirements.txt
# Verify Python version compatibility
# Check for missing dependencies
```

#### 2. Runtime Errors
```bash
# Check Render logs
# Verify environment variables
# Check database permissions
```

#### 3. Port Issues
```python
# Ensure using PORT environment variable
port = int(os.environ.get("PORT", 10000))
```

#### 4. Database Issues
```python
# Ensure data directory exists
# Check file permissions
# Verify database path
```

### Debug Commands:
```bash
# Check Render logs
# Render Dashboard → Your Service → Logs

# Check environment variables
# Render Dashboard → Your Service → Environment

# Restart service
# Render Dashboard → Your Service → Manual Deploy
```

## 🎯 Success Indicators

Render.com deployment successful হলে আপনি দেখতে পাবেন:

✅ **Service Status**: Active  
✅ **Build Status**: Build successful  
✅ **Deployment URL**: https://your-app-name.onrender.com  
✅ **Health Check**: `/health` endpoint responding  
✅ **Logs**: No errors in Render logs  

## 📞 Support

যদি কোন সমস্যা হয়:

1. **Render Logs check করুন**
2. **Environment variables verify করুন**
3. **Build logs analyze করুন**
4. **Service status check করুন**

এই guide follow করে আপনি easily এবং quickly Render.com এ Pionex Trading Bot GUI deploy করতে পারবেন! 