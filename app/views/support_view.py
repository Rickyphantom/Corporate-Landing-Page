from typing import List, Dict, Any, Optional
from app.views.components import render_head, render_sidebar, render_notice_modal

def render_support_page(
    title: str = "지원센터 — SecOps Cyber Defense",
    notices: Optional[List[Dict[str, Any]]] = None,
    active_page: str = "support"
) -> str:
    """지원센터 1:1 헬프데스크 페이지 HTML 생성 파이썬 뷰"""
    if notices is None:
        notices = []

    notice_bar_html = ""
    if notices and len(notices) > 0:
        first_n = notices[0]
        badge = first_n.get("badge_text", "NOTICE")
        n_title = first_n.get("title", "")
        n_content_summary = first_n.get("content", "")[:60]
        notice_bar_html = f"""<div class="notice-announcement-bar">
        <span class="notice-badge">{badge}</span>
        <span class="notice-text"><strong>{n_title}</strong> - {n_content_summary}...</span>
        <button class="notice-detail-btn" onclick="openNoticeModal()">상세보기 →</button>
      </div>"""

    head_html = render_head(title=title, description="SecOps 지원센터 - 24/7 핫라인, 1:1 맞춤 기술 문의, 무료 보안 진단 및 도입 컨설팅 접수.")
    sidebar_html = render_sidebar(active_page=active_page)
    modal_html = render_notice_modal(notices=notices)

    return f"""<!DOCTYPE html>
<html lang="ko">
{head_html}
<body class="standalone-page">

  <!-- 고정 사이드바 -->
  {sidebar_html}

  <!-- 메인 콘텐츠 영역 -->
  <main class="main-content">
    
    <!-- 지원센터 메인 헤더 섹션 -->
    <section class="content-section standalone-header-section">
      {notice_bar_html}

      <div class="section-badge">SUPPORT CENTER // 1:1 HELPDESK</div>
      <h1 class="hero-title">SecOps 고객 지원센터 &<br><span class="gradient-text">1:1 맞춤 엔지니어링 지원</span></h1>
      <p class="section-desc">
        24/7 SOC 전문 관제요원 및 보안 아키텍트가 기술 문의, 도입 컨설팅, 긴급 위협 대응을 신속하게 지원합니다.
      </p>

      <!-- 지원 채널 정보 카드 그리드 -->
      <div class="support-channels-grid">
        <div class="support-channel-card">
          <div class="channel-icon">🚨</div>
          <h3>24/7 SOC 긴급 핫라인</h3>
          <p class="channel-highlight">02-1588-9900</p>
          <p class="channel-desc">제로데이 침해 사고 및 실시간 위협 긴급 대응 전용 라인 (상시 운영)</p>
        </div>

        <div class="support-channel-card">
          <div class="channel-icon">✉️</div>
          <h3>기술 지원 이메일</h3>
          <p class="channel-highlight">support@secops.security</p>
          <p class="channel-desc">연동 사양, 로그 수집 설정, 시스템 장애 문의 (평균 2시간 이내 회신)</p>
        </div>

        <div class="support-channel-card">
          <div class="channel-icon">📄</div>
          <h3>문서 & API 가이드</h3>
          <p class="channel-highlight">docs.secops.security</p>
          <p class="channel-desc">에이전트 설치 가이드, RESTful API 문서 및 SIEM 연동 튜토리얼</p>
        </div>
      </div>
    </section>

    <!-- 1:1 Q&A 및 문의 접수 폼 섹션 -->
    <section class="content-section">
      <div class="support-form-wrapper">
        <!-- 1:1 문의 접수 카드 -->
        <div class="inquiry-form-container form-container-standalone">
          <div class="form-card card-lg">
            <div class="form-card-header">
              <h2>💬 1:1 기술 및 도입 문의 접수</h2>
              <p>궁금하신 기술 사양이나 맞춤 견적, 무료 POC 신청을 남겨주시면 보안 아키텍트가 확인 후 답신을 드립니다.</p>
            </div>
            
            <form id="publicInquiryForm" onsubmit="submitInquiryForm(event)">
              <div class="form-row">
                <div class="form-group flex-1">
                  <label>성함 / 담당자명 *</label>
                  <input type="text" id="inqName" class="form-input" placeholder="홍길동 팀장" required>
                </div>
                <div class="form-group flex-1">
                  <label>회사명 / 기관명</label>
                  <input type="text" id="inqCompany" class="form-input" placeholder="(주)섹옵스 테크놀로지">
                </div>
              </div>

              <div class="form-row">
                <div class="form-group flex-1">
                  <label>이메일 주소 *</label>
                  <input type="email" id="inqEmail" class="form-input" placeholder="name@company.com" required>
                </div>
                <div class="form-group flex-1">
                  <label>연락처 *</label>
                  <input type="tel" id="inqPhone" class="form-input" placeholder="010-1234-5678" required>
                </div>
              </div>

              <div class="form-group">
                <label>문의 유형 선택 *</label>
                <select id="inqType" class="form-select">
                  <option value="무료 POC/보안진단">무료 POC 신청 및 인프라 보안 진단</option>
                  <option value="견적 요청">견적 요청 및 도입 문의</option>
                  <option value="기술 문의">기술 사양 및 에이전트 연동 문의</option>
                  <option value="파트너십">파트너십 및 제휴 문의</option>
                  <option value="기타">기타 문의</option>
                </select>
              </div>

              <div class="form-group">
                <label>문의 및 요청 내용 *</label>
                <textarea id="inqMessage" class="form-textarea" rows="5" placeholder="현재 인프라 환경(클라우드/온프레미스)과 궁금하신 내용을 자유롭게 작성해 주세요..." required></textarea>
              </div>

              <div id="inquiryStatusMsg" class="form-feedback" style="display:none;"></div>

              <button type="submit" id="inqSubmitBtn" class="btn btn-primary full-width btn-lg">1:1 문의 및 진단 신청 접수</button>
            </form>
          </div>
        </div>

        <!-- 우측 사이드 바: Q&A 가이드 및 사전예약 안내 -->
        <div class="support-sidebar-info">
          <div class="info-card">
            <h3>❓ 자주 묻는 질문 지식베이스</h3>
            <p>신규 도입 시 가장 많이 들어오는 기술/보안 답변을 바로 검색할 수 있습니다.</p>
            <a href="/qna" class="btn btn-secondary full-width">Q&A 바로가기 →</a>
          </div>

          <div class="info-card pre-reg-card">
            <h3>🎁 위협 리포트 & 소식지 구독</h3>
            <p>월간 위협 인텔리전스 분석 리포트와 패치 권고안을 이메일로 받아보세요.</p>
            <form onsubmit="submitPreRegSupport(event)" class="pre-reg-form">
              <input type="email" id="supportPreRegEmail" placeholder="이메일 주소 입력..." class="form-input" required>
              <button type="submit" class="btn btn-primary full-width">리포트 구독 신청</button>
            </form>
            <div id="supportPreRegStatus" class="form-feedback" style="display:none; margin-top: 10px;"></div>
          </div>
        </div>
      </div>
    </section>

  </main>

  <!-- 공지사항 모달 -->
  {modal_html}

  <!-- 메인 스크립트 연결 -->
  <script src="/static/js/main.js"></script>
  <script>
    async function submitPreRegSupport(e) {{
      e.preventDefault();
      const email = document.getElementById('supportPreRegEmail').value.trim();
      const statusEl = document.getElementById('supportPreRegStatus');

      try {{
        const res = await fetch('/api/pre-registration', {{
          method: 'POST',
          headers: {{ 'Content-Type': 'application/json' }},
          body: JSON.stringify({{
            email: email,
            reg_type: '리포트구독',
            interest: '보안 인텔리전스 리포트'
          }})
        }});
        const data = await res.json();
        if (res.ok && data.success) {{
          statusEl.className = 'form-feedback success';
          statusEl.textContent = '✅ ' + data.message;
          statusEl.style.display = 'block';
          document.getElementById('supportPreRegEmail').value = '';
        }} else {{
          statusEl.className = 'form-feedback error';
          statusEl.textContent = '❌ ' + (data.detail || '구독 처리 실패');
          statusEl.style.display = 'block';
        }}
      }} catch (err) {{
        statusEl.className = 'form-feedback error';
        statusEl.textContent = '❌ 통신 오류가 발생했습니다.';
        statusEl.style.display = 'block';
      }}
    }}
  </script>
</body>
</html>"""
