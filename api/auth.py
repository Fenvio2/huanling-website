from flask import Blueprint, request, jsonify, g
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
import functools
from . import get_db, SECRET_KEY

auth_bp = Blueprint('auth', __name__)


def token_required(f):
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            return jsonify({'error': '缺少认证token'}), 401
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            db = get_db()
            user = db.execute('SELECT id, username, email, role, created_at, last_login FROM users WHERE id = ?',
                              (payload['user_id'],)).fetchone()
            if not user:
                return jsonify({'error': '用户不存在'}), 401
            g.current_user = dict(user)
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'token已过期'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': '无效的token'}), 401
        return f(*args, **kwargs)
    return decorated


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '')

    if not username or not email or not password:
        return jsonify({'error': '用户名、邮箱和密码不能为空'}), 400
    if len(password) < 6:
        return jsonify({'error': '密码长度不能少于6位'}), 400

    db = get_db()
    existing = db.execute('SELECT id FROM users WHERE username = ? OR email = ?',
                          (username, email)).fetchone()
    if existing:
        return jsonify({'error': '用户名或邮箱已被注册'}), 409

    password_hash = generate_password_hash(password)
    now = datetime.datetime.utcnow().isoformat()
    db.execute('INSERT INTO users (username, email, password_hash, role, created_at, last_login) VALUES (?, ?, ?, ?, ?, ?)',
               (username, email, password_hash, 'user', now, now))
    db.commit()
    return jsonify({'message': '注册成功'}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '')

    if not username or not password:
        return jsonify({'error': '用户名和密码不能为空'}), 400

    db = get_db()
    user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    if not user or not check_password_hash(user['password_hash'], password):
        return jsonify({'error': '用户名或密码错误'}), 401

    now = datetime.datetime.utcnow().isoformat()
    db.execute('UPDATE users SET last_login = ? WHERE id = ?', (now, user['id']))
    db.commit()

    token = jwt.encode({
        'user_id': user['id'],
        'username': user['username'],
        'role': user['role'],
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
    }, SECRET_KEY, algorithm='HS256')

    return jsonify({
        'token': token,
        'user': {
            'id': user['id'],
            'username': user['username'],
            'email': user['email'],
            'role': user['role']
        }
    }), 200


@auth_bp.route('/user/profile', methods=['GET'])
@token_required
def get_profile():
    return jsonify({'user': g.current_user}), 200


@auth_bp.route('/user/profile', methods=['PUT'])
@token_required
def update_profile():
    data = request.get_json()
    email = data.get('email', '').strip()
    if not email:
        return jsonify({'error': '邮箱不能为空'}), 400

    db = get_db()
    existing = db.execute('SELECT id FROM users WHERE email = ? AND id != ?',
                          (email, g.current_user['id'])).fetchone()
    if existing:
        return jsonify({'error': '邮箱已被使用'}), 409

    db.execute('UPDATE users SET email = ? WHERE id = ?', (email, g.current_user['id']))
    db.commit()
    return jsonify({'message': '更新成功'}), 200


@auth_bp.route('/logout', methods=['POST'])
@token_required
def logout():
    return jsonify({'message': '已登出'}), 200
