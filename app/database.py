from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

# MariaDB 접속 정보 설정 (사용자 환경에 맞게 ID/PW/DB명 수정)
# 예: mysql+aiomysql://아이디:비밀번호@호스트:포트/데이터베이스명
DATABASE_URL = "mysql+aiomysql://root:password@localhost:3306/landing_db"

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()

# FastAPI 의존성 주입용 함수
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session