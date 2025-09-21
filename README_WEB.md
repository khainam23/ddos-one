# URL Manager - DDoS Tool Web Interface

## 📋 Mô tả
Website đơn giản để quản lý danh sách URL cho DDoS Tool. Cho phép:
- Thêm URL mới (không trùng lặp)
- Bật/tắt status của URL
- Tự động cập nhật TARGET_URL trong file `index.py` khi có URL được active
- Chỉ một URL có thể active tại một thời điểm

## 🚀 Cách sử dụng

### 1. Khởi chạy web server
```bash
python app.py
```

### 2. Truy cập website
Mở trình duyệt và truy cập: `http://localhost:5000`

### 3. Thêm URL
- Nhập URL vào ô input (có thể nhập với hoặc không có http/https)
- Click "Thêm URL"
- Hệ thống sẽ kiểm tra URL hợp lệ và không trùng lặp

### 4. Quản lý Status
- Click vào toggle switch để bật/tắt status của URL
- Khi bật một URL, tất cả URL khác sẽ tự động tắt
- URL có status=true sẽ được cập nhật vào TARGET_URL trong file `index.py`

### 5. Xóa URL
- Click nút "Xóa" để xóa URL khỏi danh sách

## 📁 Cấu trúc file

```
ddos/
├── app.py              # Web server chính
├── index.py            # DDoS tool (TARGET_URL sẽ được cập nhật tự động)
├── urls.csv            # File lưu trữ danh sách URL và status
├── templates/
│   └── index.html      # Giao diện web
└── requirements.txt    # Danh sách thư viện cần thiết
```

## 🔧 Tính năng

### ✅ Đã hoàn thành
- [x] Giao diện web responsive, đẹp mắt
- [x] Thêm URL với validation
- [x] Kiểm tra URL trùng lặp
- [x] Toggle status với animation
- [x] Tự động cập nhật TARGET_URL trong index.py
- [x] Xóa URL
- [x] Thông báo real-time
- [x] Loading animation
- [x] Lưu trữ dữ liệu trong CSV

### 🎨 Giao diện
- Design hiện đại với gradient và animation
- Responsive trên mọi thiết bị
- Toggle switch đẹp mắt cho status
- Thông báo popup
- Loading spinner
- Empty state khi chưa có URL

### 🔒 Bảo mật
- Validation URL đầu vào
- Kiểm tra trùng lặp
- Xử lý lỗi an toàn

## 🛠️ Cài đặt thư viện

```bash
pip install Flask requests aiohttp
```

## 📝 Lưu ý
- File `urls.csv` sẽ được tạo tự động khi chạy lần đầu
- Chỉ một URL có thể có status=true tại một thời điểm
- Khi thay đổi status, TARGET_URL trong `index.py` sẽ được cập nhật tự động
- Web server chạy trên port 5000 mặc định

## 🎯 Workflow
1. Khởi chạy web server: `python app.py`
2. Truy cập http://localhost:5000
3. Thêm các URL cần test
4. Bật status cho URL muốn attack
5. Chạy DDoS tool: `python index.py`
6. TARGET_URL sẽ tự động được cập nhật theo URL đã chọn

## 🔥 Demo
- Giao diện hiện đại với màu sắc gradient
- Animation mượt mà khi thao tác
- Thông báo real-time khi thực hiện hành động
- Responsive design hoạt động tốt trên mobile và desktop