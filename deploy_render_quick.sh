#!/bin/bash

# Render.com Quick Deployment Script
# This script prepares your project for Render.com deployment

echo "🚀 Preparing Pionex Trading Bot GUI for Render.com deployment..."

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Step 1: Check if we're in the right directory
if [ ! -f "gui_app.py" ]; then
    print_error "Please run this script from the project root directory"
    exit 1
fi

print_status "Starting Render.com deployment preparation..."

# Step 2: Update main.py for Render compatibility
print_status "Updating main.py for Render.com compatibility..."

cat > main.py << 'EOF'
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
EOF

print_status "Updated main.py for Render.com"

# Step 3: Update requirements.txt
print_status "Updating requirements.txt..."

cat > requirements.txt << 'EOF'
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
EOF

print_status "Updated requirements.txt"

# Step 4: Create render.yaml
print_status "Creating render.yaml configuration..."

cat > render.yaml << 'EOF'
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
EOF

print_status "Created render.yaml"

# Step 5: Create .gitignore
print_status "Creating .gitignore..."

cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
env.bak/
venv.bak/

# Environment variables
.env
.env.local
.env.production

# Database
*.db
*.sqlite
*.sqlite3

# Logs
*.log
logs/

# Data
data/
trading_bot.db

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Render
.render-buildlogs/
EOF

print_status "Created .gitignore"

# Step 6: Update gui_app.py for Render compatibility
print_status "Checking gui_app.py for Render compatibility..."

# Check if gui_app.py needs Render-specific updates
if grep -q "socketio.run" gui_app.py; then
    print_status "gui_app.py already has socketio.run - checking for Render compatibility..."
    
    # Check if PORT environment variable is used
    if ! grep -q "os.environ.get.*PORT" gui_app.py; then
        print_warning "Consider updating gui_app.py to use PORT environment variable"
        print_warning "Add this to your main() function:"
        echo "    port = int(os.environ.get('PORT', 10000))"
        echo "    host = os.environ.get('HOST', '0.0.0.0')"
        echo "    socketio.run(app, host=host, port=port, debug=False)"
    fi
else
    print_warning "gui_app.py doesn't have socketio.run - make sure it's properly configured"
fi

# Step 7: Final instructions
echo ""
print_status "🎉 Render.com deployment preparation completed!"
echo ""
print_warning "NEXT STEPS:"
echo ""
echo "1. Push your code to GitHub:"
echo "   git add ."
echo "   git commit -m 'Prepare for Render deployment'"
echo "   git push origin main"
echo ""
echo "2. Go to Render.com dashboard:"
echo "   https://dashboard.render.com"
echo ""
echo "3. Create new Web Service:"
echo "   - Connect your GitHub repository"
echo "   - Service Name: pionex-trading-bot-gui"
echo "   - Environment: Python 3"
echo "   - Build Command: pip install -r requirements.txt"
echo "   - Start Command: python main.py"
echo ""
echo "4. Add Environment Variables in Render dashboard:"
echo "   - PIONEX_API_KEY=your_actual_pionex_api_key"
echo "   - PIONEX_SECRET_KEY=your_actual_pionex_secret_key"
echo "   - SECRET_KEY=your_random_secret_key"
echo "   - RENDER=true"
echo ""
echo "5. Deploy and wait for build to complete"
echo ""
print_status "Your application will be available at: https://your-app-name.onrender.com"
echo ""
print_status "Deployment preparation script completed!" 