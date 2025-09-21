# 🚀 NUCLEAR LOAD TESTER

Công cụ kiểm tra tải (load testing) mạnh mẽ với khả năng tạo ra hàng nghìn request đồng thời để kiểm tra khả năng chịu tải của web server.

## ⚠️ CẢNH BÁO QUAN TRỌNG

**CHỈ SỬ DỤNG TRÊN:**
- Server/website mà bạn sở hữu
- Môi trường test/development
- Với sự cho phép rõ ràng từ chủ sở hữu

**KHÔNG SỬ DỤNG ĐỂ:**
- Tấn công website của người khác
- Làm gián đoạn dịch vụ trái phép
- Vi phạm pháp luật

## 🔥 TÍNH NĂNG

### 💥 NUCLEAR ATTACK MODE
- **Multi-Process Architecture**: Tận dụng tất cả CPU cores
- **200 Synchronous Threads**: Không có delay giữa các request
- **20 Asynchronous Threads**: Mỗi thread xử lý 50 request đồng thời
- **Multi-HTTP Methods**: GET, POST, HEAD, OPTIONS
- **Multiple Attack Paths**: 12 đường dẫn khác nhau
- **Random Headers**: 8 User-Agent khác nhau (desktop + mobile)
- **Cache Busting**: Tham số ngẫu nhiên để bypass cache

### 📊 THỐNG KÊ REAL-TIME
- Requests Per Second (RPS)
- Tổng số request đã gửi
- Thời gian chạy
- Peak performance tracking

## 🛠️ CÀI ĐẶT

### Yêu cầu hệ thống
- Python 3.7+
- Windows/Linux/macOS
- RAM: Tối thiểu 4GB (khuyến nghị 8GB+)
- CPU: Multi-core (càng nhiều core càng mạnh)

### Cài đặt dependencies
```bash
pip install requests aiohttp
```

### Tải code
```bash
git clone <repository-url>
cd ddos
```

## 🚀 CÁCH SỬ DỤNG

### 1. Cấu hình target
Mở file `index.py` và chỉnh sửa:
```python
TARGET_URL = "https://your-website.com/"  # Thay bằng URL của bạn
```

### 2. Tùy chỉnh cường độ (tùy chọn)
```python
NUM_THREADS = 200          # Số thread đồng bộ
ASYNC_THREADS = 20         # Số thread bất đồng bộ  
CONCURRENT_REQUESTS = 50   # Request đồng thời mỗi async thread
```

### 3. Chạy chương trình
```bash
python index.py
```

### 4. Dừng chương trình
Nhấn **Ctrl+C** để dừng an toàn

## 📈 HIỂU KẾT QUẢ

### Thống kê hiển thị
```
💥 NUCLEAR STATS: 15420 requests | RPS: 1250 | Time: 12.3s | 🔥ATTACKING🔥
```

- **requests**: Tổng số request đã gửi
- **RPS**: Requests Per Second (request/giây)
- **Time**: Thời gian đã chạy

### Kết quả cuối cùng
```
💀 NUCLEAR ATTACK COMPLETED 💀
   Total Requests Fired: 25680
   Total Attack Time: 20.50 seconds
   Average RPS: 1252.68
   Peak Performance: 1450.00 RPS
```

## ⚙️ TÙY CHỈNH NÂNG CAO

### Thay đổi cường độ tấn công
```python
# Cường độ thấp (testing nhẹ)
NUM_THREADS = 10
ASYNC_THREADS = 2
CONCURRENT_REQUESTS = 10

# Cường độ trung bình
NUM_THREADS = 50
ASYNC_THREADS = 5
CONCURRENT_REQUESTS = 20

# Cường độ cao (NUCLEAR MODE)
NUM_THREADS = 200
ASYNC_THREADS = 20
CONCURRENT_REQUESTS = 50
```

### Thêm đường dẫn tấn công
```python
ATTACK_PATHS = [
    '/',
    '/your-custom-path',
    '/api/endpoint',
    # Thêm các path khác...
]
```

### Thêm User-Agent
```python
USER_AGENTS = [
    'Your-Custom-User-Agent/1.0',
    # Thêm các User-Agent khác...
]
```

## 🔧 TROUBLESHOOTING

### Lỗi thường gặp

**1. "ModuleNotFoundError: No module named 'aiohttp'"**
```bash
pip install aiohttp
```

**2. "Too many open files"**
- Giảm `NUM_THREADS` và `CONCURRENT_REQUESTS`
- Tăng file descriptor limit (Linux/macOS)

**3. "Connection timeout"**
- Target server có thể đã quá tải
- Tăng timeout trong code nếu cần

**4. RPS thấp**
- Kiểm tra kết nối internet
- Target server có thể có rate limiting
- Thử giảm timeout

### Tối ưu hiệu suất

**Tăng RPS:**
- Tăng `NUM_THREADS`
- Tăng `CONCURRENT_REQUESTS`
- Giảm timeout
- Sử dụng máy có nhiều CPU core

**Giảm tải hệ thống:**
- Giảm `NUM_THREADS`
- Giảm `CONCURRENT_REQUESTS`
- Thêm delay giữa các request

## 📊 BENCHMARK

### Hiệu suất tham khảo
| CPU Cores | RAM | Typical RPS | Max RPS |
|-----------|-----|-------------|---------|
| 4 cores   | 8GB | 800-1200   | 2000    |
| 8 cores   | 16GB| 1500-2500  | 4000    |
| 16 cores  | 32GB| 3000-5000  | 8000+   |

*Kết quả thực tế phụ thuộc vào target server và kết nối mạng*

## 🛡️ BẢO MẬT & PHÁP LÝ

### Sử dụng hợp pháp
- ✅ Kiểm tra server của bạn
- ✅ Môi trường development/staging
- ✅ Có permission từ chủ sở hữu
- ✅ Penetration testing hợp pháp

### Không được phép
- ❌ Tấn công website người khác
- ❌ DDoS attack
- ❌ Làm gián đoạn dịch vụ
- ❌ Vi phạm Terms of Service

### Trách nhiệm
Người sử dụng hoàn toàn chịu trách nhiệm về việc sử dụng công cụ này. Tác giả không chịu trách nhiệm về bất kỳ thiệt hại nào.

## 🤝 ĐÓNG GÓP

### Báo lỗi
- Tạo issue trên GitHub
- Mô tả chi tiết lỗi và môi trường

### Đề xuất tính năng
- Fork repository
- Tạo pull request
- Mô tả rõ tính năng mới

## 📝 CHANGELOG

### v2.0 - NUCLEAR MODE
- ✨ Multi-process architecture
- ✨ Multiple HTTP methods
- ✨ Multiple attack paths
- ✨ Enhanced connection pooling
- ✨ Real-time statistics
- 🔧 Improved error handling
- 🔧 Better performance optimization

### v1.0 - Initial Release
- ✨ Basic multi-threading
- ✨ Random headers
- ✨ Basic statistics

## 📄 LICENSE

MIT License - Xem file LICENSE để biết chi tiết.

---

**⚠️ Nhớ: Sức mạnh lớn đi kèm trách nhiệm lớn. Sử dụng có trách nhiệm!**