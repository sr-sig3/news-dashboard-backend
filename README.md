# News Dashboard Backend

뉴스 데이터 분석을 위한 백엔드 API 서비스입니다. 뉴스 키워드 분석 및 워드 클라우드 시각화를 위한 API를 제공합니다.

## 기능

- 뉴스 키워드 저장 및 조회
- 키워드 기반 검색
- 워드 클라우드 데이터 제공
- 키워드 점수 및 빈도수 기반 분석

## 기술 스택

- FastAPI
- SQLAlchemy
- PostgreSQL
- Python 3.8+

## 설치 및 실행

1. 저장소 클론
```bash
git clone [repository-url]
cd news-dashboard-backend
```

2. 가상환경 생성 및 활성화
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. 의존성 설치
```bash
pip install -r requirements.txt
```

4. 환경 변수 설정
`.env` 파일을 생성하고 다음 내용을 추가합니다:
```
DATABASE_URL=postgresql://username:password@localhost:5432/news_db
```

5. 서버 실행
```bash
uvicorn app.main:app --reload
```

## API 문서

서버가 실행되면 다음 URL에서 API 문서를 확인할 수 있습니다:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 주요 엔드포인트

#### 키워드 조회
- `GET /keywords/`: 모든 키워드 목록 조회
- `GET /keywords/{keyword_id}`: 특정 키워드 상세 정보 조회
- `GET /keywords/search/{keyword_text}`: 키워드 검색

#### 워드 클라우드
- `GET /keywords/wordcloud/`: 워드 클라우드 데이터 조회
  - 쿼리 파라미터:
    - `days`: 조회 기간 (일)
    - `min_score`: 최소 점수
    - `limit`: 반환할 키워드 수

## 데이터베이스 스키마

### Keyword 테이블
- `id`: Integer (Primary Key)
- `keyword`: String
- `score`: Float
- `news_id`: Integer
- `created_at`: DateTime

## 라이선스

MIT License