# app.py
from flask import Flask

from api import api_bp  # 导入 api.py 中的蓝图
from config import config
from api_plus import api_plus
from FlaskDemo.model import db

# 初始化Flask应用
app = Flask(__name__)

# 加载配置（默认开发环境）
app.config.from_object(config['default'])

# 注册蓝图
app.register_blueprint(api_bp)
app.register_blueprint(api_plus)

# 初始化 SQLAlchemy 实例
db.init_app(app)

if __name__ == '__main__':
    # 开发环境使用5000端口，生产环境需修改为80/443或其他端口
    app.run(host='0.0.0.0', port=8080, debug=app.config['DEBUG'])
