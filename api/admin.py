from flask import Blueprint, request, jsonify, g
from werkzeug.security import check_password_hash
import jwt
import datetime
import functools
from . import get_db, SECRET_KEY

admin_bp = Blueprint('admin', __name__)


def admin_required(f):
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            return jsonify({'error': '缺少认证token'}), 401
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            if payload.get('role') != 'admin':
                return jsonify({'error': '需要管理员权限'}), 403
            g.current_admin = payload
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'token已过期'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': '无效的token'}), 401
        return f(*args, **kwargs)
    return decorated


@admin_bp.route('/admin/login', methods=['POST'])
def admin_login():
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '')

    if not username or not password:
        return jsonify({'error': '用户名和密码不能为空'}), 400

    db = get_db()
    user = db.execute('SELECT * FROM users WHERE username = ? AND role = ?',
                      (username, 'admin')).fetchone()
    if not user or not check_password_hash(user['password_hash'], password):
        return jsonify({'error': '管理员账号或密码错误'}), 401

    token = jwt.encode({
        'user_id': user['id'],
        'username': user['username'],
        'role': user['role'],
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
    }, SECRET_KEY, algorithm='HS256')

    return jsonify({
        'token': token,
        'user': {
            'id': user['id'],
            'username': user['username'],
            'role': user['role']
        }
    }), 200


@admin_bp.route('/admin/users', methods=['GET'])
@admin_required
def get_users():
    db = get_db()
    users = db.execute('SELECT id, username, email, role, created_at, last_login FROM users ORDER BY id DESC').fetchall()
    return jsonify({'users': [dict(u) for u in users]}), 200


@admin_bp.route('/admin/stats', methods=['GET'])
@admin_required
def get_stats():
    db = get_db()
    total_users = db.execute('SELECT COUNT(*) FROM users WHERE role != ?', ('admin',)).fetchone()[0]
    today = datetime.datetime.utcnow().strftime('%Y-%m-%d')
    today_users = db.execute("SELECT COUNT(*) FROM users WHERE role != ? AND date(created_at) = ?",
                             ('admin', today)).fetchone()[0]
    active_users = db.execute("SELECT COUNT(*) FROM users WHERE role != ? AND last_login IS NOT NULL",
                              ('admin',)).fetchone()[0]

    return jsonify({
        'total_users': total_users,
        'today_registrations': today_users,
        'active_users': active_users
    }), 200


@admin_bp.route('/admin/users/<int:user_id>', methods=['DELETE'])
@admin_required
def delete_user(user_id):
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    if not user:
        return jsonify({'error': '用户不存在'}), 404
    if user['role'] == 'admin':
        return jsonify({'error': '不能删除管理员账号'}), 403
    db.execute('DELETE FROM users WHERE id = ?', (user_id,))
    db.commit()
    return jsonify({'message': '用户已删除'}), 200
