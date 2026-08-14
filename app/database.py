import os
from pathlib import Path
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

BASE_DIR = Path(__file__).resolve().parent.parent

# DB 유형 선택: 기본값 "sqlite" (개발/테스트 용이성), "mysql" 또는 "mariadb" 지원
DB_TYPE = os.getenv("DB_TYPE", "sqlite").lower()

if DB_TYPE in ["mysql", "mariadb"]:
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "3306")
    DB_NAME = os.getenv("DB_NAME", "landing_db")
    DATABASE_URL = f"mysql+aiomysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"
    
    engine = create_async_engine(
        DATABASE_URL,
        echo=False,
        pool_size=10,
        max_overflow=20,
        pool_recycle=3600,
        pool_pre_ping=True
    )
else:
    # SQLite 비동기 설정 (aiosqlite)
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