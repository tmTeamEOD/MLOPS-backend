from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, FileResponse

app = FastAPI()

@app.get("/")
async def root():
    return JSONResponse(
        content={"message": "Hello,디비 테스트56!"},
        media_type="application/json; charset=utf-8"
    )

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("static/favicon.ico")  # favicon 파일 제공

import subprocess


@app.post("/setup-reverse-ssh/")
def setup_reverse_ssh(remote_host: str, remote_user: str, remote_port: int = 9000):
    """
    FastAPI를 통해 마스터 노드에서 외부 서버로 SSH 터널링 생성
    """
    try:
        cmd = f"ssh -R {remote_port}:localhost:6443 {remote_user}@{remote_host} -N -f"
        subprocess.run(cmd, shell=True, check=True)
        return {"message": f"Reverse SSH 터널 설정 완료. 6443 포트가 {remote_host}:{remote_port}로 우회됨."}
    except subprocess.CalledProcessError as e:
        return {"error": str(e)}
