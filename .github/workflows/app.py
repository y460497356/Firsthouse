from flask import Flask, request, render_template_string
import threading
app = Flask(__name__)
# 简单的 HTML 页面代码（包含在手机端显示的界面）
# 这是一个包含输入框和提交按钮的简单表单
HTML_PAGE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>局域网通信测试</title>
    <style>
        body { font-family: sans-serif; padding: 20px; text-align: center; }
        input[type="text"] { padding: 10px; width: 70%; font-size: 16px; }
        button { padding: 10px 20px; font-size: 16px; background: #007BFF; color: white; border: none; }
        h2 { color: #333; }
    </style>
</head>
<body>
    <h2>📱 手机局域网通信</h2>
    <p>请在下方输入内容并提交：</p>

    
    <!-- 表单提交指向当前地址 -->
    <form action="/" method="POST">
        <input type="text" name="message" placeholder="输入文字..." required autocomplete="off">
        <button type="submit">发送</button>
    </form>
</body>
</html>
"""
# 处理 GET 请求（手机访问页面时）
@app.route('/', methods=['GET'])
def index():
    return render_template_string(HTML_PAGE)

# 处理 POST 请求（手机点击提交时）
@app.route('/', methods=['POST'])
def receive_message():
    # 获取手机发送的 'message' 字段
    msg = request.form.get('message')
    
    # --- 电脑端同步查看的核心代码 ---
    print("-" * 30)
    print(f"📩 收到来自手机的消息: {msg}")
    print("-" * 30)
    
    # 提交后重定向回首页，方便继续输入
    return "消息已发送！<br><a href='/'>返回继续发送</a>"

# 获取本机局域网 IP 的辅助函数
def get_local_ip():
    import socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

if __name__ == '__main__':
    host_ip = get_local_ip()
    port = 5000
    print(f"\n✅ 服务已启动！")
    print(f"🌐 请在手机浏览器输入以下地址访问：")
    print(f"👉  http://{host_ip}:{port}")
    print(f"\n按 Ctrl+C 停止服务\n")
    
    # 启动 Flask 服务，host='0.0.0.0' 允许局域网访问
    app.run(host='0.0.0.0', port=port)
