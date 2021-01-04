from pydantic import BaseModel
from typing import Optional


class ToScrape(BaseModel):
    url: str
    scope: Optional[bool]
