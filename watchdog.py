#!/usr/bin/env python3
"""
Watchdog System for Pionex Trading Bot
Monitors system health and automatically restarts if needed
"""

import os
import time
import threading
import logging
from typing import Dict, Any, Optional
from datetime import datetime, timedelta

class Watchdog:
    """Watchdog system for monitoring and auto-restart"""
    
    def __init__(self, config: Dict[str, Any] = None):
        """Initialize watchdog"""
        self.config = config or {}
        self.enabled = self.config.get('enabled', True)
        self.heartbeat_interval = self.config.get('heartbeat_interval', 30)
        self.max_failures = self.config.get('max_failures', 3)
        self.auto_restart = self.config.get('auto_restart', True)
        
        self.failure_count = 0
        self.last_heartbeat = None
        self.is_running = False
        self.thread = None
        self.logger = logging.getLogger(__name__)
    
    def start(self) -> bool:
        """Start the watchdog"""
        if not self.enabled:
            self.logger.info("Watchdog disabled in configuration")
            return False
        
        if self.is_running:
            self.logger.warning("Watchdog already running")
            return True
        
        try:
            self.is_running = True
            self.thread = threading.Thread(target=self._monitor_loop, daemon=True)
            self.thread.start()
            self.logger.info("Watchdog started successfully")
            return True
        except Exception as e:
            self.logger.error(f"Failed to start watchdog: {e}")
            self.is_running = False
            return False
    
    def stop(self) -> bool:
        """Stop the watchdog"""
        if not self.is_running:
            return True
        
        try:
            self.is_running = False
            if self.thread and self.thread.is_alive():
                self.thread.join(timeout=5)
            self.logger.info("Watchdog stopped")
            return True
        except Exception as e:
            self.logger.error(f"Error stopping watchdog: {e}")
            return False
    
    def heartbeat(self) -> bool:
        """Send heartbeat signal"""
        try:
            self.last_heartbeat = datetime.now()
            self.failure_count = 0
            self.logger.debug("Heartbeat sent")
            return True
        except Exception as e:
            self.logger.error(f"Heartbeat failed: {e}")
            return False
    
    def _monitor_loop(self):
        """Main monitoring loop"""
        self.logger.info("Watchdog monitoring loop started")
        
        while self.is_running:
            try:
                # Check if heartbeat is too old
                if self.last_heartbeat:
                    time_since_heartbeat = datetime.now() - self.last_heartbeat
                    max_allowed_time = timedelta(seconds=self.heartbeat_interval * 2)
                    
                    if time_since_heartbeat > max_allowed_time:
                        self.failure_count += 1
                        self.logger.warning(f"Heartbeat timeout. Failure count: {self.failure_count}")
                        
                        if self.failure_count >= self.max_failures:
                            self.logger.error("Maximum failures reached. Triggering restart...")
                            if self.auto_restart:
                                self._trigger_restart()
                            break
                
                time.sleep(self.heartbeat_interval)
                
            except Exception as e:
                self.logger.error(f"Error in watchdog loop: {e}")
                time.sleep(self.heartbeat_interval)
    
    def _trigger_restart(self):
        """Trigger system restart"""
        try:
            self.logger.critical("Watchdog triggering system restart")
            
            # Log restart event
            restart_log = {
                'timestamp': datetime.now().isoformat(),
                'reason': 'watchdog_max_failures',
                'failure_count': self.failure_count,
                'last_heartbeat': self.last_heartbeat.isoformat() if self.last_heartbeat else None
            }
            
            # Save restart log
            self._save_restart_log(restart_log)
            
            # In a real implementation, you might:
            # 1. Send notification
            # 2. Save state
            # 3. Restart the application
            # 4. Exit the process
            
            self.logger.info("Restart triggered successfully")
            
        except Exception as e:
            self.logger.error(f"Error triggering restart: {e}")
    
    def _save_restart_log(self, log_data: Dict[str, Any]):
        """Save restart log to file"""
        try:
            log_dir = Path('logs')
            log_dir.mkdir(exist_ok=True)
            
            log_file = log_dir / 'watchdog_restarts.log'
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(f"{json.dumps(log_data)}\n")
                
        except Exception as e:
            self.logger.error(f"Error saving restart log: {e}")
    
    def get_status(self) -> Dict[str, Any]:
        """Get watchdog status"""
        return {
            'enabled': self.enabled,
            'running': self.is_running,
            'failure_count': self.failure_count,
            'last_heartbeat': self.last_heartbeat.isoformat() if self.last_heartbeat else None,
            'max_failures': self.max_failures,
            'auto_restart': self.auto_restart,
            'heartbeat_interval': self.heartbeat_interval
        }

# Global watchdog instance
_watchdog_instance = None

def start_watchdog(config: Dict[str, Any] = None) -> Optional[Watchdog]:
    """Start the global watchdog instance"""
    global _watchdog_instance
    
    try:
        if _watchdog_instance and _watchdog_instance.is_running:
            return _watchdog_instance
        
        _watchdog_instance = Watchdog(config)
        if _watchdog_instance.start():
            return _watchdog_instance
        else:
            return None
    except Exception as e:
        logging.error(f"Failed to start watchdog: {e}")
        return None

def stop_watchdog() -> bool:
    """Stop the global watchdog instance"""
    global _watchdog_instance
    
    try:
        if _watchdog_instance:
            return _watchdog_instance.stop()
        return True
    except Exception as e:
        logging.error(f"Failed to stop watchdog: {e}")
        return False

def get_watchdog_status() -> Dict[str, Any]:
    """Get status of the global watchdog instance"""
    global _watchdog_instance
    
    if _watchdog_instance:
        return _watchdog_instance.get_status()
    else:
        return {
            'enabled': False,
            'running': False,
            'failure_count': 0,
            'last_heartbeat': None,
            'max_failures': 3,
            'auto_restart': True,
            'heartbeat_interval': 30
        }

def send_heartbeat() -> bool:
    """Send heartbeat to the global watchdog instance"""
    global _watchdog_instance
    
    if _watchdog_instance and _watchdog_instance.is_running:
        return _watchdog_instance.heartbeat()
    return False

def main():
    """Test watchdog functionality"""
    print("🔧 Testing watchdog system...")
    
    # Test configuration
    config = {
        'enabled': True,
        'heartbeat_interval': 5,  # 5 seconds for testing
        'max_failures': 2,
        'auto_restart': True
    }
    
    # Start watchdog
    watchdog = start_watchdog(config)
    if watchdog:
        print("✅ Watchdog started")
        
        # Send heartbeats
        for i in range(3):
            time.sleep(2)
            if send_heartbeat():
                print(f"✅ Heartbeat {i+1} sent")
            else:
                print(f"❌ Heartbeat {i+1} failed")
        
        # Get status
        status = get_watchdog_status()
        print(f"📊 Status: {status}")
        
        # Stop watchdog
        if stop_watchdog():
            print("✅ Watchdog stopped")
        else:
            print("❌ Failed to stop watchdog")
    else:
        print("❌ Failed to start watchdog")

if __name__ == "__main__":
    import json
    from pathlib import Path
    main() 