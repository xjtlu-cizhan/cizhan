"""词斩背单词 - 局域网服务器 (iPhone 同 WiFi 访问)

Usage: python server.py  (or double-click start-server.bat)
Open the printed URL on your iPhone, then use Safari's
Share button -> "Add to Home Screen" to install it as an app.
"""
import http.server
import socketserver
import socket
import os
import sys

PORT = 8080

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def lan_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(1)
        s.connect(("223.5.5.5", 80))  # AliDNS, no packets actually sent
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()

    def log_message(self, fmt, *args):
        pass  # quiet


ip = lan_ip()
port = PORT
while True:
    try:
        httpd = socketserver.ThreadingTCPServer(("0.0.0.0", port), Handler)
        break
    except OSError:
        port += 1
        if port > PORT + 20:
            print("No free port found.")
            sys.exit(1)

url = f"http://{ip}:{port}/"
print()
print("=" * 46)
print("  CiZhan Vocabulary Server (词斩背单词)")
print()
print(f"  电脑访问 : {url}")
print(f"  iPhone访问: {url}   (同一 WiFi)")
print()
print("  iPhone 安装到主屏幕:")
print("    Safari 打开 -> 分享按钮 -> 添加到主屏幕")
print("  Ctrl+C 停止服务器")
print("=" * 46)
print()

try:
    import qrcode
    qr = qrcode.QRCode(border=1)
    qr.add_data(url)
    qr.make(fit=True)
    qr.print_ascii(invert=True)
    print()
    print("  (用手机扫码打开)")
except Exception:
    pass

try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print()
    print("Server stopped.")
