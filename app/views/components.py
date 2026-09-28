from typing import List, Dict, Any

def render_head(title: str, description: str = "", extra_css: str = "") -> str:
    """공통 HTML Head 영역 생성"""
    if not description:
        description = "SecOps - 차세대 자율형 사이버 방어 및 위협 인텔리전스 플랫폼. 실시간 위협 탐지, 제로데이 방어, 자동화된 보안 파이프라인."
    
    css_extra = f'<link rel="stylesheet" href="{extra_css}">' if extra_css else ""
    
    return f"""<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="{description}">
  <title>{title}</title>
  
  <!-- Google Fonts & Pretendard CDN -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css">
  
  <!-- 스타일시트 -->
  <link rel="stylesheet" href="/static/css/style.css">
  {css_extra}
</head>"""

def render_sidebar(active_page: str = 'index') -> str:
    """고정 사이드바 HTML 컴포넌트 생성"""
    is_index = "active" if active_page == "index" else ""
    return f"""<aside class="sidebar" id="sidebar">
  <div class="sidebar-top">
    <div class="sidebar-logo" onclick="location.href='/';" style="cursor: pointer;">
      <div class="logo-badge">
        <span class="pulse-dot"></span>
        <span class="logo-tag">SEC-V3</span>
      </div>
      <h2>SecOps</h2>
      <p>Cyber Defense & Intelligence</p>
    </div>
    
    <nav class="sidebar-nav">
      <ul>
        <li>
          <a href="/#section1" class="nav-item {is_index}">
            <span class="nav-idx">01.</span>
            <span class="nav-label">Overview</span>
          </a>
        </li>
        <li>
          <a href="/#section2" class="nav-item">
            <span class="nav-idx">02.</span>
            <span class="nav-label">Threat Intelligence</span>
          </a>
        </li>
        <li>
          <a href="/#section3" class="nav-item">
            <span class="nav-idx">03.</span>
            <span class="nav-label">Pipeline</span>
          </a>
        </li>
        <li>
          <a href="/#section4" class="nav-item">
            <span class="nav-idx">04.</span>
            <span class="nav-label">Experience</span>
          </a>
        </li>
        <li>
          <a href="/#section5" class="nav-item">
            <span class="nav-idx">05.</span>
            <span class="nav-label">Hub (Q&A/Support)</span>
          </a>
        </li>
      </ul>
    </nav>
  </div>

  <div class="sidebar-footer">
    <div class="system-status" onclick="location.href='/admin';" title="관리자 콘솔 접속 (Ctrl+Shift+A)" style="cursor: pointer;">
      <div class="status-indicator"></div>
      <div class="status-text">
        <span class="status-title">System Status <small style="opacity:0.4; font-size:10px;">🔒</small></span>
        <span class="status-value">Defenses Active</span>
      </div>
    </div>
    <a href="/support" class="sidebar-cta">1:1 지원센터 문의</a>
  </div>
</aside>"""

def render_notice_modal(notices: List[Dict[str, Any]]) -> str:
    """공지사항 상세 모달 HTML 컴포넌트 생성"""
    if not notices or len(notices) == 0:
        return ""
    
    notice = notices[0]
    badge_text = notice.get("badge_text", "NOTICE")
    title = notice.get("title", "")
    created_at = notice.get("created_at", "")
    content = notice.get("content", "")
    
    return f"""<div id="publicNoticeModal" class="admin-modal-overlay">
  <div class="admin-modal">
    <div class="modal-header">
      <h4>📢 {badge_text}</h4>
      <button onclick="closeNoticeModal()" class="modal-close-btn">&times;</button>
    </div>
    <div class="inquiry-detail-body">
      <h3>{title}</h3>
      <p class="text-muted"><small>등록일: {created_at}</small></p>
      <hr class="modal-divider">
      <div class="detail-content-box">{content}</div>
    </div>
    <div class="modal-footer">
      <button type="button" onclick="closeNoticeModal()" class="btn btn-primary">확인</button>
    </div>
  </div>
</div>"""
