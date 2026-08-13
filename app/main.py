from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# 정적 파일(CSS, JS, 이미지 등) 경로 설정
# 프로젝트 루트 디렉터리에 'static' 폴더가 있어야 합니다.
app.mount("/static", StaticFiles(directory="static"), name="static")

# 템플릿(HTML) 경로 설정
# 프로젝트 루트 디렉터리에 'templates' 폴더가 있어야 합니다.
templates = Jinja2Templates(directory="templates")

@app.get("/")
def read_landing(request: Request):
    # 최신 Starlette/FastAPI 표준에 맞게 request 객체를 첫 번째 인자로 전달합니다.
    return templates.TemplateResponse(
        request, 
        "index.html", 
        {"title": "Corporate Landing Page"}  # HTML 내부로 전달할 데이터 (필요시 수정 가능)
    )