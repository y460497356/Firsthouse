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
    # 尝试从 form 或 json 中获取 content
    content = request.form.get('content') or request.json.get('content')
    
    if content:
        messages.append(content)
        # 保持最多 10 条消息
        if len(messages) > MAX_MESSAGES:
            messages.pop(0)
        
        # 返回包含 messages 数组的 JSON
        return jsonify({
            'status': 'success',
            'messages': messages
        })
    else:
        return jsonify({
            'status': 'error',
            'message': '内容不能为空'
        }), 400

if __name__ == '__main__':
    app.run(debug=True)
