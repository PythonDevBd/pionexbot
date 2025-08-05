#!/usr/bin/env python3
"""
Flask Installation Test Script
This script tests Flask installation and helps diagnose import issues
"""

import sys
import subprocess
import importlib

def test_pip_install():
    """Test pip installation of Flask"""
    print("🔧 Testing Flask installation...")
    
    try:
        # Try to install Flask
        result = subprocess.run([
            sys.executable, '-m', 'pip', 'install', 'Flask==2.3.3'
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("✅ Flask installed successfully via pip")
            return True
        else:
            print("❌ Flask installation failed:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Error installing Flask: {e}")
        return False

def test_flask_import():
    """Test Flask import"""
    print("🔧 Testing Flask import...")
    
    try:
        import flask
        print(f"✅ Flask imported successfully. Version: {flask.__version__}")
        return True
    except ImportError as e:
        print(f"❌ Flask import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error importing Flask: {e}")
        return False

def test_flask_app():
    """Test Flask app creation"""
    print("🔧 Testing Flask app creation...")
    
    try:
        from flask import Flask
        app = Flask(__name__)
        print("✅ Flask app created successfully")
        return True
    except Exception as e:
        print(f"❌ Flask app creation failed: {e}")
        return False

def test_requirements_install():
    """Test requirements.txt installation"""
    print("🔧 Testing requirements.txt installation...")
    
    try:
        result = subprocess.run([
            sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'
        ], capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0:
            print("✅ Requirements.txt installed successfully")
            return True
        else:
            print("❌ Requirements.txt installation failed:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Error installing requirements: {e}")
        return False

def check_python_version():
    """Check Python version"""
    print(f"🐍 Python version: {sys.version}")
    print(f"🐍 Python executable: {sys.executable}")

def check_installed_packages():
    """Check installed packages"""
    print("📦 Checking installed packages...")
    
    try:
        result = subprocess.run([
            sys.executable, '-m', 'pip', 'list'
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("📦 Installed packages:")
            for line in result.stdout.split('\n'):
                if 'Flask' in line or 'flask' in line:
                    print(f"  {line}")
        else:
            print("❌ Failed to list packages")
    except Exception as e:
        print(f"❌ Error listing packages: {e}")

def main():
    """Main test function"""
    print("🚀 Flask Installation Test Script")
    print("=" * 50)
    
    # Check Python version
    check_python_version()
    print()
    
    # Check installed packages
    check_installed_packages()
    print()
    
    # Test Flask installation
    if test_pip_install():
        print()
        
        # Test Flask import
        if test_flask_import():
            print()
            
            # Test Flask app creation
            test_flask_app()
            print()
    
    # Test requirements.txt
    print("🔧 Testing requirements.txt...")
    test_requirements_install()
    print()
    
    print("🎉 Test completed!")

if __name__ == "__main__":
    main() 