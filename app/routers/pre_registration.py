from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models import PreRegistration
from app.schemas import PreRegistrationCreate

router = APIRouter(prefix="/api/pre-registration", tags=["Pre-Registration"])

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_pre_registration(
    payload: PreRegistrationCreate,
    db: AsyncSession = Depends(get_db)
):
    """사전 예약 및 뉴스레터 구독 신청 수집 API"""
    try:
        # 동일 이메일 및 신청 유형 중복 체크
        query = select(PreRegistration).where(
            PreRegistration.email == payload.email,
            PreRegistration.reg_type == payload.reg_type
        )
        result = await db.execute(query)
        existing = result.scalar_one_or_none()

        if existing:
            return {
                "success": True,
                "message": f"이미 {payload.reg_type} 신청이 완료된 이메일입니다. 최신 소식을 빠르게 전달해 드리겠습니다.",
                "data": existing.to_dict()
            }

        pre_reg = PreRegistration(
            email=payload.email,
            phone=payload.phone,
            reg_type=payload.reg_type,
            interest=payload.interest
        )
        db.add(pre_reg)
        await db.commit()
        await db.refresh(pre_reg)

        return {
            "success": True,
            "message": "사전 예약 및 뉴스레터 구독 신청이 완료되었습니다! 혜택과 소식을 가장 먼저 보내드립니다.",
            "data": pre_reg.to_dict()
        }
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"신청 처리 중 오류가 발생했습니다: {str(e)}"
        )
