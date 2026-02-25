
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 数据库配置
DATABASE_URL = "mysql+pymysql://root:JZh2019%40nodejsjava@119.29.194.246:53306/pyDb"

# 创建数据库引擎
engine = create_engine(DATABASE_URL)

# 创建会话工厂（启用自动提交和自动刷新）
SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)

# 创建基类
Base = declarative_base()


# 获取数据库会话（自动提交）
def get_db():
    db = SessionLocal()
    try:
        yield db
        # 请求结束后自动提交
        db.commit()
    except Exception:
        # 发生异常时回滚
        db.rollback()
        raise
    finally:
        db.close()
