#include <iostream>
#include <string>
#include <thread>
#include <chrono>
#include <curl/curl.h> // Yêu cầu tích hợp thư viện libcurl

// Phân luồng logic theo Hệ điều hành lúc biên dịch
#ifdef _WIN32
    #include <windows.h>
    const std::string OS_NAME = "Windows 10";
    const std::string CLIENT_ID = "Win10_CPP_Client";
#elif __linux__
    #include <sys/sysinfo.h>
    const std::string OS_NAME = "Kali Linux";
    const std::string CLIENT_ID = "Kali_CPP_Client";
#endif

// Địa chỉ IP của máy thật (Server) chạy trên cổng 5000
const std::string SERVER_URL = "http://192.168.113.1:5000/api/heartbeat";

// Hàm mô phỏng trích xuất dữ liệu phần cứng
std::string getSystemData() {
    // Trong báo cáo thực tế, bạn sẽ gọi API của OS tại đây (VD: GlobalMemoryStatusEx trên Win)
    std::string cpu = "20%"; 
    std::string ram = "45%";
    
    // Khởi tạo chuỗi JSON thủ công để tối ưu băng thông và giảm phụ thuộc thư viện
    return "{\"client_id\":\"" + CLIENT_ID + "\", \"os\":\"" + OS_NAME + "\", \"cpu\":\"" + cpu + "\", \"ram\":\"" + ram + "\"}";
}

// Khối xử lý gửi HTTP POST
void sendHeartbeat() {
    CURL *curl = curl_easy_init();
    if(curl) {
        struct curl_slist *headers = NULL;
        headers = curl_slist_append(headers, "Content-Type: application/json");
        
        std::string jsonData = getSystemData();

        curl_easy_setopt(curl, CURLOPT_URL, SERVER_URL.c_str());
        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
        curl_easy_setopt(curl, CURLOPT_POSTFIELDS, jsonData.c_str());

        CURLcode res = curl_easy_perform(curl);
        if(res != CURLE_OK) {
            std::cerr << "[-] Lỗi kết nối mạng: " << curl_easy_strerror(res) << std::endl;
        } else {
            std::cout << "[+] Đã gửi tín hiệu thành công từ " << OS_NAME << std::endl;
        }
        
        curl_slist_free_all(headers);
        curl_easy_cleanup(curl);
    }
}

int main() {
    std::cout << "[*] Bắt đầu khởi động tiến trình giám sát..." << std::endl;
    // Chạy vòng lặp duy trì kết nối (Polling)
    while(true) {
        sendHeartbeat();
        std::this_thread::sleep_for(std::chrono::seconds(5));
    }
    return 0;
}
