from flask import Blueprint, jsonify, request
from . import get_db

payment_bp = Blueprint('payment', __name__)

ALIPAY_QR_URL = '/static/images/alipay_qr.png'
WECHAT_QR_URL = '/static/images/wechat_qr.png'


@payment_bp.route('/payment/alipay', methods=['GET'])
def alipay_info():
    return jsonify({
        'type': 'alipay',
        'qr_code_url': ALIPAY_QR_URL,
        'name': '支付宝',
        'description': '请使用支付宝扫描二维码进行支付'
    }), 200


@payment_bp.route('/payment/wechat', methods=['GET'])
def wechat_info():
    return jsonify({
        'type': 'wechat',
        'qr_code_url': WECHAT_QR_URL,
        'name': '微信支付',
        'description': '请使用微信扫描二维码进行支付'
    }), 200


@payment_bp.route('/payment/callback', methods=['POST'])
def payment_callback():
    data = request.get_json()
    if not data:
        return jsonify({'error': '无效的请求数据'}), 400

    db = get_db()
    db.execute('INSERT INTO payments (order_id, user_id, amount, payment_method, status, created_at) VALUES (?, ?, ?, ?, ?, ?)',
               (data.get('order_id'), data.get('user_id'), data.get('amount'),
                data.get('payment_method'), data.get('status', 'pending'),
                data.get('created_at', '')))
    db.commit()

    return jsonify({'message': '支付记录已保存'}), 200
