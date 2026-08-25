import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

# .env 파일 로드
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# 데이터베이스 설정 환경변수 추출
DB_TYPE = os.getenv("DB_TYPE", "sqlite").lower()
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "")
DB_NAME = os.getenv("DB_NAME", "secops_db")
DB_SSL = os.getenv("DB_SSL", "false").lower() in ["true", "1", "yes", "require"]

# 명시적 DATABASE_URL 지정 시 최우선 사용 (예: AWS RDS PostgreSQL / MySQL URL)
CUSTOM_DATABASE_URL = os.getenv("DATABASE_URL")

if CUSTOM_DATABASE_URL:
    DATABASE_URL = CUSTOM_DATABASE_URL
    engine_kwargs = {"echo": False}
    if not DATABASE_URL.startswith("sqlite"):
        engine_kwargs.update({
            "pool_size": int(os.getenv("DB_POOL_SIZE", "10")),
            "max_overflow": int(os.getenv("DB_MAX_OVERFLOW", "20")),
            "pool_recycle": 3600,
            "pool_pre_ping": True,
        })
    else:
        engine_kwargs["connect_args"] = {"check_same_thread": False}

    engine = create_async_engine(DATABASE_URL, **engine_kwargs)

elif DB_TYPE in ["postgres", "postgresql"]:
    port = DB_PORT if DB_PORT else "5432"
    ssl_query = "?ssl=require" if DB_SSL else ""
    DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{port}/{DB_NAME}{ssl_query}"
    
    engine = create_async_engine(
        DATABASE_URL,
        echo=False,
        pool_size=int(os.getenv("DB_POOL_SIZE", "10")),
        max_overflow=int(os.getenv("DB_MAX_OVERFLOW", "20")),
        pool_recycle=3600,
        pool_pre_ping=True,
    )

elif DB_TYPE in ["mysql", "mariadb"]:
    port = DB_PORT if DB_PORT else "3306"
    ssl_query = "?charset=utf8mb4"
    if DB_SSL:
        ssl_query += "&ssl=true"
    DATABASE_URL = f"mysql+aiomysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{port}/{DB_NAME}{ssl_query}"
    
    engine = create_async_engine(
        DATABASE_URL,
        echo=False,
        pool_size=int(os.getenv("DB_POOL_SIZE", "10")),
        max_overflow=int(os.getenv("DB_MAX_OVERFLOW", "20")),
        pool_recycle=3600,
        pool_pre_ping=True,
    )

else:
    # 로컬 fallback (SQLite)
    SQLITE_PATH = BASE_DIR / "landing.db"
    DATABASE_URL = f"sqlite+aiosqlite:///{SQLITE_PATH}"
    
    engine = create_async_engine(
        DATABASE_URL,
        echo=False,
        connect_args={"check_same_thread": False}
    )

# 비동기 세션 팩토리
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

# ORM 모델 기반 클래스
Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()