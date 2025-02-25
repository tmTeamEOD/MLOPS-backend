from fastapi import FastAPI, Request
import subprocess
import hmac
import hashlib
import os
import logging
import time

# GitHub Webhook Secret 설정
GITHUB_SECRET = "test"

# Docker 이미지 및 컨테이너 레지스트리 설정
DOCKER_REPO = "ghcr.io/tmteameod/smhrd_mlops"

app = FastAPI()

# 로그 설정
logging.basicConfig(level=logging.INFO)

def run_command(command):
    """명령어 실행 함수"""
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        logging.error(f"Error executing {command}: {result.stderr}")
    return result.stdout.strip()

@app.post("/webhook")
async def webhook(request: Request):
    logging.info("Webhook received!")

    # GitHub Signature 검증
    payload = await request.body()
    signature = request.headers.get("X-Hub-Signature-256", "")
    expected_signature = "sha256=" + hmac.new(GITHUB_SECRET.encode(), payload, hashlib.sha256).hexdigest()

    if not hmac.compare_digest(signature, expected_signature):
        logging.warning("Invalid signature detected")
        return {"status": "Invalid signature"}

    # Git Pull 실행
    repo_path = "/home/k8s/MLOPS-backend"
    logging.info("Running git pull...")
    run_command(["git", "-C", repo_path, "pull"])
    run_command(["bash", "-c", f"echo $GITHUB_PAT | docker login ghcr.io -u tmteameod --password-stdin"])
    # Docker 이미지 빌드 및 Push
    image_tag = f"{DOCKER_REPO}:{int(time.time())}"  # Timestamp 기반 태그
    logging.info(f"Building Docker image: {image_tag}...")
    run_command(["docker", "build", "-t", image_tag, repo_path])

    logging.info(f"Pushing Docker image: {image_tag}...")
    run_command(["docker", "push", image_tag])

    # 쿠버네티스 배포 업데이트
    logging.info("Updating Kubernetes deployment...")
    run_command(["kubectl", "set", "image", "deployment/fastapi-deployment",
                 f"fastapi={image_tag}"])

    # 롤아웃 진행 확인
    logging.info("Checking rollout status...")
    rollout_status = run_command(["kubectl", "rollout", "status", "deployment/fastapi-deployment"])

    return {"status": "Deployment updated", "rollout_status": rollout_status}


#uvicorn webhook:app --host 0.0.0.0 --port 8000 --reload
