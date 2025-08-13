from flask import Flask, render_template, request, redirect, url_for, session
import config
from parser import parse_log

app = Flask(__name__)
app.secret_key = 'some_random_secret_key'  # 用于 session 加密

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != config.USERNAME or request.form['password'] != config.PASSWORD:
            error = '无效的凭据，请重试。'
        else:
            session['logged_in'] = True
            return redirect(url_for('index'))
    return render_template('login.html', error=error)

@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    chat_messages = parse_log(config.CHAT_LOG_PATH)
    
    # 获取筛选参数
    user_filter = request.args.get('user')
    keyword_filter = request.args.get('keyword')
    
    if user_filter:
        chat_messages = [msg for msg in chat_messages if msg['user'] == user_filter]
    
    if keyword_filter:
        chat_messages = [msg for msg in chat_messages if keyword_filter.lower() in msg['message'].lower()]
        
    # 获取所有独立用户用于筛选下拉菜单
    users = sorted(list(set(msg['user'] for msg in parse_log(config.CHAT_LOG_PATH))))

    return render_template('index.html', messages=chat_messages, users=users, keyword=keyword_filter)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=config.PORT, debug=True)
