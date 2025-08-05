#!/bin/bash

# Metadata Generation Fix Script
# This script fixes metadata generation issues during pip installation

echo "🔧 Fixing metadata generation issues..."

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

# Step 2: Upgrade pip to latest version
print_status "Upgrading pip to latest version..."
python -m pip install --upgrade pip

# Step 3: Install build tools
print_status "Installing build tools..."
pip install --upgrade setuptools wheel build

# Step 4: Clear all caches
print_status "Clearing all caches..."
pip cache purge
pip cache info

# Step 5: Install packages one by one to avoid conflicts
print_status "Installing packages one by one..."

# Core packages
print_status "Installing Flask..."
pip install Flask>=2.2.0,<2.4.0

print_status "Installing Flask-SocketIO..."
pip install Flask-SocketIO>=5.2.0,<5.4.0

print_status "Installing Werkzeug..."
pip install Werkzeug>=2.2.0,<2.4.0

print_status "Installing python-socketio..."
pip install python-socketio>=5.7.0,<5.9.0

print_status "Installing python-engineio..."
pip install python-engineio>=4.6.0,<4.8.0

# Environment packages
print_status "Installing python-dotenv..."
pip install python-dotenv>=0.19.0,<1.1.0

print_status "Installing PyYAML..."
pip install PyYAML>=6.0.0,<7.0.0

# Database
print_status "Installing SQLAlchemy..."
pip install SQLAlchemy>=2.0.0,<2.1.0

# HTTP packages
print_status "Installing requests..."
pip install requests>=2.28.0,<2.32.0

print_status "Installing urllib3..."
pip install urllib3>=1.26.0,<2.1.0

# Security
print_status "Installing cryptography..."
pip install cryptography>=40.0.0,<42.0.0

# Data processing (install these last as they're heavy)
print_status "Installing numpy..."
pip install numpy>=1.24.0,<1.27.0

print_status "Installing pandas..."
pip install pandas>=1.5.0,<2.2.0

print_status "Installing scipy..."
pip install scipy>=1.10.0,<1.12.0

# Technical analysis
print_status "Installing ta..."
pip install ta>=0.10.0,<0.11.0

# WebSocket
print_status "Installing websocket-client..."
pip install websocket-client>=1.5.0,<1.7.0

# Utilities
print_status "Installing schedule..."
pip install schedule>=1.2.0,<1.3.0

print_status "Installing psutil..."
pip install psutil>=5.9.0,<5.10.0

# Production server
print_status "Installing gunicorn..."
pip install gunicorn>=20.1.0,<21.3.0

print_status "Installing eventlet..."
pip install eventlet>=0.33.0,<0.34.0

# Step 6: Test installation
print_status "Testing installation..."
python -c "
try:
    import flask
    print(f'✅ Flask imported successfully. Version: {flask.__version__}')
except Exception as e:
    print(f'❌ Flask import failed: {e}')

try:
    from flask_socketio import SocketIO
    print('✅ Flask-SocketIO imported successfully')
except Exception as e:
    print(f'❌ Flask-SocketIO import failed: {e}')

try:
    import pandas
    print(f'✅ Pandas imported successfully. Version: {pandas.__version__}')
except Exception as e:
    print(f'❌ Pandas import failed: {e}')

try:
    import numpy
    print(f'✅ NumPy imported successfully. Version: {numpy.__version__}')
except Exception as e:
    print(f'❌ NumPy import failed: {e}')
"

# Step 7: Create minimal requirements for testing
print_status "Creating minimal requirements for testing..."
cat > requirements_minimal.txt << 'EOF'
# Minimal requirements for testing
Flask>=2.2.0,<2.4.0
Flask-SocketIO>=5.2.0,<5.4.0
python-dotenv>=0.19.0,<1.1.0
requests>=2.28.0,<2.32.0
EOF

# Step 8: Test minimal requirements
print_status "Testing minimal requirements..."
pip install -r requirements_minimal.txt

# Step 9: Final verification
print_status "Final verification..."
python -c "
try:
    from flask import Flask
    from flask_socketio import SocketIO
    import requests
    
    app = Flask(__name__)
    socketio = SocketIO(app)
    
    print('✅ All core packages imported successfully')
    print('✅ Flask app and SocketIO created successfully')
    print('✅ Ready for deployment')
    
except Exception as e:
    print(f'❌ Final verification failed: {e}')
"

echo ""
print_status "🎉 Metadata generation fix completed!"
echo ""
print_warning "If you still have issues:"
echo "1. Try using a different Python version (3.9, 3.10, or 3.11)"
echo "2. Create a fresh virtual environment"
echo "3. Use conda instead of pip if available"
echo "4. Check for system-level package conflicts" 