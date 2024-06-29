from pydantic import BaseModel


class ExtractParams(BaseModel):
    url: str
    download: bool = False
    index: list = None
    skip: bool = False


class ExtractData(BaseModel):
    message: str
    url: str
    data: dict | None
