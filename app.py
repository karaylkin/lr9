import os
from flask import Flask, jsonify, request, render_template, send_from_directory
from dotenv import load_dotenv
from functools import wraps
from models import User, BonusLevel
from auth import generate_token, decode_token

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')

# Имитация базы данных
users = {
    'abuser1': User('user1', 'password123', cashback_level=0, spending=500),
    'abuser2': User('user2', 'password123', cashback_level=2, spending=10000)
}

bonus_levels = [
    BonusLevel('Бронза', 0, 1),
    BonusLevel('Серебро', 1000, 3),
    BonusLevel('Золото', 5000, 5),
    BonusLevel('Платина', 10000, 7)
]


def get_bonus_level_by_spending(spending):
    for level in reversed(bonus_levels):
        if spending >= level.threshold:
            return level.name, level.cashback_percent
    return "bronze", 1  # default


def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        if not token.startswith('Bearer '):
            return jsonify({'message': 'Invalid token format'}), 401
        token = token.split(' ')[1]
        username = decode_token(token)
        if not username:
            return jsonify({'message': 'Invalid or expired token'}), 401
        return f(username, *args, **kwargs)

    return decorated_function


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password required'}), 400

    user = users.get(username)
    if not user or user.password != password:
        return jsonify({'message': 'Invalid credentials'}), 401

    token = generate_token(username)
    return jsonify({'token': token})


@app.route('/bonus', methods=['GET'])
@token_required
def get_bonus_info(username):

    user = users.get(username)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    level_name, cashback_percent = get_bonus_level_by_spending(user.spending)
    next_level_index = next((i for i, level in enumerate(bonus_levels) if level.threshold > user.spending), None)
    next_level_name = bonus_levels[next_level_index].name if next_level_index is not None else "max"
    next_level_threshold = bonus_levels[next_level_index].threshold if next_level_index is not None else -1

    return jsonify({
        'username': user.username,
        'current_spending': user.spending,
        'cashback_level_name': level_name,
        'cashback_percent': cashback_percent,
        "next_level_name": next_level_name,
        'next_level_threshold': next_level_threshold
    })


@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)


if __name__ == '__main__':
    app.run(debug=True)
