#!/usr/bin/env python3
"""
Pionex API Client
Handles communication with Pionex trading API
"""

import os
import time
import hmac
import hashlib
import requests
import json
from typing import Dict, Any, Optional, List
from urllib.parse import urlencode

class PionexAPI:
    """Pionex API client for trading operations"""
    
    def __init__(self, api_key: str = None, secret_key: str = None, base_url: str = None):
        """Initialize API client"""
        self.api_key = api_key or os.getenv('PIONEX_API_KEY', '')
        self.secret_key = secret_key or os.getenv('PIONEX_SECRET_KEY', '')
        self.base_url = base_url or os.getenv('PIONEX_BASE_URL', 'https://api.pionex.com')
        
        if not self.api_key or not self.secret_key:
            raise ValueError("API key and secret key are required")
    
    def _generate_signature(self, timestamp: str, method: str, path: str, params: Dict = None, body: Dict = None) -> str:
        """Generate HMAC signature for API requests"""
        # Create string to sign
        string_to_sign = f"{timestamp}{method}{path}"
        
        if params:
            sorted_params = sorted(params.items())
            query_string = urlencode(sorted_params)
            string_to_sign += f"?{query_string}"
        
        if body:
            string_to_sign += json.dumps(body)
        
        # Generate HMAC signature
        signature = hmac.new(
            self.secret_key.encode('utf-8'),
            string_to_sign.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        return signature
    
    def _make_request(self, method: str, endpoint: str, params: Dict = None, data: Dict = None) -> Dict[str, Any]:
        """Make API request with authentication"""
        url = f"{self.base_url}{endpoint}"
        timestamp = str(int(time.time() * 1000))
        
        # Generate signature
        signature = self._generate_signature(timestamp, method, endpoint, params, data)
        
        # Prepare headers
        headers = {
            'Content-Type': 'application/json',
            'X-PIONEX-API-KEY': self.api_key,
            'X-PIONEX-TIMESTAMP': timestamp,
            'X-PIONEX-SIGNATURE': signature
        }
        
        try:
            if method.upper() == 'GET':
                response = requests.get(url, params=params, headers=headers, timeout=10)
            elif method.upper() == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=10)
            elif method.upper() == 'DELETE':
                response = requests.delete(url, params=params, headers=headers, timeout=10)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            return {'error': f"Request failed: {str(e)}"}
        except json.JSONDecodeError as e:
            return {'error': f"Invalid JSON response: {str(e)}"}
        except Exception as e:
            return {'error': f"Unexpected error: {str(e)}"}
    
    def test_connection(self) -> Dict[str, Any]:
        """Test API connection by getting account info"""
        return self._make_request('GET', '/api/v1/account')
    
    def get_account_info(self) -> Dict[str, Any]:
        """Get account information"""
        return self._make_request('GET', '/api/v1/account')
    
    def get_balance(self) -> Dict[str, Any]:
        """Get account balance"""
        return self._make_request('GET', '/api/v1/account/balance')
    
    def get_positions(self, symbol: str = None) -> Dict[str, Any]:
        """Get open positions"""
        params = {}
        if symbol:
            params['symbol'] = symbol
        return self._make_request('GET', '/api/v1/position', params=params)
    
    def get_orders(self, symbol: str = None, status: str = None) -> Dict[str, Any]:
        """Get orders"""
        params = {}
        if symbol:
            params['symbol'] = symbol
        if status:
            params['status'] = status
        return self._make_request('GET', '/api/v1/order', params=params)
    
    def place_order(self, symbol: str, side: str, order_type: str, quantity: float, 
                   price: float = None, stop_price: float = None) -> Dict[str, Any]:
        """Place a new order"""
        data = {
            'symbol': symbol,
            'side': side.upper(),
            'type': order_type.upper(),
            'quantity': quantity
        }
        
        if price:
            data['price'] = price
        if stop_price:
            data['stopPrice'] = stop_price
        
        return self._make_request('POST', '/api/v1/order', data=data)
    
    def cancel_order(self, order_id: str) -> Dict[str, Any]:
        """Cancel an order"""
        params = {'orderId': order_id}
        return self._make_request('DELETE', '/api/v1/order', params=params)
    
    def get_ticker(self, symbol: str) -> Dict[str, Any]:
        """Get ticker information"""
        params = {'symbol': symbol}
        return self._make_request('GET', '/api/v1/market/ticker', params=params)
    
    def get_klines(self, symbol: str, interval: str, limit: int = 100) -> Dict[str, Any]:
        """Get kline/candlestick data"""
        params = {
            'symbol': symbol,
            'interval': interval,
            'limit': limit
        }
        return self._make_request('GET', '/api/v1/market/klines', params=params)
    
    def get_symbols(self) -> Dict[str, Any]:
        """Get available trading symbols"""
        return self._make_request('GET', '/api/v1/market/symbols')
    
    def get_server_time(self) -> Dict[str, Any]:
        """Get server time"""
        return self._make_request('GET', '/api/v1/time')
    
    def get_exchange_info(self) -> Dict[str, Any]:
        """Get exchange information"""
        return self._make_request('GET', '/api/v1/market/exchangeInfo')

def test_api_connection():
    """Test API connection"""
    try:
        api = PionexAPI()
        result = api.test_connection()
        
        if 'error' in result:
            print(f"❌ API connection failed: {result['error']}")
            return False
        else:
            print("✅ API connection successful")
            return True
            
    except Exception as e:
        print(f"❌ API connection error: {e}")
        return False

def main():
    """Test API functionality"""
    print("🔧 Testing Pionex API...")
    
    if test_api_connection():
        print("✅ API is working correctly")
    else:
        print("❌ API test failed")

if __name__ == "__main__":
    main() 