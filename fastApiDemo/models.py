# models.py
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field # 导入SQLModel基类和Field
from sqlalchemy import text # 用于定义服务器端默认值

# 定义Post模型，它既是Pydantic模型，也是SQLAlchemy表模型
class Post(SQLModel, table=True): # table=True 表明这是一个数据库表模型
    __tablename__ = "posts" # 可选，如果省略，SQLModel会尝试根据类名推断表名

    # 定义字段，Field用于提供额外的数据库列信息和Pydantic校验信息
    id: Optional[int] = Field(default=None, primary_key=True, index=True) # 主键，自动生成，建立索引
    title: str = Field(index=True) # 标题，建立索引以便快速搜索
    content: str = Field(nullable=False) # nullable=False 表示该字段不能为空
    published: bool = Field(default=True, sa_column_kwargs={"server_default": text("true")}) # 是否发布，默认True
    created_at: Optional[datetime] = Field(
        default=None, # Pydantic层面允许不传，数据库层面有默认值
        sa_column_kwargs={"server_default": text("now()")} # 数据库级别默认值为当前时间
    )
