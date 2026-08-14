from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI, Request, Depends
from starlette.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import engine, Base, get_db, AsyncSessionLocal
from app.models import LandingContent, Notice
from app.routers import contact, pre_registration, admin

# 기본 디렉터리 경로 설정
BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent

@asynccontextmanager
async def lifespan(app: FastAPI):
    """애플리케이션 시작 시 DB 테이블 자동 생성 및 기본 시드 데이터 등록"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # 시드 데이터 확인 및 등록
    async with AsyncSessionLocal() as session:
        # 1. 랜딩페이지 동적 콘텐츠 초기값
        content_count = await session.execute(select(LandingContent))
        if not content_count.scalars().all():
            default_contents = [
                LandingContent(
                    key="hero_title",
                    value='자율형 보안 관제 &<br><span class="gradient-text">지능형 사이버 방어</span>',
                    section_name="Overview"
                ),
                LandingContent(
                    key="hero_subtitle",
                    value='복잡해지는 멀티클라우드 환경과 고도화된 제로데이 공격을 실시간 신경망 엔진으로 감지하고 0.4초 이내에 자동 차단 및 격리합니다.',
                    section_name="Overview"
                ),
                LandingContent(
                    key="stat_detection_rate",
                    value="99.98%",
                    section_name="Overview"
                ),
                LandingContent(
                    key="stat_response_time",
                    value="< 0.4s",
                    section_name="Overview"
                ),
                LandingContent(
                    key="stat_daily_attacks",
                    value="10M+",
                    section_name="Overview"
                )
            ]
            session.add_all(default_contents)

        # 2. 초기 공지사항 데이터
        notice_count = await session.execute(select(Notice))
        if not notice_count.scalars().all():
            default_notice = Notice(
                title="SecOps v4.2 차세대 위협 방어 엔진 출시 및 얼리액세스 이벤트",
                content="실시간 AI 위협 탐지 속도를 30% 향상시킨 v4.2 신경망 차단 엔진이 정식 출시되었습니다. 사전 예약을 신청하시면 14일 무료 종합 포렌식 진단을 제공해 드립니다.",
                badge_text="NEW RELEASE",
                is_active=True,
                is_pinned=True
            )
            session.add(default_notice)

        await session.commit()
    
    yield

app = FastAPI(title="SecOps Corporate Landing Page", lifespan=lifespan)

# 정적 파일(CSS, JS 등) 및 템플릿(HTML) 경로 마운트
app.mount("/static", StaticFiles(directory=str(PROJECT_ROOT / "static")), name="static")
templates = Jinja2Templates(directory=str(PROJECT_ROOT / "templates"))

# 라우터 포함
app.include_router(contact.router)
app.include_router(pre_registration.router)
app.include_router(admin.router)

@app.get("/")
async def read_landing(request: Request, db: AsyncSession = Depends(get_db)):
    # DB에서 랜딩페이지 동적 콘텐츠 및 공지사항 가져오기
    content_result = await db.execute(select(LandingContent))
    raw_contents = content_result.scalars().all()
    contents = {c.key: c.value for c in raw_contents}

    notice_result = await db.execute(
        select(Notice).where(Notice.is_active == True).order_by(Notice.is_pinned.desc(), Notice.created_at.desc())
    )
    active_notices = notice_result.scalars().all()
    active_notice_list = [n.to_dict() for n in active_notices]

    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "title": "SecOps — Next-Gen Cyber Defense & Operations",
            "year": 2026,
            "contents": contents,
            "notices": active_notice_list
        }
    )