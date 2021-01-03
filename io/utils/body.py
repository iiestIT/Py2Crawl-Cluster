from pydantic import BaseModel


class ToScrape(BaseModel):
    url: str
