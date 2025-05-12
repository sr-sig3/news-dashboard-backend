from pydantic import BaseModel
from datetime import datetime
from typing import List

class KeywordBase(BaseModel):
    keyword: str
    score: float
    news_id: int

class KeywordCreate(KeywordBase):
    pass

class Keyword(KeywordBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class WordCloudItem(BaseModel):
    text: str
    value: float

class WordCloudResponse(BaseModel):
    keywords: List[WordCloudItem]
    total_count: int 