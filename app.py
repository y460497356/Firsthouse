from flask import Flask, render_template, request, jsonify, Response
import time
import json

app = Flask(__name__)

messages = ["系统已就绪", "等待消息..."]
MAX_MESSAGES = 10

@app.route('/')
def index():
    return render_template('index.html')

# --- 新增：消息推送路由 ---
@app.route('/stream')
def stream():
    def generate():
        last_count = len(messages)
        while True:
            # 每隔1秒检查一下消息列表有没有变化
            if len(messages) != last_count:
                # 如果有变化，就把最新的消息列表打包发送出去
                data = json.dumps({'messages': messages})
                yield f"data: {data}\n\n"
                last_count = len(messages)
            time.sleep(1)
    return Response(generate(), mimetype='text/event-stream')
# --- 新增结束 ---

@app.route('/send', methods=['POST'])
def send():
    data = request.get_json()
    if data:
        content = data.get('content')
    else:
        content = request.form.get('content')

    if content:
        print(f"收到消息: {content}")
        messages.append(content)
        if len(messages) > MAX_MESSAGES:
            messages.pop(0)
        return jsonify({'status': 'success', 'messages': messages})
    else:
        return jsonify({'status': 'error', 'message': '内容不能为空'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
