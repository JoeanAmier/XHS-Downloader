from typing import Optional

from pydantic import BaseModel


class SiteItemCreate(BaseModel):
    pId: int
    name: str
    desc: Optional[str] = None
    uri: str
    isExpand: int = 0
    favicon: Optional[str] = None
    status: int = 0
    orderNum: int = 0
    category: str  # index, other


class SiteItemUpdate(BaseModel):
    pId: int
    name: str
    desc: Optional[str] = None
    uri: str
    isExpand: int = 0
    favicon: Optional[str] = None
    status: int = 0
    orderNum: int = 0
    category: str  # index, other
