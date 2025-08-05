#!/usr/bin/env python3
"""
Deployment Configuration for Pionex Trading Bot GUI
This file handles different deployment environments and configurations
"""

import os
import sys
from pathlib import Path

class DeploymentConfig:
    """Configuration class for different deployment environments"""
    
    def __init__(self):
        self.environment = self._detect_environment()
        self.config = self._get_config()
    
    def _detect_environment(self):
        """Detect the deployment environment"""
        if os.environ.get('RENDER'):
            return 'render'
        elif os.environ.get('HEROKU'):
            return 'heroku'
        elif os.environ.get('RAILWAY'):
            return 'railway'
        elif os.environ.get('DIGITALOCEAN'):
            return 'digitalocean'
        else:
            return 'local'
    
    def _get_config(self):
        """Get configuration based on environment"""
        base_config = {
            'host': '127.0.0.1',
            'port': 5000,
            'debug': True,
            'data_dir': 'data',
            'logs_dir': 'logs',
            'database_url': 'sqlite:///trading_bot.db'
        }
        
        if self.environment == 'render':
            return {
                'host': '0.0.0.0',
                'port': int(os.environ.get('PORT', 10000)),
                'debug': False,
                'data_dir': 'data',
                'logs_dir': 'logs',
                'database_url': 'sqlite:///data/trading_bot.db'
            }
        elif self.environment == 'heroku':
            return {
                'host': '0.0.0.0',
                'port': int(os.environ.get('PORT', 5000)),
                'debug': False,
                'data_dir': 'data',
                'logs_dir': 'logs',
                'database_url': os.environ.get('DATABASE_URL', 'sqlite:///data/trading_bot.db')
            }
        elif self.environment == 'railway':
            return {
                'host': '0.0.0.0',
                'port': int(os.environ.get('PORT', 5000)),
                'debug': False,
                'data_dir': 'data',
                'logs_dir': 'logs',
                'database_url': os.environ.get('DATABASE_URL', 'sqlite:///data/trading_bot.db')
            }
        elif self.environment == 'digitalocean':
            return {
                'host': '0.0.0.0',
                'port': int(os.environ.get('PORT', 5000)),
                'debug': False,
                'data_dir': 'data',
                'logs_dir': 'logs',
                'database_url': 'sqlite:///data/trading_bot.db'
            }
        else:
            return base_config
    
    def setup_directories(self):
        """Create necessary directories"""
        data_dir = Path(self.config['data_dir'])
        logs_dir = Path(self.config['logs_dir'])
        
        data_dir.mkdir(exist_ok=True)
        logs_dir.mkdir(exist_ok=True)
        
        print(f"📁 Data directory: {data_dir.absolute()}")
        print(f"📁 Logs directory: {logs_dir.absolute()}")
    
    def get_flask_config(self):
        """Get Flask configuration"""
        return {
            'host': self.config['host'],
            'port': self.config['port'],
            'debug': self.config['debug']
        }
    
    def print_environment_info(self):
        """Print environment information"""
        print(f"🌍 Environment: {self.environment}")
        print(f"🏠 Host: {self.config['host']}")
        print(f"🚪 Port: {self.config['port']}")
        print(f"🐛 Debug: {self.config['debug']}")
        print(f"💾 Database: {self.config['database_url']}")

def main():
    """Main function to test deployment configuration"""
    config = DeploymentConfig()
    config.print_environment_info()
    config.setup_directories()
    
    print("\n✅ Deployment configuration ready!")
    return config

if __name__ == "__main__":
    main() 