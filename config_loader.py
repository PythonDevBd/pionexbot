#!/usr/bin/env python3
"""
Configuration Loader for Pionex Trading Bot
Handles loading and validation of configuration files
"""

import os
import yaml
import json
from pathlib import Path
from typing import Dict, Any, Optional

def load_yaml_config(file_path: str = "config.yaml") -> Dict[str, Any]:
    """Load configuration from YAML file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        return config or {}
    except FileNotFoundError:
        print(f"⚠️ Config file not found: {file_path}")
        return {}
    except yaml.YAMLError as e:
        print(f"❌ Error parsing config file: {e}")
        return {}
    except Exception as e:
        print(f"❌ Error loading config: {e}")
        return {}

def load_env_config() -> Dict[str, Any]:
    """Load configuration from environment variables"""
    config = {}
    
    # API Configuration
    config['api'] = {
        'key': os.getenv('PIONEX_API_KEY', ''),
        'secret': os.getenv('PIONEX_SECRET_KEY', ''),
        'base_url': os.getenv('PIONEX_BASE_URL', 'https://api.pionex.com')
    }
    
    # Database Configuration
    config['database'] = {
        'url': os.getenv('DATABASE_URL', 'sqlite:///trading_bot.db'),
        'type': os.getenv('DATABASE_TYPE', 'sqlite')
    }
    
    # GUI Configuration
    config['gui'] = {
        'host': os.getenv('GUI_HOST', '127.0.0.1'),
        'port': int(os.getenv('GUI_PORT', 5000)),
        'debug': os.getenv('GUI_DEBUG', 'false').lower() == 'true'
    }
    
    # Logging Configuration
    config['logging'] = {
        'level': os.getenv('LOG_LEVEL', 'INFO'),
        'file': os.getenv('LOG_FILE', 'logs/trading_bot.log'),
        'max_size': int(os.getenv('LOG_MAX_SIZE', 10 * 1024 * 1024)),  # 10MB
        'backup_count': int(os.getenv('LOG_BACKUP_COUNT', 5))
    }
    
    return config

def get_config(file_path: str = "config.yaml") -> Dict[str, Any]:
    """Get merged configuration from YAML and environment"""
    
    # Load YAML config
    yaml_config = load_yaml_config(file_path)
    
    # Load environment config
    env_config = load_env_config()
    
    # Merge configurations (environment overrides YAML)
    config = {}
    
    # Merge YAML config
    config.update(yaml_config)
    
    # Override with environment config
    for section, values in env_config.items():
        if section not in config:
            config[section] = {}
        config[section].update(values)
    
    # Set defaults for missing sections
    config.setdefault('trading_pair', {
        'symbol': 'BTCUSDT',
        'base_currency': 'BTC',
        'quote_currency': 'USDT'
    })
    
    config.setdefault('position_size', {
        'type': 'fixed',  # 'fixed' or 'percentage'
        'value': 10.0,    # USD amount or percentage
        'max_position': 100.0
    })
    
    config.setdefault('leverage', {
        'value': 1,
        'max_leverage': 10
    })
    
    config.setdefault('risk_management', {
        'stop_loss': 2.0,      # percentage
        'take_profit': 5.0,    # percentage
        'max_daily_loss': 10.0, # percentage
        'max_open_positions': 3
    })
    
    config.setdefault('trading_hours', {
        'enabled': False,
        'start': '09:00',
        'end': '17:00',
        'timezone': 'UTC'
    })
    
    config.setdefault('watchdog', {
        'enabled': True,
        'heartbeat_interval': 30,  # seconds
        'max_failures': 3,
        'auto_restart': True
    })
    
    config.setdefault('notifications', {
        'enabled': False,
        'telegram_bot_token': '',
        'telegram_chat_id': '',
        'email_enabled': False,
        'email_smtp_server': '',
        'email_username': '',
        'email_password': ''
    })
    
    return config

def validate_config(config: Dict[str, Any]) -> bool:
    """Validate configuration"""
    errors = []
    
    # Check API configuration
    api_config = config.get('api', {})
    if not api_config.get('key'):
        errors.append("API key is required")
    if not api_config.get('secret'):
        errors.append("API secret is required")
    
    # Check trading pair
    trading_pair = config.get('trading_pair', {})
    if not trading_pair.get('symbol'):
        errors.append("Trading pair symbol is required")
    
    # Check position size
    position_size = config.get('position_size', {})
    if position_size.get('value', 0) <= 0:
        errors.append("Position size must be greater than 0")
    
    # Check leverage
    leverage = config.get('leverage', {})
    if leverage.get('value', 0) <= 0:
        errors.append("Leverage must be greater than 0")
    
    if errors:
        print("❌ Configuration validation failed:")
        for error in errors:
            print(f"  - {error}")
        return False
    
    return True

def save_config(config: Dict[str, Any], file_path: str = "config.yaml") -> bool:
    """Save configuration to YAML file"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
        return True
    except Exception as e:
        print(f"❌ Error saving config: {e}")
        return False

def create_default_config(file_path: str = "config.yaml") -> bool:
    """Create default configuration file"""
    default_config = {
        'api': {
            'key': 'your_pionex_api_key_here',
            'secret': 'your_pionex_secret_key_here',
            'base_url': 'https://api.pionex.com'
        },
        'database': {
            'url': 'sqlite:///trading_bot.db',
            'type': 'sqlite'
        },
        'gui': {
            'host': '127.0.0.1',
            'port': 5000,
            'debug': False
        },
        'logging': {
            'level': 'INFO',
            'file': 'logs/trading_bot.log',
            'max_size': 10485760,  # 10MB
            'backup_count': 5
        },
        'trading_pair': {
            'symbol': 'BTCUSDT',
            'base_currency': 'BTC',
            'quote_currency': 'USDT'
        },
        'position_size': {
            'type': 'fixed',
            'value': 10.0,
            'max_position': 100.0
        },
        'leverage': {
            'value': 1,
            'max_leverage': 10
        },
        'risk_management': {
            'stop_loss': 2.0,
            'take_profit': 5.0,
            'max_daily_loss': 10.0,
            'max_open_positions': 3
        },
        'trading_hours': {
            'enabled': False,
            'start': '09:00',
            'end': '17:00',
            'timezone': 'UTC'
        },
        'watchdog': {
            'enabled': True,
            'heartbeat_interval': 30,
            'max_failures': 3,
            'auto_restart': True
        },
        'notifications': {
            'enabled': False,
            'telegram_bot_token': '',
            'telegram_chat_id': '',
            'email_enabled': False,
            'email_smtp_server': '',
            'email_username': '',
            'email_password': ''
        }
    }
    
    return save_config(default_config, file_path)

def main():
    """Test configuration loading"""
    print("🔧 Testing configuration loader...")
    
    # Try to load existing config
    config = get_config()
    
    if not config:
        print("⚠️ No config found, creating default...")
        if create_default_config():
            print("✅ Default config created")
            config = get_config()
        else:
            print("❌ Failed to create default config")
            return
    
    # Validate config
    if validate_config(config):
        print("✅ Configuration is valid")
        print(f"📊 Trading pair: {config.get('trading_pair', {}).get('symbol', 'N/A')}")
        print(f"💰 Position size: {config.get('position_size', {}).get('value', 'N/A')}")
        print(f"⚡ Leverage: {config.get('leverage', {}).get('value', 'N/A')}")
    else:
        print("❌ Configuration validation failed")

if __name__ == "__main__":
    main() 