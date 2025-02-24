from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse

app = FastAPI()

@app.get("/")
async def root():
    return JSONResponse(
        content={"message": "Hello, 개지미스!"},
        media_type="application/json; charset=utf-8"
    )

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("static/favicon.ico")  # favicon 파일 제공