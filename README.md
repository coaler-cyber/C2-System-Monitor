# C2 System Health Monitor 🖥️

Một hệ thống Command & Control (C2) mô phỏng, được thiết kế để giám sát trạng thái phần cứng của các máy trạm phân tán (Windows, Linux) theo thời gian thực. Dự án ứng dụng kiến trúc Client-Server với cơ chế Heartbeat.

## 🌟 Kiến trúc Hệ thống
* **Backend (C2 Server):** Python (Flask), cơ sở dữ liệu SQLite để lưu trữ trạng thái lâu dài.
* **Frontend (Dashboard):** Giao diện Web Dark Mode (Bootstrap 5), sử dụng cơ chế HTTP Polling định kỳ lấy dữ liệu.
* **Client (Agents):** 
  * Máy trạm Linux: Lập trình bằng C++ (libcurl).
  * Máy trạm Windows: Lập trình bằng Python (đóng gói .exe độc lập).

## 🚀 Tính năng nổi bật
* Giao tiếp phi trạng thái (Stateless) qua REST API, giảm tải cho máy chủ.
* Thu thập tự động thông số CPU, RAM, OS từ đa nền tảng.
* Đánh giá trạng thái Online/Offline dựa trên mốc thời gian (Timeout Threshold = 30s).

## ⚙️ Hướng dẫn vận hành Server
1. Cài đặt thư viện: `pip install Flask`
2. Khởi chạy máy chủ: `python server.py`
3. Truy cập Dashboard tại: `http://localhost:5000`