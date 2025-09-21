# 🥷 Stealth DDoS - Anti-Detection Tool

Tool DDoS với các tính năng chống phát hiện và tránh bị block IP.

## ✨ Tính năng chính

### 🛡️ Anti-Detection Features
- **Proxy Rotation**: Tự động xoay proxy để thay đổi IP
- **User-Agent Rotation**: Xoay User-Agent để giả mạo trình duyệt
- **IP Header Spoofing**: Giả mạo IP thông qua headers (X-Forwarded-For, X-Real-IP, etc.)
- **Random Delays**: Thêm delay ngẫu nhiên để tránh pattern detection
- **Header Randomization**: Random hóa tất cả headers
- **Path Randomization**: Random attack paths
- **Method Randomization**: Random HTTP methods

### 🚀 Performance Features
- **Multi-threading**: Sync + Async threads
- **Connection Pooling**: Tái sử dụng kết nối
- **Configurable Parameters**: Dễ dàng điều chỉnh

### 📊 Monitoring Features
- **Real-time Statistics**: Theo dõi RPS, success rate
- **Detailed Logging**: Log chi tiết với proxy info
- **Success Rate Tracking**: Theo dõi tỷ lệ thành công

## 📁 File Structure

```
ddos/
├── stealth_ddos.py      # Main attack script (phiên bản mới)
├── index.py             # Original script (đã cập nhật)
├── config.py            # Configuration file
├── proxy_fetcher.py     # Proxy management
├── app.py              # Web interface
├── install_requirements.py # Dependency installer
└── README.md           # This file
```

## 🚀 Quick Start

### 1. Cài đặt dependencies
```bash
python install_requirements.py
```

### 2. Cấu hình target
Chỉnh sửa `config.py`:
```python
TARGET_URL = "https://your-target.com/"
```

### 3. Chạy attack
```bash
# Phiên bản mới (khuyến nghị)
python stealth_ddos.py

# Hoặc phiên bản cũ đã cập nhật
python index.py
```

### 4. Sử dụng Web Interface
```bash
python app.py
```
Truy cập: http://localhost:5000

## ⚙️ Configuration

### Cấu hình cơ bản trong `config.py`:

```python
# Target
TARGET_URL = "https://example.com/"

# Performance
NUM_THREADS = 30          # Số sync threads
ASYNC_THREADS = 8         # Số async threads
CONCURRENT_REQUESTS = 15  # Requests per async thread

# Anti-Detection
USE_PROXIES = True        # Bật proxy rotation
USE_DELAYS = True         # Bật random delays
ROTATE_IP_HEADERS = True  # Bật IP spoofing
USE_FRESH_PROXIES = True  # Tự động lấy proxy mới

# Delays
MIN_DELAY = 0.2          # Delay tối thiểu (giây)
MAX_DELAY = 3.0          # Delay tối đa (giây)
```

## 🔧 Advanced Usage

### Proxy Management
```python
from proxy_fetcher import update_proxy_list, load_saved_proxies

# Lấy proxy mới từ internet
fresh_proxies = update_proxy_list()

# Load proxy đã lưu
saved_proxies = load_saved_proxies()
```

### Custom Headers
Chỉnh sửa `USER_AGENTS`, `REFERERS`, `ACCEPT_LANGUAGES` trong `config.py`

### Performance Tuning
- Tăng `NUM_THREADS` cho nhiều requests hơn
- Giảm `MIN_DELAY`/`MAX_DELAY` cho tốc độ cao hơn
- Tắt `USE_DELAYS` để tốc độ tối đa (rủi ro cao)

## 🛡️ Anti-Detection Strategies

### 1. IP Rotation
- Sử dụng proxy để thay đổi IP
- Tự động refresh proxy list
- Fallback to backup proxies

### 2. Traffic Mimicking
- Random User-Agents (Chrome, Firefox, Safari, Mobile)
- Random Accept-Language headers
- Random Referer headers
- Realistic request patterns

### 3. Timing Randomization
- Random delays between requests
- Random delays between batches
- Avoid predictable patterns

### 4. Header Spoofing
- X-Forwarded-For manipulation
- X-Real-IP spoofing
- Multiple IP header combinations

## 📊 Monitoring

### Real-time Stats
```
📈 Total: 1250 | RPS: 45.2 | Success: 87.3% | Errors: 12.7% | Time: 28.5s
```

### Log Format
```
🔥 #1240 | GET /index.php | 200 | Success: 87.1% via http://proxy:8080
⚡ Async #1241 | /login | 403 | Success: 87.0%
```

## ⚠️ Important Notes

### Legal Disclaimer
- Chỉ sử dụng trên hệ thống bạn sở hữu hoặc có permission
- Tool này chỉ for educational purposes
- Tác giả không chịu tr책nhiệm cho việc sử dụng sai mục đích

### Performance Tips
- Bắt đầu với settings thấp và tăng dần
- Monitor success rate - nếu quá thấp thì giảm intensity
- Sử dụng fresh proxies cho hiệu quả tốt nhất

### Troubleshooting
- Nếu success rate thấp: tăng delays, giảm threads
- Nếu không có proxy: tắt `USE_PROXIES` hoặc update proxy list
- Nếu bị block: tăng delays, enable tất cả anti-detection features

## 🔄 Updates

### Version 2.0 (Stealth)
- ✅ Proxy rotation with auto-refresh
- ✅ Enhanced header randomization
- ✅ IP spoofing via headers
- ✅ Configurable delays
- ✅ Better error handling
- ✅ Real-time statistics
- ✅ Success rate tracking

### Version 1.0 (Original)
- ✅ Basic multi-threading
- ✅ User-Agent rotation
- ✅ Multiple HTTP methods
- ✅ Path randomization

## 🤝 Contributing

Feel free to contribute improvements, especially:
- New proxy sources
- Better anti-detection methods
- Performance optimizations
- Bug fixes

---

**Remember**: Use responsibly and only on systems you own or have explicit permission to test! 🛡️