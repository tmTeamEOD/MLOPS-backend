# 베이스 이미지
FROM python:3.9

# 작업 디렉토리 설정
WORKDIR /app

# 의존성 사전 설치 (캐싱 최적화)
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 추가
COPY . /app

# FastAPI 실행
CMD ["uvicorn", "webhook:app", "--host", "0.0.0.0", "--port", "80"]
