from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from datetime import datetime, timedelta
from fastapi.middleware.cors import CORSMiddleware

from . import models, schemas
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS 설정 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React 개발 서버 주소
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)

@app.get("/keywords/", response_model=List[schemas.Keyword])
def get_keywords(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    keywords = db.query(models.Keyword).offset(skip).limit(limit).all()
    return keywords

@app.get("/keywords/{keyword_id}", response_model=schemas.Keyword)
def get_keyword(keyword_id: int, db: Session = Depends(get_db)):
    keyword = db.query(models.Keyword).filter(models.Keyword.id == keyword_id).first()
    if keyword is None:
        raise HTTPException(status_code=404, detail="Keyword not found")
    return keyword

@app.get("/keywords/search/{keyword_text}", response_model=List[schemas.Keyword])
def search_keywords(keyword_text: str, db: Session = Depends(get_db)):
    keywords = db.query(models.Keyword).filter(
        models.Keyword.keyword.ilike(f"%{keyword_text}%")
    ).all()
    return keywords

@app.get("/keywords/wordcloud/", response_model=schemas.WordCloudResponse)
def get_wordcloud(
    days: int = 7,
    min_score: float = 0.0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    # 특정 기간 동안의 키워드 집계
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # 키워드별로 점수 합산 및 빈도수 계산
    keyword_stats = db.query(
        models.Keyword.keyword,
        func.sum(models.Keyword.score).label('total_score'),
        func.count(models.Keyword.id).label('frequency')
    ).filter(
        models.Keyword.created_at >= start_date,
        models.Keyword.score >= min_score
    ).group_by(
        models.Keyword.keyword
    ).order_by(
        func.sum(models.Keyword.score).desc()
    ).limit(limit).all()
    
    # 워드 클라우드 데이터 형식으로 변환
    wordcloud_items = [
        schemas.WordCloudItem(
            text=keyword,
            value=float(total_score * frequency)  # 점수와 빈도수를 곱하여 가중치 계산
        )
        for keyword, total_score, frequency in keyword_stats
    ]
    
    return schemas.WordCloudResponse(
        keywords=wordcloud_items,
        total_count=len(wordcloud_items)
    ) 
