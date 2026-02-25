
from sqlalchemy import Column, BigInteger, String, DateTime
from datetime import datetime
from database import Base


class UserInfo(Base):
    __tablename__ = "tb_user_info"

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="主键ID")
    name = Column(String(255), nullable=True, comment="姓名")
    work = Column(String(255), nullable=True, comment="职业")
    create_time = Column(DateTime, nullable=False, default=datetime.now, comment="创建时间")
    update_time = Column(DateTime, nullable=False, default=datetime.now, comment="更新时间")
