import asyncio
import os
import sys
from pathlib import Path

# Windows 콘솔 인코딩 대응
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# 부모 디렉터리를 sys.path에 추가
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from sqlalchemy import select, text
from app.database import engine, AsyncSessionLocal, Base, DATABASE_URL, DB_TYPE
from app.models import LandingContent, Notice, FaqItem, ContactInquiry, PreRegistration

async def test_connection():
    print(f"[1/3] 데이터베이스 연결 시도 중...")
    print(f"   • DB 유형: {DB_TYPE}")
    # 비밀번호 마스킹 처리하여 출력
    masked_url = DATABASE_URL
    if "@" in masked_url:
        prefix, rest = masked_url.split("@", 1)
        if ":" in prefix:
            proto_user, _ = prefix.rsplit(":", 1)
            masked_url = f"{proto_user}:****@{rest}"
    print(f"   • Connection URL: {masked_url}")

    try:
        # 1. 간단한 연결 확인 (SELECT 1)
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            val = result.scalar()
            print(f"[2/3] DB 연결 성공! (Query Output: {val})")

        # 2. 테이블 생성 테스트
        print(f"[3/3] DB 테이블 스키마 자동 동기화 (create_all) 실행...")
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print(f"모든 테이블 스키마가 성공적으로 생성 및 확인되었습니다.")

        # 3. 데이터 수 건 조회 테스트
        async with AsyncSessionLocal() as session:
            notices = (await session.execute(select(Notice))).scalars().all()
            faqs = (await session.execute(select(FaqItem))).scalars().all()
            print(f"[결과 요약] 현재 등록된 공지사항: {len(notices)}개 | FAQ: {len(faqs)}개")

        print("\nAWS RDS / 데이터베이스 연동 테스트 완료!")

    except Exception as e:
        print(f"\n❌ DB 연결 실패!")
        print(f"에러 메시지: {e}")
        print("\n💡 RDS 연결 체크리스트:")
        print(" 1. AWS RDS 보안 그룹(Security Group)에서 인바운드 규칙(Port 5432 또는 3306)이 허용되어 있는지 확인하세요.")
        print(" 2. RDS 퍼블릭 액세스(Public Accessibility) 기능이 '예(Yes)'로 설정되어 있는지 확인하세요.")
        print(" 3. .env 파일의 DB_HOST, DB_USER, DB_PASSWORD, DB_NAME이 정확한지 확인하세요.")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(test_connection())
