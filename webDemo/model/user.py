# models/user.py
from . import db  # 导入在 __init__.py 中初始化的 db 实例

class User(db.Model):
    __tablename__ = 'users'  # 数据库表名
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    create_time = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())

    # 将模型转换为字典（便于返回JSON）
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'email': self.email,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S')
        }
