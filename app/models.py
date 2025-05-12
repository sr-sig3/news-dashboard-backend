from sqlalchemy import Column, Integer, String, DateTime, Float
from .database import Base

class Keyword(Base):
    __tablename__ = "keywords"

    id = Column(Integer, primary_key=True, index=True)
    keyword = Column(String, index=True)
    score = Column(Float)
    news_id = Column(Integer, index=True)
    created_at = Column(DateTime) 