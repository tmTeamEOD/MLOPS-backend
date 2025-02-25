from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, FileResponse

app = FastAPI()

@app.get("/")
async def root():
    return JSONResponse(
        content={"message": "Hello,디비 테스트5611!"},
        media_type="application/json; charset=utf-8"
    )

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("static/favicon.ico")  # favicon 파일 제공

from pydantic import BaseModel
import subprocess

# JSON 요청을 받을 데이터 모델 정의
class SSHRequest(BaseModel):
    remote_host: str
    remote_user: str
    remote_port: int = 9000  # 기본값 9000

@app.post("/setup-reverse-ssh/")
def setup_reverse_ssh(request: SSHRequest):
    """
    FastAPI에서 원격 SSH 터널을 설정하는 API
    """
    try:
        cmd = f"ssh -R {request.remote_port}:localhost:6443 {request.remote_user}@{request.remote_host} -N -f"
        subprocess.run(cmd, shell=True, check=True)
        return {"message": f"Reverse SSH 터널 설정 완료. 6443 포트가 {request.remote_host}:{request.remote_port}로 우회됨."}
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"SSH 터널링 실패: {str(e)}")
