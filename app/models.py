from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from app.database import Base

class ContactInquiry(Base):
    """방문자 문의 및 견적 요청 모델"""
    __tablename__ = "contact_inquiries"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, index=True)
    phone = Column(String(50), nullable=False)
    company = Column(String(150), nullable=True)
    inquiry_type = Column(String(50), nullable=False, default="견적 요청")
    message = Column(Text, nullable=False)
    status = Column(String(20), nullable=False, default="PENDING")  # PENDING, IN_PROGRESS, COMPLETED
    created_at = Column(DateTime, default=datetime.utcnow)

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

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(255), nullable=False, index=True)
    phone = Column(String(50), nullable=True)
    reg_type = Column(String(50), nullable=False, default="PRE_REGISTER")  # PRE_REGISTER, NEWSLETTER
    interest = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

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

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    key = Column(String(100), unique=True, index=True, nullable=False)
    value = Column(Text, nullable=False)
    section_name = Column(String(100), nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

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

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    badge_text = Column(String(50), nullable=False, default="NOTICE")
    is_active = Column(Boolean, default=True)
    is_pinned = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

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
