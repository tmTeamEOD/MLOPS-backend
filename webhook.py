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

    try:
        # Git Pull 실행
        git_pull_result = subprocess.run(["git", "-C", repo_path, "pull"], capture_output=True, text=True, check=True)

        # 쿠버네티스 배포 적용
        kubectl_apply_result = subprocess.run(["kubectl", "apply", "-f", f"{repo_path}/k8s"], capture_output=True,
                                              text=True, check=True)

        # FastAPI Deployment 강제 재배포
        rollout_result = subprocess.run(["kubectl", "rollout", "restart", "deployment/fastapi-deployment"],
                                        capture_output=True, text=True, check=True)

        return {
            "status": "Deployment updated",
            "git_pull": git_pull_result.stdout,
            "kubectl_apply": kubectl_apply_result.stdout,
            "rollout_restart": rollout_result.stdout
        }

    except subprocess.CalledProcessError as e:
        return {
            "status": "Error executing command",
            "command": e.cmd,
            "output": e.output,
            "stderr": e.stderr
        }
