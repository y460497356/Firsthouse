from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# 模拟数据库 (全局变量)
messages = ["系统已就绪", "等待消息..."]
MAX_MESSAGES = 10

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send():
    # 1. 获取数据
    content = request.form.get('content')
    
    if content:
        messages.append(content)
        # 保持最多 10 条消息
        if len(messages) > MAX_MESSAGES:
            messages.pop(0)
        
        # 2. 打印到终端 (确保你能在运行窗口看到)
        print(f"📱 收到新消息: {content}")
        print(f"💬 当前消息列表: {messages}")
        
        return jsonify({'status': 'success', 'messages': messages})
    else:
        return jsonify({'status': 'error', 'message': '内容不能为空'})

if __name__ == '__main__':
    # 3. 关键修改：关闭 debug 模式，并监听 0.0.0.0
    # threaded=True 确保多用户访问时不会卡死
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
