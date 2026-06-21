from pydantic import BaseModel, HttpUrl
from datetime import datetime


# HttpUrl does real validation , returns 422 before your handler even runs

class ShortenRequest(BaseModel):
    url: HttpUrl
    custom_code: str | None = None
    expires_in: int | None = None

class ShortenResponse(BaseModel):
    code: str
    short_url: str
    original_url: str

class StatsResponse(BaseModel):
    code: str
    original_url: str
    clicks: int
    created_at: datetime

