from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db, engine, Base
from models import UserInfo
from schemas import UserInfoCreate, UserInfoUpdate, UserInfoResponse

# 创建 FastAPI 应用
app = FastAPI(title="用户信息管理API", description="用户信息的增删改查接口")

# 创建数据库表
Base.metadata.create_all(bind=engine)


# 创建用户
@app.post("/users/", response_model=UserInfoResponse, summary="创建用户")
def create_user(user: UserInfoCreate, db: Session = Depends(get_db)):
    """
    创建新用户
    
    - **name**: 用户姓名
    - **work**: 用户职业
    """
    db_user = UserInfo(**user.model_dump())
    db.add(db_user)
    # 自动提交，无需手动调用 db.commit()
    db.refresh(db_user)
    return db_user


# 获取所有用户
@app.get("/users/", response_model=List[UserInfoResponse], summary="获取所有用户")
def get_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    获取所有用户列表
    
    - **skip**: 跳过的记录数
    - **limit**: 返回的记录数
    """
    users = db.query(UserInfo).offset(skip).limit(limit).all()
    return users


# 根据ID获取用户
@app.get("/users/{user_id}", response_model=UserInfoResponse, summary="获取指定用户")
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    根据用户ID获取用户信息
    
    - **user_id**: 用户ID
    """
    user = db.query(UserInfo).filter(UserInfo.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户未找到")
    return user


# 更新用户
@app.put("/users/{user_id}", response_model=UserInfoResponse, summary="更新用户")
def update_user(user_id: int, user: UserInfoUpdate, db: Session = Depends(get_db)):
    """
    更新用户信息
    
    - **user_id**: 用户ID
    - **name**: 用户姓名
    - **work**: 用户职业
    """
    db_user = db.query(UserInfo).filter(UserInfo.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="用户未找到")
    
    update_data = user.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)
    
    # 自动提交，无需手动调用 db.commit()
    db.refresh(db_user)
    return db_user


# 删除用户
@app.delete("/users/{user_id}", summary="删除用户")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    删除用户
    
    - **user_id**: 用户ID
    """
    db_user = db.query(UserInfo).filter(UserInfo.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="用户未找到")
    
    db.delete(db_user)
    # 自动提交，无需手动调用 db.commit()
    return {"message": "用户删除成功"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)