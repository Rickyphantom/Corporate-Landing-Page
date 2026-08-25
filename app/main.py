from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI, Request, Depends
from fastapi.responses import RedirectResponse
from starlette.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import engine, Base, get_db, AsyncSessionLocal
from app.models import LandingContent, Notice, FaqItem
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

        # 3. 초기 Q&A FAQ 데이터
        faq_count = await session.execute(select(FaqItem))
        if not faq_count.scalars().all():
            default_faqs = [
                FaqItem(
                    category="서비스/도입",
                    question="기존 온프레미스(On-Premise) 및 레거시 시스템과도 연동이 가능한가요?",
                    answer="네, 가능합니다. SecOps는 AWS, Azure, GCP 등 주요 퍼블릭 클라우드뿐만 아니라 온프레미스 하이퍼바이저 및 베어메탈 서버 환경을 위한 경량화 에이전트(Lightweight Daemon)와 Syslog, SNMP 인터페이스를 모두 지원합니다.",
                    order_num=1,
                    is_active=True
                ),
                FaqItem(
                    category="기술/보안",
                    question="AI 엔진의 오탐률(False Positive)은 어떻게 제어하나요?",
                    answer="조직 내부의 정상 트래픽 기준선(Baseline)을 학습하는 전용 격리형 신경망 모델을 배포하며, MITRE ATT&CK 프레임워크 기반 3단계 교차 검증 알고리즘을 통해 오탐률을 0.02% 이하로 최소화합니다.",
                    order_num=2,
                    is_active=True
                ),
                FaqItem(
                    category="컨설팅/비용",
                    question="맞춤형 보안 컨설팅 및 취약점 진단 절차는 어떻게 진행되나요?",
                    answer="신청 후 24시간 이내 전담 보안 아키텍트가 배정되어 사전 인프라 인터뷰를 진행합니다. 이후 2주간 무중단 취약점 스캔 및 모의 침투 테스트를 거쳐 상세 진단 리포트와 개선 가이드를 무상 제공합니다.",
                    order_num=3,
                    is_active=True
                ),
                FaqItem(
                    category="컴플라이언스",
                    question="ISMS-P, SOC2 등 보안 인증 규제 대응을 지원하나요?",
                    answer="감사 증적 자동 수집 및 감사관 제출용 표준 보고서 생성 기능을 기본 탑재하고 있어, 규제 대응에 소요되는 리소스를 80% 이상 절감할 수 있습니다.",
                    order_num=4,
                    is_active=True
                )
            ]
            session.add_all(default_faqs)

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
<<<<<<< HEAD
async def read_landing(request: Request, db: AsyncSession = Depends(get_db)):
    # DB에서 랜딩페이지 동적 콘텐츠 및 공지사항, FAQ 가져오기
    content_result = await db.execute(select(LandingContent))
    raw_contents = content_result.scalars().all()
    contents = {c.key: c.value for c in raw_contents}
=======
async def read_root():
    """웹페이지 루트 접근 시 관리자페이지로 리다이렉트"""
    return RedirectResponse(url="/admin")
>>>>>>> f08d0654ab6bb1749ec1ef6852cec5b8e1f74693

@app.get("/qna")
async def read_qna():
    """Q&A 페이지 접근 시 관리자페이지로 리다이렉트"""
    return RedirectResponse(url="/admin")

<<<<<<< HEAD
    faq_result = await db.execute(
        select(FaqItem).where(FaqItem.is_active == True).order_by(FaqItem.order_num.asc(), FaqItem.id.asc())
    )
    active_faqs = faq_result.scalars().all()
    faq_list = [f.to_dict() for f in active_faqs]

    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "title": "SecOps — Next-Gen Cyber Defense & Operations",
            "year": 2026,
            "contents": contents,
            "notices": active_notice_list,
            "faqs": faq_list,
            "active_page": "index"
        }
    )

@app.get("/qna")
async def read_qna(request: Request, db: AsyncSession = Depends(get_db)):
    faq_result = await db.execute(
        select(FaqItem).where(FaqItem.is_active == True).order_by(FaqItem.order_num.asc(), FaqItem.id.asc())
    )
    active_faqs = faq_result.scalars().all()
    faq_list = [f.to_dict() for f in active_faqs]

    return templates.TemplateResponse(
        request,
        "qna.html",
        {
            "title": "Q&A 지식베이스 — SecOps Cyber Defense",
            "year": 2026,
            "faqs": faq_list,
            "active_page": "qna"
        }
    )

@app.get("/support")
async def read_support(request: Request, db: AsyncSession = Depends(get_db)):
    notice_result = await db.execute(
        select(Notice).where(Notice.is_active == True).order_by(Notice.is_pinned.desc(), Notice.created_at.desc())
    )
    active_notices = notice_result.scalars().all()
    active_notice_list = [n.to_dict() for n in active_notices]

    return templates.TemplateResponse(
        request,
        "support.html",
        {
            "title": "지원센터 — SecOps Cyber Defense",
            "year": 2026,
            "notices": active_notice_list,
            "active_page": "support"
        }
    )
=======
@app.get("/support")
async def read_support():
    """지원 센터 접근 시 관리자페이지로 리다이렉트"""
    return RedirectResponse(url="/admin")
>>>>>>> f08d0654ab6bb1749ec1ef6852cec5b8e1f74693
