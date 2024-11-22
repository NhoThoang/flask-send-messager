from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_socketio import SocketIO, emit
from flask_socketio import SocketIO, emit, join_room


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Tạo danh sách user tạm thời
users = {
    'user1': {'password': 'pass1'},
    'user2': {'password': 'pass2'},
    'user3': {'password': 'pass3'},
    'user4': {'password': 'pass4'},
    'user5': {'password': 'pass5'}
}

# Lưu tin nhắn (giả sử dùng bộ nhớ tạm)
messages = []

class User(UserMixin):
    def __init__(self, username):
        self.id = username

@login_manager.user_loader
def load_user(user_id):
    return User(user_id) if user_id in users else None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            user = User(username)
            login_user(user)
            return redirect(url_for('index'))
        flash('Sai tên đăng nhập hoặc mật khẩu!')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    return render_template('index.html', username=current_user.id, users=list(users.keys()))

# SocketIO xử lý tin nhắn
@socketio.on('send_message')
def handle_send_message(data):
    sender = data['sender']
    recipient = data['recipient']
    message = data['message']
    messages.append({'sender': sender, 'recipient': recipient, 'message': message})
    emit('receive_message', {'sender': sender, 'message': message}, room=recipient)

@socketio.on('join')
def handle_join(data):
    join_room(data['username'])

if __name__ == '__main__':
    socketio.run(app, debug=True)
