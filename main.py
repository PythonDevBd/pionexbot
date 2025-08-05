#!/usr/bin/env python3
"""
Pionex Trading Bot GUI - Main Entry Point
Compatible with multiple deployment platforms
"""

import os
import sys
from pathlib import Path

def main():
    """Main entry point for the GUI"""
    print("🚀 Starting Pionex Trading Bot GUI...")
    
    # Import deployment configuration
    try:
        from deployment_config import DeploymentConfig
        config = DeploymentConfig()
        config.print_environment_info()
        config.setup_directories()
    except ImportError:
        print("⚠️ Deployment config not available, using defaults")
        # Create basic directories
        Path("data").mkdir(exist_ok=True)
        Path("logs").mkdir(exist_ok=True)
    
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