
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class UserInfoBase(BaseModel):
    name: Optional[str] = None
    work: Optional[str] = None


class UserInfoCreate(UserInfoBase):
    pass


class UserInfoUpdate(UserInfoBase):
    pass


class UserInfoResponse(UserInfoBase):
    id: int
    create_time: datetime
    update_time: datetime

    class Config:
        from_attributes = True
