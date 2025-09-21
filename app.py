from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import csv
import os
from urllib.parse import urlparse
import re

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Đường dẫn file CSV
CSV_FILE = 'urls.csv'
INDEX_FILE = 'index.py'

def init_csv():
    """Khởi tạo file CSV nếu chưa tồn tại"""
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['url', 'status'])

def is_valid_url(url):
    """Kiểm tra URL có hợp lệ không"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def url_exists(url):
    """Kiểm tra URL đã tồn tại trong CSV chưa"""
    if not os.path.exists(CSV_FILE):
        return False
    
    with open(CSV_FILE, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['url'] == url:
                return True
    return False

def get_all_urls():
    """Lấy tất cả URL từ CSV"""
    if not os.path.exists(CSV_FILE):
        return []
    
    urls = []
    with open(CSV_FILE, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            urls.append({
                'url': row['url'],
                'status': row['status'].lower() == 'true'
            })
    return urls

def add_url_to_csv(url, status='false'):
    """Thêm URL mới vào CSV"""
    with open(CSV_FILE, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([url, status])

def update_url_status(url, status):
    """Cập nhật status của URL trong CSV"""
    urls = []
    
    # Đọc tất cả dữ liệu
    with open(CSV_FILE, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['url'] == url:
                row['status'] = str(status).lower()
            urls.append(row)
    
    # Ghi lại file
    with open(CSV_FILE, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['url', 'status'])
        writer.writeheader()
        writer.writerows(urls)

def update_target_url_in_index():
    """Cập nhật TARGET_URL trong file index.py với URL có status=true"""
    # Lấy URL đầu tiên có status=true
    target_url = None
    with open(CSV_FILE, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['status'].lower() == 'true':
                target_url = row['url']
                break
    
    if target_url is None:
        return False
    
    # Đọc file index.py
    with open(INDEX_FILE, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Thay thế TARGET_URL
    pattern = r'TARGET_URL\s*=\s*["\'][^"\']*["\']'
    new_line = f'TARGET_URL = "{target_url}"'
    
    if re.search(pattern, content):
        new_content = re.sub(pattern, new_line, content)
        
        # Ghi lại file
        with open(INDEX_FILE, 'w', encoding='utf-8') as file:
            file.write(new_content)
        return True
    
    return False

@app.route('/')
def index():
    """Trang chủ hiển thị danh sách URL"""
    urls = get_all_urls()
    return render_template('index.html', urls=urls)

@app.route('/add', methods=['POST'])
def add_url():
    """Thêm URL mới"""
    url = request.form.get('url', '').strip()
    
    if not url:
        flash('Vui lòng nhập URL!', 'error')
        return redirect(url_for('index'))
    
    # Thêm http:// nếu không có scheme
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    if not is_valid_url(url):
        flash('URL không hợp lệ!', 'error')
        return redirect(url_for('index'))
    
    if url_exists(url):
        flash('URL đã tồn tại!', 'error')
        return redirect(url_for('index'))
    
    add_url_to_csv(url)
    flash('Thêm URL thành công!', 'success')
    return redirect(url_for('index'))

@app.route('/toggle_status', methods=['POST'])
def toggle_status():
    """Thay đổi status của URL"""
    data = request.get_json()
    url = data.get('url')
    status = data.get('status')
    
    if not url:
        return jsonify({'success': False, 'message': 'URL không hợp lệ'})
    
    # Nếu đang bật status=true, tắt tất cả URL khác
    if status:
        urls = get_all_urls()
        for u in urls:
            if u['url'] != url:
                update_url_status(u['url'], False)
    
    update_url_status(url, status)
    
    # Cập nhật TARGET_URL trong index.py nếu có URL active
    if status:
        success = update_target_url_in_index()
        if success:
            return jsonify({'success': True, 'message': 'Cập nhật thành công! TARGET_URL đã được thay đổi trong index.py'})
        else:
            return jsonify({'success': True, 'message': 'Cập nhật status thành công nhưng không thể cập nhật index.py'})
    
    return jsonify({'success': True, 'message': 'Cập nhật status thành công!'})

@app.route('/delete', methods=['POST'])
def delete_url():
    """Xóa URL"""
    data = request.get_json()
    url = data.get('url')
    
    if not url:
        return jsonify({'success': False, 'message': 'URL không hợp lệ'})
    
    # Đọc tất cả URL trừ URL cần xóa
    urls = []
    with open(CSV_FILE, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['url'] != url:
                urls.append(row)
    
    # Ghi lại file
    with open(CSV_FILE, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['url', 'status'])
        writer.writeheader()
        writer.writerows(urls)
    
    return jsonify({'success': True, 'message': 'Xóa URL thành công!'})

if __name__ == '__main__':
    init_csv()
    app.run(debug=True, host='0.0.0.0', port=5000)