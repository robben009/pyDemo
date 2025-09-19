# （Flask-SQLAlchemy版）
from flask import Blueprint, request, jsonify

from webDemo.model import db
from webDemo.model.user import User

# 创建蓝图
api_plus = Blueprint('api_plus', __name__)


# 新增用户
@api_plus.post('/api/users2')
def create_user2():
    print(type(api_plus))
    data = request.get_json()
    required_fields = ['name', 'age', 'email']
    if not all(field in data for field in required_fields):
        return jsonify({'error': '缺少必填字段'}), 400

    try:
        # 创建User对象（无需手动写SQL）
        new_user = User(
            name=data['name'],
            age=data['age'],
            email=data['email']
        )
        db.session.add(new_user)  # 添加到会话
        db.session.commit()  # 提交会话（等同于SQL的COMMIT）
        return jsonify({'message': '用户创建成功', 'user': new_user.to_dict()}), 201
    except Exception as e:
        db.session.rollback()  # 回滚事务
        return jsonify({'error': '创建用户失败', 'detail': str(e)}), 500



# 查询所有用户
@api_plus.get('/api/users2')
def get_all_users2():
    try:
        # 等价于SELECT * FROM users ORDER BY create_time DESC
        users = User.query.order_by(User.create_time.desc()).all()
        return jsonify({
            'count': len(users),
            'users': [user.to_dict() for user in users]
        }), 200
    except Exception as e:
        return jsonify({'error': '查询用户失败', 'detail': str(e)}), 500
