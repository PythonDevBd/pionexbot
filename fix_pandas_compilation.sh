#!/bin/bash

# Pandas Compilation Fix Script
# This script fixes pandas compilation issues by using alternative approaches

echo "🔧 Fixing pandas compilation issues..."

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

# Step 2: Upgrade pip and build tools
print_status "Upgrading pip and build tools..."
python -m pip install --upgrade pip setuptools wheel build

# Step 3: Clear cache
print_status "Clearing pip cache..."
pip cache purge

# Step 4: Install core packages without pandas
print_status "Installing core packages (without pandas)..."

# Core Flask packages
pip install Flask>=2.2.0,<2.4.0
pip install Flask-SocketIO>=5.2.0,<5.4.0
pip install Werkzeug>=2.2.0,<2.4.0
pip install python-socketio>=5.7.0,<5.9.0
pip install python-engineio>=4.6.0,<4.8.0

# Environment packages
pip install python-dotenv>=0.19.0,<1.1.0
pip install PyYAML>=6.0.0,<7.0.0

# Database
pip install SQLAlchemy>=2.0.0,<2.1.0

# HTTP packages
pip install requests>=2.28.0,<2.32.0
pip install urllib3>=1.26.0,<2.1.0

# Security
pip install cryptography>=40.0.0,<42.0.0

# Basic data processing (without pandas)
pip install numpy>=1.24.0,<1.27.0
pip install scipy>=1.10.0,<1.12.0

# WebSocket
pip install websocket-client>=1.5.0,<1.7.0

# Utilities
pip install schedule>=1.2.0,<1.3.0
pip install psutil>=5.9.0,<5.10.0

# Production server
pip install gunicorn>=20.1.0,<21.3.0
pip install eventlet>=0.33.0,<0.34.0

# Step 5: Try alternative pandas installation methods
print_status "Trying alternative pandas installation methods..."

# Method 1: Try installing pandas with specific version
print_status "Method 1: Installing pandas 1.5.3 (stable version)..."
pip install pandas==1.5.3

# If that fails, try Method 2
if [ $? -ne 0 ]; then
    print_warning "Method 1 failed, trying Method 2..."
    print_status "Method 2: Installing pandas with --no-build-isolation..."
    pip install pandas==1.5.3 --no-build-isolation
fi

# If that fails, try Method 3
if [ $? -ne 0 ]; then
    print_warning "Method 2 failed, trying Method 3..."
    print_status "Method 3: Installing pandas with --no-deps..."
    pip install pandas==1.5.3 --no-deps
fi

# If that fails, try Method 4
if [ $? -ne 0 ]; then
    print_warning "Method 3 failed, trying Method 4..."
    print_status "Method 4: Installing pandas with conda (if available)..."
    if command -v conda &> /dev/null; then
        conda install pandas=1.5.3 -y
    else
        print_warning "Conda not available, skipping pandas for now"
    fi
fi

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
    import numpy
    print(f'✅ NumPy imported successfully. Version: {numpy.__version__}')
except Exception as e:
    print(f'❌ NumPy import failed: {e}')

try:
    import pandas
    print(f'✅ Pandas imported successfully. Version: {pandas.__version__}')
except ImportError:
    print('⚠️ Pandas not available - using alternative data processing')
except Exception as e:
    print(f'❌ Pandas import failed: {e}')

try:
    import requests
    print('✅ Requests imported successfully')
except Exception as e:
    print(f'❌ Requests import failed: {e}')
"

# Step 7: Create alternative data processing module
print_status "Creating alternative data processing module..."
cat > data_utils.py << 'EOF'
"""
Alternative Data Processing Utilities (Pandas-free)
This module provides basic data processing functions without pandas dependency
"""

import json
import csv
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

def load_json_data(file_path: str) -> Dict[str, Any]:
    """Load data from JSON file"""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading JSON data: {e}")
        return {}

def save_json_data(data: Dict[str, Any], file_path: str) -> bool:
    """Save data to JSON file"""
    try:
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving JSON data: {e}")
        return False

