import os
import platform
import psutil
import requests
import json

SERVER_URL = 'http://192.168.113.1:5000/api/system-info'

def get_system_info():
    ram_gb = round(psutil.virtual_memory().total / (1024 ** 3), 2)
    
    payload = {
        "username": os.getlogin(),
        "os": platform.system(),
        "os_release": platform.release(),
        "cpu": platform.processor(),
        "ram": ram_gb
    }
    return payload

def send_to_server(data):
    try:
        headers = {'Content-type': 'application/json'}
        response = requests.post(SERVER_URL, data=json.dumps(data), headers=headers)
        
        if response.status_code == 200:
            print("[+] Gửi dữ liệu thành công!")
            print("Server phản hồi:", response.json())
        else:
            print(f"[-] Lỗi Server trả về mã: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("[-] Không thể kết nối. Hãy kiểm tra lại IP Server và cấu hình mạng của máy ảo.")

if __name__ == "__main__":
    sys_data = get_system_info()
    print("Đang chuẩn bị gửi gói dữ liệu:", sys_data)
    send_to_server(sys_data)