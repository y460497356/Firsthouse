from flask import Flask, render_template, request, jsonify
import sys
import os

# --- 核心修改：适配打包后的路径 ---
def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller 创建的临时文件夹路径
        base_path = sys._MEIPASS
    else:
        # 开发环境下的正常路径
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# 使用上面的函数来定位 templates 文件夹
template_folder = get_resource_path('templates')
app = Flask(__name__, template_folder=template_folder)

# 模拟数据库
messages = ["系统已就绪", "等待消息..."]
MAX_MESSAGES = 10

@app.route('/')
def index():
    # 渲染首页
    return render_template('index.html', messages=messages[-MAX_MESSAGES:])

@app.route('/send', methods=['POST'])
def send_message():
    content = request.form.get('content', '').strip()
    if content:
        messages.append(content)
        # 保持只保留最新的10条
        if len(messages) > MAX_MESSAGES:
            messages.pop(0)
    # 返回最新的消息列表给前端
    return jsonify({
        'status': 'success',
        'messages': messages[-MAX_MESSAGES:]
    })

if __name__ == '__main__':
    # host='0.0.0.0' 允许局域网访问
    app.run(debug=True, host='0.0.0.0', port=5000)
