from typing import Optional, Dict
from pydantic import BaseModel, EmailStr, Field

class ContactInquiryCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="이름/담당자명")
    email: EmailStr = Field(..., description="이메일 주소")
    phone: str = Field(..., min_length=8, max_length=50, description="연락처")
    company: Optional[str] = Field(None, max_length=150, description="회사명/직함")
    inquiry_type: str = Field("견적 요청", description="문의 유형")
    message: str = Field(..., min_length=5, description="문의 및 요청 상세 내용")

class ContactStatusUpdate(BaseModel):
    status: str = Field(..., description="상태: PENDING, IN_PROGRESS, COMPLETED")

class PreRegistrationCreate(BaseModel):
    email: EmailStr = Field(..., description="이메일 주소")
    phone: Optional[str] = Field(None, description="연락처")
    reg_type: str = Field("PRE_REGISTER", description="신청 유형: PRE_REGISTER 또는 NEWSLETTER")
    interest: Optional[str] = Field(None, description="관심 서비스 분야")

class NoticeCreate(BaseModel):
    title: str = Field(..., min_length=2, max_length=255, description="공지사항 제목")
    content: str = Field(..., description="공지사항 내용")
    badge_text: str = Field("NOTICE", description="배지 텍스트")
    is_active: bool = Field(True, description="게시 여부")
    is_pinned: bool = Field(False, description="상단 고정 여부")

class NoticeUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    badge_text: Optional[str] = None
    is_active: Optional[bool] = None
    is_pinned: Optional[bool] = None

class FaqCreate(BaseModel):
    category: str = Field("일반", description="카테고리")
    question: str = Field(..., min_length=2, description="질문 내용")
    answer: str = Field(..., min_length=2, description="답변 내용")
    order_num: int = Field(0, description="정렬 순서")
    is_active: bool = Field(True, description="활성화 여부")

class FaqUpdate(BaseModel):
    category: Optional[str] = None
    question: Optional[str] = None
    answer: Optional[str] = None
    order_num: Optional[int] = None
    is_active: Optional[bool] = None

class ContentBatchUpdate(BaseModel):
    contents: Dict[str, str] = Field(..., description="키-값 형태의 랜딩페이지 설정 내용")

class AdminLoginPayload(BaseModel):
    password: str = Field(..., description="관리자 인증 비밀번호")

