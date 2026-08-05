from pydantic import BaseModel


class ExtractParams(BaseModel):
    url: str
    download: bool = False
    index: list[str | int] | None = None
    cookie: str = None
    proxy: str = None
    check_record: bool = True


class ExtractData(BaseModel):
    message: str
    params: ExtractParams
    data: dict | None
