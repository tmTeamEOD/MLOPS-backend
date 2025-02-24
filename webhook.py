from fastapi import FastAPI, Request
import subprocess
import hmac
import hashlib
import os

# GitHub Webhook Secret 설정
GITHUB_SECRET = "test"

app = FastAPI()

# GitHub Webhook을 받을 엔드포인트
@app.post("/webhook")
async def webhook(request: Request):
    # GitHub Signature 검증
    payload = await request.body()
    signature = request.headers.get("X-Hub-Signature-256")
    expected_signature = "sha256=" + hmac.new(GITHUB_SECRET.encode(), payload, hashlib.sha256).hexdigest()

    if not hmac.compare_digest(signature, expected_signature):
        return {"status": "Invalid signature"}

    # Git Pull & 배포 실행
    repo_path = "/home/skitterbot/MLOPS/backend"
    subprocess.run(["git", "-C", repo_path, "pull"], check=True)
    subprocess.run(["kubectl", "apply", "-f", f"{repo_path}/k8s"], check=True)
    subprocess.run(["kubectl", "rollout", "restart", "deployment/fastapi-deployment"],
                   capture_output=True, text=True, check=True)
    return {"status": "Deployment updated"}
