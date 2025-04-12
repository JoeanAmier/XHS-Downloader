from pydantic import BaseModel


class ExtractParams(BaseModel):
    url: str
    download: bool = False
    index: list = None
    cookie: str = None
    proxy: str = None
    skip: bool = False


class ExtractData(BaseModel):
    message: str
    params: ExtractParams
    data: dict | None
