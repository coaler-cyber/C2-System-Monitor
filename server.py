import sqlite3
from datetime import datetime
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
DB_NAME = "monitor.db"

def init_db():
    """Khởi tạo cơ sở dữ liệu và bảng lưu trữ nếu chưa tồn tại."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            client_id TEXT PRIMARY KEY,
            ip TEXT,
            os TEXT,
            cpu TEXT,
            ram TEXT,
            last_seen REAL
        )
    """)
    conn.commit()
    conn.close()

def get_db_connection():
    """Tạo kết nối đến SQLite và trả về kết quả dạng Dictionary (Row-based)."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def dashboard():
    """Hiển thị giao diện Web."""
    return render_template('index.html')

@app.route('/api/heartbeat', methods=['POST'])
def handle_heartbeat():
    """API tiếp nhận tín hiệu từ các Client và ghi đè/cập nhật vào Database."""
    data = request.get_json()
    if not data or 'client_id' not in data:
        return jsonify({"error": "Dữ liệu không hợp lệ"}), 400

    client_id = data['client_id']
    ip = request.remote_addr
    os_name = data.get('os', 'Unknown')
    cpu = data.get('cpu', '0%')
    ram = data.get('ram', '0%')
    last_seen = datetime.now().timestamp()

    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Cập nhật nếu đã có (UPSERT) hoặc chèn mới nếu chưa có
    cursor.execute("""
        INSERT INTO clients (client_id, ip, os, cpu, ram, last_seen)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(client_id) DO UPDATE SET
            ip = excluded.ip,
            os = excluded.os,
            cpu = excluded.cpu,
            ram = excluded.ram,
            last_seen = excluded.last_seen
    """, (client_id, ip, os_name, cpu, ram, last_seen))
    
    conn.commit()
    conn.close()
    return jsonify({"status": "success"}), 200

@app.route('/api/clients', methods=['GET'])
def get_clients():
    """Truy xuất toàn bộ danh sách máy trạm từ Database trả về cho Frontend."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clients")
    rows = cursor.fetchall()
    conn.close()

    # Định dạng lại dữ liệu dạng JSON Key-Value tương thích với giao diện Frontend
    clients_dict = {}
    for row in rows:
        clients_dict[row['client_id']] = {
            "ip": row['ip'],
            "os": row['os'],
            "cpu": row['cpu'],
            "ram": row['ram'],
            "last_seen": row['last_seen']
        }
    return jsonify(clients_dict)

if __name__ == '__main__':
    # Tạo bảng SQLite khi vừa khởi động Server
    init_db()
    # Lắng nghe kết nối trên tất cả các giao diện mạng ở cổng 5000
    app.run(host='0.0.0.0', port=5000, debug=True)