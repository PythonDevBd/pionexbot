#!/usr/bin/env python3
"""
Test script for Pionex Trading Bot modules
"""

import sys
import os

def test_imports():
    """Test all module imports"""
    print("🔧 Testing module imports...")
    
    # Test config_loader
    try:
        from config_loader import get_config, create_default_config
        print("✅ config_loader imported successfully")
    except Exception as e:
        print(f"❌ config_loader import failed: {e}")
        return False
    
    # Test pionex_api
    try:
        from pionex_api import PionexAPI
        print("✅ pionex_api imported successfully")
    except Exception as e:
        print(f"❌ pionex_api import failed: {e}")
        return False
    
    # Test watchdog
    try:
        from watchdog import start_watchdog, stop_watchdog, get_watchdog_status
        print("✅ watchdog imported successfully")
    except Exception as e:
        print(f"❌ watchdog import failed: {e}")
        return False
    
    return True

def test_config_loader():
    """Test configuration loader"""
    print("\n🔧 Testing configuration loader...")
    
    try:
        from config_loader import get_config, create_default_config
        
        # Create default config if needed
        config = get_config()
        if not config:
            print("⚠️ No config found, creating default...")
            if create_default_config():
                print("✅ Default config created")
                config = get_config()
            else:
                print("❌ Failed to create default config")
                return False
        
        print("✅ Configuration loaded successfully")
        print(f"📊 Trading pair: {config.get('trading_pair', {}).get('symbol', 'N/A')}")
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_pionex_api():
    """Test Pionex API (without actual API calls)"""
    print("\n🔧 Testing Pionex API...")
    
    try:
        from pionex_api import PionexAPI
        
        # Test API class creation (without actual API key)
        try:
            api = PionexAPI("test_key", "test_secret")
            print("✅ PionexAPI class created successfully")
        except ValueError as e:
            print("✅ PionexAPI validation working (expected error for test keys)")
        
        return True
        
    except Exception as e:
        print(f"❌ Pionex API test failed: {e}")
        return False

def test_watchdog():
    """Test watchdog system"""
    print("\n🔧 Testing watchdog system...")
    
    try:
        from watchdog import start_watchdog, stop_watchdog, get_watchdog_status
        
        # Test watchdog functions
        status = get_watchdog_status()
        print("✅ Watchdog status retrieved")
        print(f"📊 Status: {status}")
        
        return True
        
    except Exception as e:
        print(f"❌ Watchdog test failed: {e}")
        return False

def test_gui_import():
    """Test GUI import"""
    print("\n🔧 Testing GUI import...")
    
    try:
        from gui_app import main as gui_main
        print("✅ GUI module imported successfully")
        return True
        
    except Exception as e:
        print(f"❌ GUI import failed: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Pionex Trading Bot Module Tests")
    print("=" * 50)
    
    tests = [
        ("Module Imports", test_imports),
        ("Configuration Loader", test_config_loader),
        ("Pionex API", test_pionex_api),
        ("Watchdog System", test_watchdog),
        ("GUI Import", test_gui_import)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running {test_name} test...")
        if test_func():
            print(f"✅ {test_name} test passed")
            passed += 1
        else:
            print(f"❌ {test_name} test failed")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready.")
        return True
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 