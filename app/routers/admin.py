import io
import csv
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.responses import HTMLResponse, StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from app.database import get_db
from app.models import ContactInquiry, PreRegistration, LandingContent, Notice
from app.schemas import (
    ContactStatusUpdate, NoticeCreate, NoticeUpdate, ContentBatchUpdate
)

router = APIRouter(tags=["Admin"])

# ==============================================================================
# 📺 관리자 대시보드 HTML 페이지
# ==============================================================================
@router.get("/admin", response_class=HTMLResponse)
async def admin_dashboard_page(request: Request):
    """관리자 대시보드 메인 웹 페이지"""
    from app.main import templates
    return templates.TemplateResponse(request, "admin.html", {"title": "SecOps — Administrator Portal"})


# ==============================================================================
# 📬 1. 문의 및 견적 요청 관리 API
# ==============================================================================
@router.get("/api/admin/inquiries")
async def get_all_inquiries(
    status_filter: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    query = select(ContactInquiry).order_by(ContactInquiry.created_at.desc())
    if status_filter:
        query = query.where(ContactInquiry.status == status_filter)
    result = await db.execute(query)
    inquiries = result.scalars().all()
    return {"success": True, "count": len(inquiries), "data": [i.to_dict() for i in inquiries]}


@router.patch("/api/admin/inquiries/{inquiry_id}/status")
async def update_inquiry_status(
    inquiry_id: int,
    payload: ContactStatusUpdate,
    db: AsyncSession = Depends(get_db)
):
    query = select(ContactInquiry).where(ContactInquiry.id == inquiry_id)
    result = await db.execute(query)
    inquiry = result.scalar_one_or_none()

    if not inquiry:
        raise HTTPException(status_code=404, detail="해당 문의 건을 찾을 수 없습니다.")

    inquiry.status = payload.status
    await db.commit()
    await db.refresh(inquiry)
    return {"success": True, "message": "문의 상태가 변경되었습니다.", "data": inquiry.to_dict()}


@router.delete("/api/admin/inquiries/{inquiry_id}")
async def delete_inquiry(
    inquiry_id: int,
    db: AsyncSession = Depends(get_db)
):
    query = select(ContactInquiry).where(ContactInquiry.id == inquiry_id)
    result = await db.execute(query)
    inquiry = result.scalar_one_or_none()

    if not inquiry:
        raise HTTPException(status_code=404, detail="삭제할 문의 건을 찾을 수 없습니다.")

    await db.delete(inquiry)
    await db.commit()
    return {"success": True, "message": "문의가 성공적으로 삭제되었습니다."}


# ==============================================================================
# 🚀 2. 사전 예약 및 뉴스레터 구독자 관리 API
# ==============================================================================
@router.get("/api/admin/pre-registrations")
async def get_all_pre_registrations(
    reg_type: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    query = select(PreRegistration).order_by(PreRegistration.created_at.desc())
    if reg_type:
        query = query.where(PreRegistration.reg_type == reg_type)
    result = await db.execute(query)
    registrations = result.scalars().all()
    return {"success": True, "count": len(registrations), "data": [r.to_dict() for r in registrations]}


@router.get("/api/admin/pre-registrations/export-csv")
async def export_pre_registrations_csv(db: AsyncSession = Depends(get_db)):
    """사전 예약자 및 구독자 목록 CSV 다운로드"""
    query = select(PreRegistration).order_by(PreRegistration.created_at.desc())
    result = await db.execute(query)
    registrations = result.scalars().all()

    output = io.StringIO()
    # UTF-8 BOM 추가 (엑셀 한글 깨짐 방지)
    output.write('\ufeff')
    writer = csv.writer(output)
    writer.writerow(["ID", "이메일", "연락처", "신청유형", "관심분야", "신청일시"])

    for r in registrations:
        writer.writerow([
            r.id,
            r.email,
            r.phone or "",
            r.reg_type,
            r.interest or "",
            r.created_at.strftime("%Y-%m-%d %H:%M:%S") if r.created_at else ""
        ])

    output.seek(0)
    return StreamingResponse(
        io.BytesIO(output.getvalue().encode('utf-8-sig')),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=secops_pre_registrations.csv"}
    )


# ==============================================================================
# 📢 3. 관리자 공지사항 CRUD API
# ==============================================================================
@router.get("/api/admin/notices")
async def get_all_notices(db: AsyncSession = Depends(get_db)):
    query = select(Notice).order_by(Notice.is_pinned.desc(), Notice.created_at.desc())
    result = await db.execute(query)
    notices = result.scalars().all()
    return {"success": True, "count": len(notices), "data": [n.to_dict() for n in notices]}


@router.post("/api/admin/notices", status_code=status.HTTP_201_CREATED)
async def create_notice(payload: NoticeCreate, db: AsyncSession = Depends(get_db)):
    notice = Notice(
        title=payload.title,
        content=payload.content,
        badge_text=payload.badge_text,
        is_active=payload.is_active,
        is_pinned=payload.is_pinned
    )
    db.add(notice)
    await db.commit()
    await db.refresh(notice)
    return {"success": True, "message": "새 공지사항이 등록되었습니다.", "data": notice.to_dict()}


@router.put("/api/admin/notices/{notice_id}")
async def update_notice(
    notice_id: int,
    payload: NoticeUpdate,
    db: AsyncSession = Depends(get_db)
):
    query = select(Notice).where(Notice.id == notice_id)
    result = await db.execute(query)
    notice = result.scalar_one_or_none()

    if not notice:
        raise HTTPException(status_code=404, detail="수정할 공지사항을 찾을 수 없습니다.")

    if payload.title is not None:
        notice.title = payload.title
    if payload.content is not None:
        notice.content = payload.content
    if payload.badge_text is not None:
        notice.badge_text = payload.badge_text
    if payload.is_active is not None:
        notice.is_active = payload.is_active
    if payload.is_pinned is not None:
        notice.is_pinned = payload.is_pinned

    await db.commit()
    await db.refresh(notice)
    return {"success": True, "message": "공지사항이 수정되었습니다.", "data": notice.to_dict()}


@router.delete("/api/admin/notices/{notice_id}")
async def delete_notice(notice_id: int, db: AsyncSession = Depends(get_db)):
    query = select(Notice).where(Notice.id == notice_id)
    result = await db.execute(query)
    notice = result.scalar_one_or_none()

    if not notice:
        raise HTTPException(status_code=404, detail="삭제할 공지사항을 찾을 수 없습니다.")

    await db.delete(notice)
    await db.commit()
    return {"success": True, "message": "공지사항이 삭제되었습니다."}


# ==============================================================================
# ⚙️ 4. 동적 랜딩페이지 콘텐츠 관리 API
# ==============================================================================
@router.get("/api/admin/contents")
async def get_landing_contents(db: AsyncSession = Depends(get_db)):
    query = select(LandingContent)
    result = await db.execute(query)
    contents = result.scalars().all()
    content_dict = {item.key: item.value for item in contents}
    return {"success": True, "data": content_dict, "raw": [c.to_dict() for c in contents]}


@router.post("/api/admin/contents")
async def update_landing_contents(
    payload: ContentBatchUpdate,
    db: AsyncSession = Depends(get_db)
):
    """키-값 쌍 형태의 랜딩페이지 콘텐츠 일괄 등록 및 업데이트"""
    try:
        for key, value in payload.contents.items():
            query = select(LandingContent).where(LandingContent.key == key)
            result = await db.execute(query)
            existing = result.scalar_one_or_none()

            if existing:
                existing.value = str(value)
            else:
                new_item = LandingContent(key=key, value=str(value))
                db.add(new_item)

        await db.commit()
        return {"success": True, "message": "동적 콘텐츠 설정이 업데이트되었습니다."}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"콘텐츠 설정 업데이트 오류: {str(e)}")
