# config.py
import pymysql


class Config:
    # MySQL数据库连接信息
    MYSQL_HOST = '150.158.121.165'    # 数据库主机地址（本地为127.0.0.1）
    MYSQL_PORT = 53306           # 数据库端口（默认3306）
    MYSQL_USER = 'root'         # 数据库用户名（根据实际情况修改）
    MYSQL_PASSWORD = 'JZh2019@nodejsjava'   # 数据库密码（根据实际情况修改）
    MYSQL_DB = 'todo'           # 数据库名（与前文创建的一致）
    MYSQL_CHARSET = 'utf8mb4'   # 字符集
    # 数据库连接配置 (使用了SQLAlchemy才需要一下两个配置)
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:JZh2019%40nodejsjava@150.158.121.165:53306/todo'  # 连接数据库
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 关闭对象修改追踪


# 开发环境配置（继承Config）
class DevelopmentConfig(Config):
    DEBUG = True  # 开启调试模式

# 生产环境配置（继承Config）
class ProductionConfig(Config):
    DEBUG = False  # 关闭调试模式
    # 生产环境可添加数据库连接池配置，提升性能
    MYSQL_POOL_SIZE = 10
    MYSQL_MAX_OVERFLOW = 20

# 配置映射，方便切换环境
envConf = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


# 数据库连接函数
def get_db_connection():
    try:
        connection = pymysql.connect(
            host=Config.MYSQL_HOST,
            port=Config.MYSQL_PORT,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            db=Config.MYSQL_DB,
            charset=Config.MYSQL_CHARSET,
            cursorclass=pymysql.cursors.DictCursor  # 游标返回字典格式（便于转换为JSON）
        )
        return connection
    except pymysql.Error as e:
        return None

# 关闭数据库连接函数
def close_db_connection(connection, cursor):
    if cursor:
        cursor.close()
    if connection:
        connection.close()
