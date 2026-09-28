from typing import Dict, List, Any, Optional
from app.views.components import render_head, render_sidebar, render_notice_modal

def render_index_page(
    title: str = "SecOps — Next-Gen Cyber Defense",
    contents: Optional[Dict[str, str]] = None,
    notices: Optional[List[Dict[str, Any]]] = None,
    faqs: Optional[List[Dict[str, Any]]] = None,
    active_page: str = "index"
) -> str:
    """메인 랜딩페이지 HTML 생성 파이썬 뷰"""
    if contents is None:
        contents = {}
    if notices is None:
        notices = []
    
    # 01. Overview 섹션 데이터
    hero_title = contents.get(
        "hero_title",
        '자율형 보안 관제 &<br><span class="gradient-text">지능형 사이버 방어</span>'
    )
    hero_subtitle = contents.get(
        "hero_subtitle",
        "복잡해지는 멀티클라우드 환경과 고도화된 제로데이 공격을 실시간 신경망 엔진으로 감지하고 0.4초 이내에 자동 차단 및 격리합니다."
    )
    stat_detection = contents.get("stat_detection_rate", "99.98%")
    stat_response = contents.get("stat_response_time", "< 0.4s")
    stat_daily = contents.get("stat_daily_attacks", "10M+")

    # 상단 공지 배너
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

    head_html = render_head(title=title)
    sidebar_html = render_sidebar(active_page=active_page)
    modal_html = render_notice_modal(notices=notices)

    return f"""<!DOCTYPE html>
<html lang="ko">
{head_html}
<body>

  <!-- 고정 사이드바 -->
  {sidebar_html}

  <!-- 메인 콘텐츠 영역 -->
  <main class="main-content">
    
    <!-- 01. Overview 섹션 -->
    <section id="section1" class="content-section">
      {notice_bar_html}
      
      <div class="section-badge">01 // OVERVIEW</div>
      <h1 class="hero-title">{hero_title}</h1>
      <p class="section-desc">
        {hero_subtitle}
      </p>
      
      <div class="stats-grid">
        <div class="stat-card">
          <span class="stat-number">{stat_detection}</span>
          <span class="stat-label">실시간 위협 탐지율</span>
        </div>
        <div class="stat-card">
          <span class="stat-number">{stat_response}</span>
          <span class="stat-label">평균 사고 대응 시간</span>
        </div>
        <div class="stat-card">
          <span class="stat-number">{stat_daily}</span>
          <span class="stat-label">일일 방어 공격 건수</span>
        </div>
      </div>

      <div class="btn-group">
        <a href="#section2" class="btn btn-primary">위협 인텔리전스 탐색</a>
        <a href="/qna" class="btn btn-secondary">Q&A 지식베이스</a>
        <a href="/support" class="btn btn-secondary border-cyan">1:1 지원센터 문의</a>
      </div>
    </section>

    <!-- 02. Threat Intelligence 섹션 -->
    <section id="section2" class="content-section">
      <div class="section-badge">02 // THREAT INTELLIGENCE</div>
      <h1 class="hero-title">실시간 글로벌<br><span class="gradient-text">위협 인텔리전스 레이더</span></h1>
      <p class="section-desc">
        전 세계 180개국 엔드포인트에서 발생하는 텔레메트리 데이터를 실시간 상관 분석하여 조직에 닥칠 위협 벡터를 선제적으로 무력화합니다.
      </p>

      <div class="features-grid">
        <div class="feature-card">
          <div class="card-icon">🛡️</div>
          <h3>제로데이 행위 기반 차단</h3>
          <p>시그니처가 존재하지 않는 신종 악성코드 및 랜섬웨어의 메모리 내 이상 행위를 마이크로초 단위로 포착합니다.</p>
          <div class="card-meta"><span>Zero-Day Shield Active</span></div>
        </div>

        <div class="feature-card">
          <div class="card-icon">⚡</div>
          <h3>MITRE ATT&CK 자동 매핑</h3>
          <p>공격자의 전술·기법·절차(TTP)를 실시간 추적하여 침투 경로를 시각화하고 잠재 취약 구간을 사전 방어합니다.</p>
          <div class="card-meta"><span>TTP Graph v4.2</span></div>
        </div>

        <div class="feature-card">
          <div class="card-icon">🌐</div>
          <h3>멀티클라우드 워크로드 가시성</h3>
          <p>AWS, Azure, GCP 및 쿠버네티스 컨테이너 환경 전반의 보안 태세를 단일 대시보드에서 일괄 통제합니다.</p>
          <div class="card-meta"><span>Cross-Cloud Sync</span></div>
        </div>
      </div>
    </section>

    <!-- 03. Pipeline 섹션 -->
    <section id="section3" class="content-section">
      <div class="section-badge">03 // PIPELINE</div>
      <h1 class="hero-title">엔드투엔드<br><span class="gradient-text">보안 오케스트레이션 파이프라인</span></h1>
      <p class="section-desc">
        위협 수집부터 정밀 분석, 자율 격리 및 복구까지 전 과정이 사람의 수동 개입 없이 유기적으로 동작하는 SOAR 파이프라인입니다.
      </p>

      <div class="pipeline-flow">
        <div class="pipeline-step">
          <div class="step-num">STEP 01</div>
          <h4>Telemetry Ingestion</h4>
          <p>네트워크 트래픽, 엔드포인트 로그, API 호출을 무손실 실시간 수집</p>
        </div>
        <div class="pipeline-arrow">→</div>
        
        <div class="pipeline-step">
          <div class="step-num">STEP 02</div>
          <h4>Neural Detection</h4>
          <p>경량 신경망 AI 모델을 통한 비정상 패턴 추론 및 오탐 필터링</p>
        </div>
        <div class="pipeline-arrow">→</div>

        <div class="pipeline-step">
          <div class="step-num">STEP 03</div>
          <h4>Automated Containment</h4>
          <p>네트워크 마이크로 세그멘테이션으로 감염 노드 즉각 격리</p>
        </div>
        <div class="pipeline-arrow">→</div>

        <div class="pipeline-step">
          <div class="step-num">STEP 04</div>
          <h4>Forensic & Recovery</h4>
          <p>AI 포렌식 리포트 자동 생성 및 롤백 스냅샷 복구 가동</p>
        </div>
      </div>
    </section>

    <!-- 04. Experience 섹션 -->
    <section id="section4" class="content-section">
      <div class="section-badge">04 // EXPERIENCE</div>
      <h1 class="hero-title">엔터프라이즈를 위한<br><span class="gradient-text">최상의 보안 신뢰성</span></h1>
      <p class="section-desc">
        글로벌 금융, 핀테크, 하이테크 기업들이 SecOps의 강력한 보안 인프라 위에서 안심하고 비즈니스를 확장하고 있습니다.
      </p>

      <div class="experience-wrapper">
        <div class="compliance-box">
          <h3>보안 표준 및 컴플라이언스 준수</h3>
          <p>SOC 2 Type II, ISO/IEC 27001, ISMS-P 및 GDPR 인증을 모두 획득하여 최고 수준의 데이터 보호 체계를 보장합니다.</p>
          <div class="badge-list">
            <span class="cert-badge">SOC2 Type II</span>
            <span class="cert-badge">ISO 27001</span>
            <span class="cert-badge">ISMS-P</span>
            <span class="cert-badge">GDPR Compliant</span>
          </div>
        </div>

        <div class="contact-card">
          <h3>맞춤형 보안 컨설팅 신청</h3>
          <p>전문 SecOps 엔지니어와 함께 현재 인프라의 취약점을 진단하고 맞춤형 방어 파이프라인을 구축하세요.</p>
          <form class="demo-form" onsubmit="event.preventDefault(); alert('보안 진단 신청이 완료되었습니다. 담당자가 곧 연락드립니다.');">
            <input type="email" placeholder="회사 이메일 주소 (name@company.com)" required class="form-input">
            <button type="submit" class="btn btn-primary full-width">무료 보안 진단 신청</button>
          </form>
        </div>
      </div>
    </section>

    <!-- 05. Q&A & Support 허브 섹션 -->
    <section id="section5" class="content-section">
      <div class="section-badge">05 // HUB</div>
      <h1 class="hero-title">지식베이스 &<br><span class="gradient-text">1:1 고객 지원센터</span></h1>
      <p class="section-desc">
        자주 묻는 질문 지식베이스와 24/7 전문 보안 엔지니어링 지원센터를 독립된 전용 페이지에서 제공합니다.
      </p>

      <div class="hub-cards-grid">
        <div class="hub-card">
          <div class="hub-badge">KNOWLEDGEBASE</div>
          <div class="hub-icon">❓</div>
          <h3>Q&A 자주 묻는 질문</h3>
          <p>솔루션 도입, 온프레미스/클라우드 연동 사양, AI 알고리즘 및 컴플라이언스 FAQ를 검색하세요.</p>
          <a href="/qna" class="btn btn-primary full-width">Q&A 지식베이스 이동 →</a>
        </div>

        <div class="hub-card">
          <div class="hub-badge badge-cyan">SUPPORT CENTER</div>
          <div class="hub-icon">💬</div>
          <h3>1:1 기술 및 도입 지원센터</h3>
          <p>24/7 SOC 핫라인, 1:1 기술 및 견적 문의, 무료 인프라 보안 진단/POC를 신청하세요.</p>
          <a href="/support" class="btn btn-secondary full-width">1:1 지원센터 문의하기 →</a>
        </div>
      </div>
    </section>

  </main>

  <!-- 공지사항 모달 -->
  {modal_html}

  <!-- 메인 스크립트 연결 -->
  <script src="/static/js/main.js"></script>
</body>
</html>"""
