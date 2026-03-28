from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# 模拟数据库
messages = ["系统已就绪", "等待消息..."]
MAX_MESSAGES = 10

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send():
    # 修正 1: 使用 request.get_json() 处理 JSON 数据
    data = request.get_json()
    if data:
        content = data.get('content')
    else:
        # 修正 2: 如果不是 JSON，尝试从表单中获取
        content = request.form.get('content')

    if content:
        print(f"收到消息: {content}")  # 修正 3: 确保终端有输出
        messages.append(content)
        if len(messages) > MAX_MESSAGES:
            messages.pop(0)
        # 修正 4: 确保返回的消息列表是可序列化的
        return jsonify({'status': 'success', 'messages': messages})
    else:
        return jsonify({'status': 'error', 'message': '内容不能为空'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)  # 修正 5: 关闭调试模式
