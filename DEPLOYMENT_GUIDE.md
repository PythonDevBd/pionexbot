# 🚀 Pionex Trading Bot GUI - Deployment Guide

## 📋 Overview

This guide covers deployment to various platforms with proper version management and configuration.

## 🛠️ Files Created

### 1. **Procfile**
- Specifies how to run the application
- Used by Heroku and other platforms
- Command: `web: python main.py`

### 2. **runtime.txt**
- Specifies Python version: `python-3.11.7`
- Ensures consistent Python version across deployments

### 3. **requirements_basic.txt**
- Minimal requirements without heavy compilation packages
- Excludes scipy, pandas to avoid compilation issues
- Includes only essential packages

### 4. **deployment_config.py**
- Handles different deployment environments
- Auto-detects platform (Render, Heroku, Railway, etc.)
- Sets appropriate configuration for each platform

### 5. **render.yaml**
- Updated to use `requirements_basic.txt`
- Includes proper build commands
- Environment variables configured

## 🌍 Supported Platforms

### 1. **Render.com**
```yaml
# render.yaml configuration
services:
  - type: web
    name: pionex-trading-bot-gui
    env: python
    plan: free
    buildCommand: |
      pip install --upgrade pip setuptools wheel
      pip install -r requirements_basic.txt
    startCommand: python main.py
```

### 2. **Heroku**
```bash
# Procfile
web: python main.py

# runtime.txt
python-3.11.7
```

### 3. **Railway**
```bash
# Uses Procfile automatically
# runtime.txt for Python version
```

### 4. **DigitalOcean App Platform**
```yaml
# Uses render.yaml format
# Or custom configuration
```

## 🔧 Installation Methods

### Method 1: Basic Requirements (Recommended)
```bash
pip install -r requirements_basic.txt
```

### Method 2: Minimal Installation
```bash
# Install core packages only
pip install Flask>=2.2.0,<2.4.0
pip install Flask-SocketIO>=5.2.0,<5.4.0
pip install python-dotenv>=0.19.0,<1.1.0
pip install requests>=2.28.0,<2.32.0
```

### Method 3: Development Installation
```bash
# Install with development tools
pip install -r requirements.txt
```

## 🚀 Deployment Steps

### Render.com Deployment

1. **Push to GitHub**
```bash
git add .
git commit -m "Add deployment configuration"
git push origin main
```

2. **Create Render Service**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New Web Service"
   - Connect your GitHub repository
   - Service Name: `pionex-trading-bot-gui`
   - Environment: `Python 3`
   - Build Command: `pip install --upgrade pip setuptools wheel && pip install -r requirements_basic.txt`
   - Start Command: `python main.py`

3. **Add Environment Variables**
   - `PIONEX_API_KEY`: Your Pionex API key
   - `PIONEX_SECRET_KEY`: Your Pionex secret key
   - `SECRET_KEY`: Random secret key
   - `RENDER`: `true`

### Heroku Deployment

1. **Install Heroku CLI**
```bash
# Download from https://devcenter.heroku.com/articles/heroku-cli
```

2. **Deploy to Heroku**
```bash
heroku create your-app-name
git push heroku main
```

3. **Set Environment Variables**
```bash
heroku config:set PIONEX_API_KEY=your_api_key
heroku config:set PIONEX_SECRET_KEY=your_secret_key
heroku config:set SECRET_KEY=your_random_secret
```

### Railway Deployment

1. **Connect Repository**
   - Go to [Railway Dashboard](https://railway.app)
   - Connect your GitHub repository
   - Railway will auto-detect Python app

2. **Environment Variables**
   - Add in Railway dashboard
   - Same variables as Render.com

## 🔍 Troubleshooting

### Common Issues

1. **Compilation Errors**
   - Use `requirements_basic.txt` instead of full requirements
   - Avoid heavy packages like scipy, pandas

2. **Port Issues**
   - Use `$PORT` environment variable
   - Default to port 5000 for local development

3. **Import Errors**
   - Check Python version compatibility
   - Use Python 3.11.7 (specified in runtime.txt)

4. **Database Issues**
   - SQLite works for basic deployments
   - Use PostgreSQL for production

### Debug Commands

```bash
# Test local installation
python deployment_config.py

# Test Flask app
python -c "from flask import Flask; app = Flask(__name__); print('Flask OK')"

# Check Python version
python --version

# List installed packages
pip list
```

## 📊 Environment Detection

The `deployment_config.py` automatically detects:

- **Render.com**: `RENDER` environment variable
- **Heroku**: `HEROKU` environment variable  
- **Railway**: `RAILWAY` environment variable
- **DigitalOcean**: `DIGITALOCEAN` environment variable
- **Local**: Default configuration

## 🎯 Expected Results

Successful deployment should show:

```
🚀 Starting Pionex Trading Bot GUI...
🌍 Environment: render
🏠 Host: 0.0.0.0
🚪 Port: 10000
🐛 Debug: false
💾 Database: sqlite:///data/trading_bot.db
📁 Data directory: /app/data
📁 Logs directory: /app/logs
✅ Deployment configuration ready!
```

## 🔗 URLs

After deployment, your app will be available at:

- **Render.com**: `https://your-app-name.onrender.com`
- **Heroku**: `https://your-app-name.herokuapp.com`
- **Railway**: `https://your-app-name.railway.app`

## 📝 Notes

- Use `requirements_basic.txt` for deployment
- Use `requirements.txt` for local development
- Python 3.11.7 is recommended for stability
- Alternative data processing available in `data_utils.py`
- All platforms support the same environment variables 