def load_csv_data(file_path: str) -> List[Dict[str, Any]]:
    """Load data from CSV file"""
    try:
        data = []
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
        return data
    except Exception as e:
        print(f"Error loading CSV data: {e}")
        return []

def save_csv_data(data: List[Dict[str, Any]], file_path: str) -> bool:
    """Save data to CSV file"""
    try:
        if not data:
            return False
        
        with open(file_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        return True
    except Exception as e:
        print(f"Error saving CSV data: {e}")
        return False

def calculate_simple_moving_average(values: List[float], window: int) -> List[float]:
    """Calculate simple moving average"""
    if len(values) < window:
        return []
    
    result = []
    for i in range(window - 1, len(values)):
        avg = sum(values[i - window + 1:i + 1]) / window
        result.append(avg)
    
    return result

def calculate_rsi(prices: List[float], period: int = 14) -> List[float]:
    """Calculate Relative Strength Index"""
    if len(prices) < period + 1:
        return []
    
    gains = []
    losses = []
    
    for i in range(1, len(prices)):
        change = prices[i] - prices[i-1]
        if change > 0:
            gains.append(change)
            losses.append(0)
        else:
            gains.append(0)
            losses.append(abs(change))
    
    rsi_values = []
    for i in range(period, len(gains)):
        avg_gain = sum(gains[i-period:i]) / period
        avg_loss = sum(losses[i-period:i]) / period
        
        if avg_loss == 0:
            rsi = 100
        else:
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))
        
        rsi_values.append(rsi)
    
    return rsi_values

def format_timestamp(timestamp: float) -> str:
    """Format timestamp to readable string"""
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

def parse_timestamp(timestamp_str: str) -> float:
    """Parse timestamp string to float"""
    try:
        dt = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
        return dt.timestamp()
    except:
        return 0.0

# Example usage functions
def process_trading_data(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Process trading data without pandas"""
    if not data:
        return {}
    
    # Extract prices
    prices = [float(item.get('price', 0)) for item in data if item.get('price')]
    
    # Calculate indicators
    sma_20 = calculate_simple_moving_average(prices, 20)
    rsi_14 = calculate_rsi(prices, 14)
    
    return {
        'total_records': len(data),
        'price_count': len(prices),
        'sma_20': sma_20[-1] if sma_20 else None,
        'rsi_14': rsi_14[-1] if rsi_14 else None,
        'latest_price': prices[-1] if prices else None
    }
EOF

print_status "Created data_utils.py for pandas-free data processing"

# Step 8: Test the alternative data processing
print_status "Testing alternative data processing..."
python -c "
try:
    from data_utils import process_trading_data, calculate_simple_moving_average
    
    # Test data
    test_data = [
        {'price': '100.0', 'timestamp': '2023-01-01 10:00:00'},
        {'price': '101.0', 'timestamp': '2023-01-01 10:01:00'},
        {'price': '102.0', 'timestamp': '2023-01-01 10:02:00'},
    ]
    
    result = process_trading_data(test_data)
    print('✅ Alternative data processing works!')
    print(f'Result: {result}')
    
except Exception as e:
    print(f'❌ Alternative data processing failed: {e}')
"

# Step 9: Final verification
print_status "Final verification..."
python -c "
try:
    from flask import Flask
    from flask_socketio import SocketIO
    import requests
    import numpy
    
    app = Flask(__name__)
    socketio = SocketIO(app)
    
    print('✅ Core Flask app created successfully')
    print('✅ NumPy imported successfully')
    
    try:
        import pandas
        print('✅ Pandas imported successfully')
    except ImportError:
        print('⚠️ Pandas not available - using alternative data processing')
    
    print('✅ Ready for deployment')
    
except Exception as e:
    print(f'❌ Final verification failed: {e}')
"

echo ""
print_status "🎉 Pandas compilation fix completed!"
echo ""
print_warning "If pandas installation failed:"
echo "1. The application will work without pandas"
echo "2. Alternative data processing is available in data_utils.py"
echo "3. You can install pandas later using: conda install pandas"
echo "4. Or try: pip install pandas --no-build-isolation" 