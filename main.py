from fastapi import FastAPI
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
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class CommandRequest(BaseModel):
    command: str

@app.post("/run-command/")
def run_command(request: CommandRequest):
    try:
        result = subprocess.run(request.command, shell=True, capture_output=True, text=True, check=True)
        return {"output": result.stdout, "error": result.stderr}
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Command failed: {e.stderr}")
