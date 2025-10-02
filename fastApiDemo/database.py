# database.py
from sqlmodel import create_engine

# 数据库连接URL格式：postgresql://用户名:密码@主机:端口/数据库名
# 确保替换为你的实际数据库凭据和名称
SQLALCHEMY_DATABASE_URL = "postgresql://[你的用户名]:[你的密码]@localhost:5432/[你的数据库名]"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True) # echo=True 会打印执行的SQL语句，便于调试
