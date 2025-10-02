from fastapi import FastAPI, Response, status, HTTPException, Depends
from typing import List, Optional
from sqlmodel import Session, select, SQLModel  # 导入SQLModel的Session和select

from .database import engine
from .models import Post  # 导入Post模型

app = FastAPI()

# 定义一个依赖项函数，用于获取数据库会话
def get_session(): # FastAPI 教程中常命名为 get_db
    with Session(engine) as session: # 使用SQLModel的Session，并确保引擎被传入
        yield session
        # 当请求处理完毕后，with语句会自动处理session.close()
        # 如果在会话块内发生异常，事务会自动回滚
        # 如果没有异常，且你调用了 session.commit()，事务会被提交


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=Post)
def create_new_post(post_payload: Post, session: Session = Depends(get_session)):
    # post_payload 是一个已经通过Pydantic校验的Post实例
    # 注意：如果Post模型中的id是Optional且primary_key=True, default=None
    # 在创建时，我们不应该给id赋值，数据库会自动生成。
    # 如果post_payload传入了id，你可能需要:
    # db_post = Post.model_validate(post_payload) # Pydantic v2
    # 或 db_post = Post(**post_payload.dict(exclude_unset=True, exclude={'id'})) # 确保不传入id

    db_post = Post.model_validate(post_payload)  # 确保从请求体创建的实例符合模型定义
    # 如果ID是可选的，且数据库自动生成，
    # 传入的post_payload不应包含ID，或者需要处理它

    session.add(db_post)  # 将新帖子对象添加到会话中，准备插入
    session.commit()  # 提交事务，将更改写入数据库
    session.refresh(db_post)  # 从数据库刷新对象，获取自动生成的值 (如ID, created_at)
    return db_post

# main.py (接上文)

@app.get("/posts", response_model=List[Post])
def get_all_existing_posts(session: Session = Depends(get_session)):
    statement = select(Post) # 创建一个SQLModel查询语句
    results = session.exec(statement) # 执行查询语句
    posts_list = results.all() # 获取所有结果行
    return posts_list

# main.py (接上文)

@app.get("/posts/{post_id}", response_model=Post)
def get_single_post(post_id: int, session: Session = Depends(get_session)):
    # db.get(ModelClass, primary_key_value) 是获取单个对象最高效的方式
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"ID为 {post_id} 的帖子未找到")
    return post



# main.py (接上文)

# 为了更新，通常我们会定义一个不包含只读字段（如id, created_at）的Pydantic模型
class PostUpdate(SQLModel): # Pydantic模型，用于更新，字段都设为Optional
    title: Optional[str] = None
    content: Optional[str] = None
    published: Optional[bool] = None

@app.put("/posts/{post_id}", response_model=Post)
def update_existing_post(
    post_id: int,
    post_update_payload: PostUpdate, # 使用专门的Update模型
    session: Session = Depends(get_session)
):
    db_post = session.get(Post, post_id) # 获取要更新的帖子对象
    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"ID为 {post_id} 的帖子未找到")

    # post_update_payload.model_dump(exclude_unset=True) 获取请求中实际传递的字段值
    # exclude_unset=True 确保只获取客户端明确设置的字段，用于部分更新(PATCH)
    # 对于PUT，客户端应该提供所有可修改字段的新值
    update_data = post_update_payload.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_post, key, value) # 更新帖子对象的属性

    session.add(db_post) # 即使是更新，SQLModel也需要add来追踪对象变化
    session.commit()
    session.refresh(db_post)
    return db_post



# main.py (接上文)

@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_post(post_id: int, session: Session = Depends(get_session)):
    db_post = session.get(Post, post_id)
    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"ID为 {post_id} 的帖子未找到")

    session.delete(db_post) # 从会话中标记此对象为待删除
    session.commit()       # 提交事务，将删除操作写入数据库

    # 对于204 No Content，不应返回任何响应体
    return Response(status_code=status.HTTP_204_NO_CONTENT)
