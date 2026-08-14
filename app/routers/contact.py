from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import ContactInquiry
from app.schemas import ContactInquiryCreate

router = APIRouter(prefix="/api/contact", tags=["Contact Inquiries"])

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_contact_inquiry(
    payload: ContactInquiryCreate,
    db: AsyncSession = Depends(get_db)
):
    """방문자 문의하기 및 견적 요청 저장 API"""
    try:
        inquiry = ContactInquiry(
            name=payload.name,
            email=payload.email,
            phone=payload.phone,
            company=payload.company,
            inquiry_type=payload.inquiry_type,
            message=payload.message,
            status="PENDING"
        )
        db.add(inquiry)
        await db.commit()
        await db.refresh(inquiry)
        
        return {
            "success": True,
            "message": "문의 및 견적 요청이 성공적으로 등록되었습니다. 담당자가 조속히 연락드리겠습니다.",
            "data": inquiry.to_dict()
        }
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"문의 저장 중 오류가 발생했습니다: {str(e)}"
        )
