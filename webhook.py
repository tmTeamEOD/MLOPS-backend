from fastapi import FastAPI, Request
import subprocess
import hmac
import hashlib
import os
import logging

# GitHub Webhook Secret 설정
GITHUB_SECRET = "test"

app = FastAPI()

# 로그 설정
logging.basicConfig(level=logging.INFO)


def run_command(command):
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

    # Git Pull & 배포 실행
    repo_path = "/home/skitterbot/MLOPS/backend"

    logging.info("Running git pull...")
    run_command(["git", "-C", repo_path, "pull"])

    logging.info("Applying Kubernetes configurations...")
    run_command(["kubectl", "apply", "-f", f"{repo_path}/k8s"])

    logging.info("Restarting deployment...")
    run_command(["kubectl", "rollout", "restart", "deployment/fastapi-deployment"])

    return {"status": "Deployment updated"}
