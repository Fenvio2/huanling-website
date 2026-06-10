from flask import Flask, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash
import datetime

from api import init_db, get_db
from api.auth import auth_bp
from api.admin import admin_bp
from api.payment import payment_bp


def create_app():
    app = Flask(__name__)
    CORS(app)

    # 初始化数据库
    init_db()

    # 预置管理员账号
    _seed_admin()

    # 注册蓝图
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(admin_bp, url_prefix='/api')
    app.register_blueprint(payment_bp, url_prefix='/api')

    @app.route('/api/health', methods=['GET'])
    def health():
        return jsonify({'status': 'ok'}), 200

    return app


def _seed_admin():
    db = get_db()
    existing = db.execute('SELECT id FROM users WHERE username = ?', ('18536695765',)).fetchone()
    if not existing:
        password_hash = generate_password_hash('ggj050925@GGJ')
        now = datetime.datetime.utcnow().isoformat()
        db.execute(
            'INSERT INTO users (username, email, password_hash, role, created_at) VALUES (?, ?, ?, ?, ?)',
            ('18536695765', 'admin@huanling.com', password_hash, 'admin', now)
        )
        db.commit()
    db.close()


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
