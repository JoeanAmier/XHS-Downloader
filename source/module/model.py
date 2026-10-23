from pydantic import BaseModel, ConfigDict


class ExtractParams(BaseModel):
    model_config = ConfigDict(extra="forbid")

    url: str
    download: bool = False
    index: list[str | int] | None = None
    cookie: str | None = None
    check_record: bool = True


class ExtractData(BaseModel):
    message: str
    params: ExtractParams
    data: dict | None
