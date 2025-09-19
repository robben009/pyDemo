# api.py
import pymysql
from flask import Blueprint, request, jsonify, app

from config import get_db_connection, close_db_connection
from webDemo.model import db
from webDemo.model.user import User

# 创建蓝图
api_bp = Blueprint('api', __name__)


# 新增用户（Flask-SQLAlchemy版）
@api_bp.route('/api/users2', methods=['POST'])
def create_user2():
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


# 查询所有用户（Flask-SQLAlchemy版）
@api_bp.route('/api/users2', methods=['GET'])
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


@api_bp.post('/api/users')
def create_user():
    # 获取请求体JSON数据
    data = request.get_json()
    # 验证必填字段
    required_fields = ['name', 'age', 'email']
    if not all(field in data for field in required_fields):
        return jsonify({'error': '缺少必填字段（name/age/email）'}), 400

    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({'error': '数据库连接失败'}), 500

        cursor = connection.cursor()
        # 执行插入SQL
        sql = "INSERT INTO users (name, age, email) VALUES (%s, %s, %s)"
        cursor.execute(sql, (data['name'], data['age'], data['email']))
        connection.commit()  # 提交事务

        # 获取新增用户的ID，查询并返回完整信息
        user_id = cursor.lastrowid
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        new_user = cursor.fetchone()

        return jsonify({'message': '用户创建成功', 'user': new_user}), 201  # 201表示创建成功

    except pymysql.IntegrityError as e:
        # 处理唯一约束冲突（如email重复）
        connection.rollback()  # 回滚事务
        return jsonify({'error': '邮箱已存在', 'detail': str(e)}), 409
    except Exception as e:
        if connection:
            connection.rollback()
        app.logger.error(f"创建用户失败：{str(e)}")
        return jsonify({'error': '创建用户失败', 'detail': str(e)}), 500
    finally:
        close_db_connection(connection, cursor)


@api_bp.get('/api/users')
def get_all_users():
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({'error': '数据库连接失败'}), 500

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users ORDER BY create_time DESC")
        users = cursor.fetchall()  # 获取所有数据

        return jsonify({'count': len(users), 'users': users}), 200

    except Exception as e:
        app.logger.error(f"查询所有用户失败：{str(e)}")
        return jsonify({'error': '查询用户失败', 'detail': str(e)}), 500
    finally:
        close_db_connection(connection, cursor)


@api_bp.get('/api/users/<int:user_id>')
def get_single_user(user_id):
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({'error': '数据库连接失败'}), 500

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()  # 获取单条数据

        if not user:
            return jsonify({'error': '用户不存在'}), 404

        return jsonify({'user': user}), 200

    except Exception as e:
        app.logger.error(f"查询用户{user_id}失败：{str(e)}")
        return jsonify({'error': '查询用户失败', 'detail': str(e)}), 500
    finally:
        close_db_connection(connection, cursor)


@api_bp.put('/api/users/<int:user_id>')
def update_user(user_id):
    data = request.get_json()
    # 验证至少有一个可更新字段
    update_fields = ['name', 'age', 'email']
    if not any(field in data for field in update_fields):
        return jsonify({'error': '需提供至少一个更新字段（name/age/email）'}), 400

    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({'error': '数据库连接失败'}), 500

        cursor = connection.cursor()
        # 先检查用户是否存在
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        if not cursor.fetchone():
            return jsonify({'error': '用户不存在'}), 404

        # 构建动态更新SQL（避免更新未提供的字段）
        set_clause = ", ".join([f"{field} = %s" for field in data if field in update_fields])
        values = [data[field] for field in data if field in update_fields]
        values.append(user_id)  # 最后添加user_id用于WHERE条件

        sql = f"UPDATE users SET {set_clause} WHERE id = %s"
        cursor.execute(sql, values)
        connection.commit()

        # 查询更新后的用户信息
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        updated_user = cursor.fetchone()

        return jsonify({'message': '用户更新成功', 'user': updated_user}), 200

    except pymysql.IntegrityError as e:
        connection.rollback()
        return jsonify({'error': '邮箱已存在', 'detail': str(e)}), 409
    except Exception as e:
        if connection:
            connection.rollback()
        app.logger.error(f"更新用户{user_id}失败：{str(e)}")
        return jsonify({'error': '更新用户失败', 'detail': str(e)}), 500
    finally:
        close_db_connection(connection, cursor)


@api_bp.delete('/api/users/<int:user_id>')
def delete_user(user_id):
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({'error': '数据库连接失败'}), 500

        cursor = connection.cursor()
        # 检查用户是否存在
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        if not cursor.fetchone():
            return jsonify({'error': '用户不存在'}), 404

        # 执行删除SQL
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        connection.commit()

        return jsonify({'message': f'用户{user_id}删除成功'}), 200

    except Exception as e:
        if connection:
            connection.rollback()
        app.logger.error(f"删除用户{user_id}失败：{str(e)}")
        return jsonify({'error': '删除用户失败', 'detail': str(e)}), 500
    finally:
        close_db_connection(connection, cursor)
