#!/bin/bash

# Flask Installation Fix Script
# This script fixes Flask installation issues

echo "🔧 Fixing Flask installation issues..."

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

# Step 1: Check Python environment
print_status "Checking Python environment..."
python --version
pip --version

# Step 2: Upgrade pip and setuptools
print_status "Upgrading pip and setuptools..."
python -m pip install --upgrade pip setuptools wheel

# Step 3: Clear pip cache
print_status "Clearing pip cache..."
pip cache purge

# Step 4: Install Flask individually
print_status "Installing Flask individually..."
pip install Flask==2.3.3

# Step 5: Install Flask-SocketIO
print_status "Installing Flask-SocketIO..."
pip install Flask-SocketIO==5.3.6

# Step 6: Install other Flask dependencies
print_status "Installing Flask dependencies..."
pip install Werkzeug==2.3.7
pip install python-socketio==5.8.0
pip install python-engineio==4.7.1

# Step 7: Test Flask installation
print_status "Testing Flask installation..."
python -c "
try:
    import flask
    print(f'✅ Flask imported successfully. Version: {flask.__version__}')
except ImportError as e:
    print(f'❌ Flask import failed: {e}')
except Exception as e:
    print(f'❌ Unexpected error: {e}')
"

# Step 8: Install all requirements
print_status "Installing all requirements..."
pip install -r requirements.txt

# Step 9: Test complete installation
print_status "Testing complete installation..."
python test_flask_install.py

# Step 10: Final verification
print_status "Final verification..."
python -c "
try:
    from flask import Flask
    from flask_socketio import SocketIO
    print('✅ Flask and Flask-SocketIO imported successfully')
    
    app = Flask(__name__)
    socketio = SocketIO(app)
    print('✅ Flask app and SocketIO created successfully')
    
except Exception as e:
    print(f'❌ Error: {e}')
"

echo ""
print_status "🎉 Flask installation fix completed!"
echo ""
print_warning "If you still have issues:"
echo "1. Check your Python environment"
echo "2. Try creating a new virtual environment"
echo "3. Make sure you're using the correct Python version"
echo "4. Check for conflicting packages" 