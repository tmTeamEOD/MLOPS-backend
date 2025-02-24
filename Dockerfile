FROM ubuntu:latest
FROM python:3.12-slim

WORKDIR /app

# 패키지 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 복사
COPY . .

# Uvicorn을 사용해 앱 실행 (포트 80번 사용)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]