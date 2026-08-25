from datetime import datetime
from typing import Optional
from sqlalchemy import String, Text, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class ContactInquiry(Base):
    """방문자 문의 및 견적 요청 모델"""
    __tablename__ = "contact_inquiries"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    phone: Mapped[str] = mapped_column(String(50), nullable=False)
    company: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
    inquiry_type: Mapped[str] = mapped_column(String(50), nullable=False, default="견적 요청")
    message: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="PENDING")  # PENDING, IN_PROGRESS, COMPLETED
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "company": self.company or "",
            "inquiry_type": self.inquiry_type,
            "message": self.message,
            "status": self.status,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else ""
        }

class PreRegistration(Base):
    """사전 예약 및 뉴스레터 구독 수집 모델"""
    __tablename__ = "pre_registrations"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    phone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    reg_type: Mapped[str] = mapped_column(String(50), nullable=False, default="PRE_REGISTER")  # PRE_REGISTER, NEWSLETTER
    interest: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "phone": self.phone or "",
            "reg_type": self.reg_type,
            "interest": self.interest or "",
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else ""
        }

class LandingContent(Base):
    """관리자 동적 랜딩페이지 텍스트/데이터 설정 모델"""
    __tablename__ = "landing_contents"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    key: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    value: Mapped[str] = mapped_column(Text, nullable=False)
    section_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "key": self.key,
            "value": self.value,
            "section_name": self.section_name or "",
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S") if self.updated_at else ""
        }

class Notice(Base):
    """관리자 공지사항 및 새소식 모델"""
    __tablename__ = "notices"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    badge_text: Mapped[str] = mapped_column(String(50), nullable=False, default="NOTICE")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_pinned: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "badge_text": self.badge_text,
            "is_active": self.is_active,
            "is_pinned": self.is_pinned,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else ""
        }

class FaqItem(Base):
    """자주 묻는 질문 (Q&A) 모델"""
    __tablename__ = "faq_items"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    category: Mapped[str] = mapped_column(String(50), nullable=False, default="일반")
    question: Mapped[str] = mapped_column(String(255), nullable=False)
    answer: Mapped[str] = mapped_column(Text, nullable=False)
    order_num: Mapped[int] = mapped_column(default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "category": self.category,
            "question": self.question,
            "answer": self.answer,
            "order_num": self.order_num,
            "is_active": self.is_active,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else ""
        }
