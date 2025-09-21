import requests
import re
import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

def fetch_free_proxies():
    """Lấy danh sách proxy miễn phí từ các nguồn online"""
    proxies = []
    
    # Nguồn 1: Free Proxy List
    try:
        response = requests.get('https://www.proxy-list.download/api/v1/get?type=http', timeout=10)
        if response.status_code == 200:
            proxy_list = response.text.strip().split('\n')
            for proxy in proxy_list:
                if proxy and ':' in proxy:
                    proxies.append(f'http://{proxy.strip()}')
    except:
        pass
    
    # Nguồn 2: ProxyScrape
    try:
        response = requests.get('https://api.proxyscrape.com/v2/?request=get&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all', timeout=10)
        if response.status_code == 200:
            proxy_list = response.text.strip().split('\n')
            for proxy in proxy_list:
                if proxy and ':' in proxy:
                    proxies.append(f'http://{proxy.strip()}')
    except:
        pass
    
    # Nguồn 3: GitHub proxy lists
    try:
        response = requests.get('https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt', timeout=10)
        if response.status_code == 200:
            proxy_list = response.text.strip().split('\n')
            for proxy in proxy_list:
                if proxy and ':' in proxy:
                    proxies.append(f'http://{proxy.strip()}')
    except:
        pass
    
    # Loại bỏ duplicate
    proxies = list(set(proxies))
    
    print(f"✅ Fetched {len(proxies)} proxies from online sources")
    return proxies

def test_proxy(proxy, test_url='http://httpbin.org/ip', timeout=5):
    """Test xem proxy có hoạt động không"""
    try:
        proxies_dict = {'http': proxy, 'https': proxy}
        response = requests.get(test_url, proxies=proxies_dict, timeout=timeout)
        if response.status_code == 200:
            return proxy
    except:
        pass
    return None

def get_working_proxies(proxy_list, max_workers=50, test_count=100):
    """Test và lấy danh sách proxy hoạt động"""
    working_proxies = []
    
    # Chỉ test một số proxy ngẫu nhiên để tiết kiệm thời gian
    test_proxies = random.sample(proxy_list, min(test_count, len(proxy_list)))
    
    print(f"🔍 Testing {len(test_proxies)} proxies...")
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_proxy = {executor.submit(test_proxy, proxy): proxy for proxy in test_proxies}
        
        for future in as_completed(future_to_proxy):
            result = future.result()
            if result:
                working_proxies.append(result)
                print(f"✅ Working proxy found: {result}")
    
    print(f"🎯 Found {len(working_proxies)} working proxies out of {len(test_proxies)} tested")
    return working_proxies

def update_proxy_list():
    """Cập nhật danh sách proxy và trả về danh sách proxy hoạt động"""
    print("🔄 Fetching fresh proxy list...")
    
    # Lấy proxy từ các nguồn online
    all_proxies = fetch_free_proxies()
    
    if not all_proxies:
        print("❌ No proxies found from online sources")
        return []
    
    # Test proxy
    working_proxies = get_working_proxies(all_proxies)
    
    if working_proxies:
        # Lưu vào file để sử dụng sau
        with open('working_proxies.txt', 'w') as f:
            for proxy in working_proxies:
                f.write(proxy + '\n')
        print(f"💾 Saved {len(working_proxies)} working proxies to working_proxies.txt")
    
    return working_proxies

def load_saved_proxies():
    """Load proxy đã lưu từ file"""
    try:
        with open('working_proxies.txt', 'r') as f:
            proxies = [line.strip() for line in f.readlines() if line.strip()]
        print(f"📂 Loaded {len(proxies)} proxies from saved file")
        return proxies
    except FileNotFoundError:
        print("📂 No saved proxy file found")
        return []

if __name__ == "__main__":
    # Test script
    proxies = update_proxy_list()
    print(f"Final result: {len(proxies)} working proxies")