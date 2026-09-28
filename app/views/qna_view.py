from typing import List, Dict, Any, Optional
from app.views.components import render_head, render_sidebar

def render_qna_page(
    title: str = "Q&A 지식베이스 — SecOps Cyber Defense",
    faqs: Optional[List[Dict[str, Any]]] = None,
    active_page: str = "qna"
) -> str:
    """Q&A FAQ 페이지 HTML 생성 파이썬 뷰"""
    head_html = render_head(title=title, description="SecOps Q&A 및 자주 묻는 질문(FAQ) 지식베이스.")
    sidebar_html = render_sidebar(active_page=active_page)

    faq_items_html = ""
    if faqs and len(faqs) > 0:
        for faq in faqs:
            cat = faq.get("category", "일반")
            q = faq.get("question", "")
            a = faq.get("answer", "")
            faq_items_html += f"""
            <div class="faq-item" data-category="{cat}" data-question="{q}">
              <button class="faq-question" onclick="toggleFaq(this)">
                <span class="faq-cat-tag">{cat}</span>
                <span class="faq-title">Q. {q}</span>
                <span class="faq-icon">+</span>
              </button>
              <div class="faq-answer">
                <p>{a}</p>
              </div>
            </div>"""
    else:
        # 기본 FAQ 아이템
        faq_items_html = """
            <div class="faq-item" data-category="서비스/도입" data-question="기존 온프레미스 및 레거시 시스템과 연동이 가능한가요?">
              <button class="faq-question" onclick="toggleFaq(this)">
                <span class="faq-cat-tag">서비스/도입</span>
                <span class="faq-title">Q. 기존 온프레미스 및 레거시 시스템과 연동이 가능한가요?</span>
                <span class="faq-icon">+</span>
              </button>
              <div class="faq-answer">
                <p>네, 가능합니다. SecOps는 주요 퍼블릭 클라우드뿐만 아니라 온프레미스 베어메탈 서버 환경을 위한 경량 보안 에이전트와 Syslog/SIEM 연동 API를 공식 지원합니다.</p>
              </div>
            </div>

            <div class="faq-item" data-category="기술/보안" data-question="AI 탐지 모델의 오탐률(False Positive) 관리 방안은 어떻게 되나요?">
              <button class="faq-question" onclick="toggleFaq(this)">
                <span class="faq-cat-tag">기술/보안</span>
                <span class="faq-title">Q. AI 탐지 모델의 오탐률(False Positive) 관리 방안은 어떻게 되나요?</span>
                <span class="faq-icon">+</span>
              </button>
              <div class="faq-answer">
                <p>SecOps 신경망 엔진은 자율 학습 알고리즘을 도입하여 각 기업의 정상 트래픽 패턴을 기본 베이스라인으로 학습합니다. 99.98% 이상의 정밀도를 기록하며, 위험도가 낮은 경보는 자동으로 필터링됩니다.</p>
              </div>
            </div>

            <div class="faq-item" data-category="컨설팅/비용" data-question="무료 보안 진단 및 POC(개념 검증) 수행 절차가 궁금합니다.">
              <button class="faq-question" onclick="toggleFaq(this)">
                <span class="faq-cat-tag">컨설팅/비용</span>
                <span class="faq-title">Q. 무료 보안 진단 및 POC(개념 검증) 수행 절차가 궁금합니다.</span>
                <span class="faq-icon">+</span>
              </button>
              <div class="faq-answer">
                <p>지원센터를 통해 신청해주시면 전문 보안 엔지니어가 1:1 상담 후 2주간 무료 POC 환경을 구성해 드립니다. 실제 조직 인프라 기반의 위협 가시성 리포트가 무료로 제공됩니다.</p>
              </div>
            </div>"""

    return f"""<!DOCTYPE html>
<html lang="ko">
{head_html}
<body class="standalone-page">

  <!-- 고정 사이드바 -->
  {sidebar_html}

  <!-- 메인 콘텐츠 영역 -->
  <main class="main-content">
    
    <!-- Q&A 메인 헤더 섹션 -->
    <section class="content-section standalone-header-section">
      <div class="section-badge">KNOWLEDGEBASE // FAQ</div>
      <h1 class="hero-title">SecOps Q&A &<br><span class="gradient-text">자주 묻는 질문 센터</span></h1>
      <p class="section-desc">
        SecOps 자율 보안 솔루션 도입부터 인프라 연동, 컴플라이언스, 라이선스 체계까지 자주 검색되는 주요 문의 사항을 확인하세요.
      </p>

      <!-- FAQ 검색 & 필터 바 -->
      <div class="qna-search-wrapper">
        <div class="faq-search-box search-box-lg">
          <span class="search-icon">🔍</span>
          <input type="text" id="faqSearchInput" placeholder="궁금하신 내용이나 키워드를 검색해보세요 (예: 온프레미스, 제로데이, 비용)..." onkeyup="filterFaqs()">
        </div>

        <div class="faq-category-tabs tabs-lg">
          <button class="faq-cat-btn active" onclick="filterFaqCategory('ALL')">전체보기</button>
          <button class="faq-cat-btn" onclick="filterFaqCategory('서비스/도입')">서비스/도입</button>
          <button class="faq-cat-btn" onclick="filterFaqCategory('기술/보안')">기술/보안</button>
          <button class="faq-cat-btn" onclick="filterFaqCategory('컨설팅/비용')">컨설팅/비용</button>
          <button class="faq-cat-btn" onclick="filterFaqCategory('컴플라이언스')">컴플라이언스</button>
        </div>
      </div>
    </section>

    <!-- FAQ 아코디언 목록 섹션 -->
    <section class="content-section">
      <div class="faq-standalone-container">
        <div class="faq-accordion-list" id="faqAccordionList">
          {faq_items_html}
        </div>

        <!-- 1:1 지원센터 연결 CTA 카드 -->
        <div class="qna-cta-card">
          <div class="cta-icon">💬</div>
          <div class="cta-text">
            <h3>찾으시는 답변을 얻지 못하셨나요?</h3>
            <p>보안 아키텍트와 1:1 상담을 진행하거나 맞춤 기술 사양을 문의하실 수 있습니다.</p>
          </div>
          <a href="/support" class="btn btn-primary">1:1 지원센터 문의하기 →</a>
        </div>
      </div>
    </section>

  </main>

  <!-- 메인 스크립트 연결 -->
  <script src="/static/js/main.js"></script>
</body>
</html>"""
