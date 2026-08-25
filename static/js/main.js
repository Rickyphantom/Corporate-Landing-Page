/**
 * SecOps 기업 랜딩 페이지 메인 스크립트
 * - 화면 중앙 기준 거리 기반 텍스트/섹션 부드러운 투명도(Opacity) 제어
 * - 스크롤에 따른 사이드바 Active 메뉴 하이라이트 동기화
 * - FAQ (Q&A) 아코디언 및 카테고리/검색 필터 기능
 * - 1:1 Q&A 문의 접수 AJAX 전송 및 비밀 관리자 단축키 지원 (Ctrl+Shift+A)
 */

document.addEventListener('DOMContentLoaded', () => {
  const sections = document.querySelectorAll('.content-section');
  const navLinks = document.querySelectorAll('.sidebar-nav .nav-item');
  const isMainLandingPage = (window.location.pathname === '/' || window.location.pathname === '/index.html');

  function updateScrollEffects() {
    if (!isMainLandingPage) {
      sections.forEach((sec) => {
        sec.style.opacity = '1';
      });
      return;
    }

    const windowHeight = window.innerHeight;
    const windowCenter = windowHeight / 2;

    let closestSection = null;
    let minDistance = Infinity;

    sections.forEach((sec) => {
      const rect = sec.getBoundingClientRect();
      const secCenter = rect.top + rect.height / 2;

      const distance = Math.abs(windowCenter - secCenter);

      const maxDistance = windowHeight * 0.6;
      let opacity = 1 - distance / maxDistance;

      if (opacity < 0.1) opacity = 0.1;
      if (opacity > 1) opacity = 1;

      sec.style.opacity = opacity;

      if (distance < minDistance) {
        minDistance = distance;
        closestSection = sec;
      }
    });

    if (closestSection) {
      const currentId = closestSection.getAttribute('id');
      navLinks.forEach((link) => {
        const href = link.getAttribute('href');
        if (href === `#${currentId}`) {
          link.classList.add('active');
        } else {
          link.classList.remove('active');
        }
      });
    }
  }

  window.addEventListener('scroll', updateScrollEffects, { passive: true });
  window.addEventListener('resize', updateScrollEffects, { passive: true });
  updateScrollEffects();

  // 🔑 혜안 단축키: Ctrl + Shift + A 누를 시 관리자 페이지로 비밀 이동
  window.addEventListener('keydown', (e) => {
    if (e.ctrlKey && e.shiftKey && (e.key === 'A' || e.key === 'a')) {
      e.preventDefault();
      window.location.href = '/admin';
    }
  });
});

// -----------------------------------------------------------------------------
// ❓ FAQ (Q&A) 인터랙션 함수
// -----------------------------------------------------------------------------
function toggleFaq(btn) {
  const faqItem = btn.closest('.faq-item');
  const isOpen = faqItem.classList.contains('active');

  // 다른 모든 아코디언 닫기
  document.querySelectorAll('.faq-item').forEach(item => {
    item.classList.remove('active');
    const icon = item.querySelector('.faq-icon');
    if (icon) icon.textContent = '+';
  });

  if (!isOpen) {
    faqItem.classList.add('active');
    const icon = faqItem.querySelector('.faq-icon');
    if (icon) icon.textContent = '−';
  }
}

let activeCategory = 'ALL';

function filterFaqCategory(category) {
  activeCategory = category;
  document.querySelectorAll('.faq-cat-btn').forEach(btn => {
    if (btn.textContent.trim() === category || (category === 'ALL' && btn.textContent.trim() === '전체')) {
      btn.classList.add('active');
    } else {
      btn.classList.remove('active');
    }
  });
  filterFaqs();
}

function filterFaqs() {
  const searchInput = document.getElementById('faqSearchInput');
  const query = searchInput ? searchInput.value.toLowerCase().trim() : '';
  const faqItems = document.querySelectorAll('#faqAccordionList .faq-item');

  faqItems.forEach(item => {
    const cat = item.getAttribute('data-category') || '';
    const qText = item.getAttribute('data-question') || '';
    const fullText = item.textContent.toLowerCase();

    const matchesCategory = (activeCategory === 'ALL' || cat === activeCategory);
    const matchesSearch = (!query || fullText.includes(query) || qText.toLowerCase().includes(query));

    if (matchesCategory && matchesSearch) {
      item.style.display = 'block';
    } else {
      item.style.display = 'none';
    }
  });
}

// -----------------------------------------------------------------------------
// 💬 1:1 Q&A 및 문의 접수 전송
// -----------------------------------------------------------------------------
async function submitInquiryForm(e) {
  e.preventDefault();

  const name = document.getElementById('inqName').value.trim();
  const email = document.getElementById('inqEmail').value.trim();
  const phone = document.getElementById('inqPhone').value.trim();
  const company = document.getElementById('inqCompany').value.trim();
  const inquiry_type = document.getElementById('inqType').value;
  const message = document.getElementById('inqMessage').value.trim();

  const statusMsgEl = document.getElementById('inquiryStatusMsg');
  const submitBtn = document.getElementById('inqSubmitBtn');

  submitBtn.disabled = true;
  submitBtn.textContent = '접수 진행 중...';

  try {
    const response = await fetch('/api/contact', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name,
        email,
        phone,
        company,
        inquiry_type,
        message
      })
    });

    const result = await response.json();

    if (response.ok && result.success) {
      statusMsgEl.className = 'form-feedback success';
      statusMsgEl.textContent = '✅ ' + result.message;
      statusMsgEl.style.display = 'block';
      document.getElementById('publicInquiryForm').reset();
    } else {
      statusMsgEl.className = 'form-feedback error';
      statusMsgEl.textContent = '❌ ' + (result.detail || '문의 접수 중 오류가 발생했습니다.');
      statusMsgEl.style.display = 'block';
    }
  } catch (err) {
    statusMsgEl.className = 'form-feedback error';
    statusMsgEl.textContent = '❌ 서버 통신 오류가 발생했습니다. 잠시 후 다시 시도해 주세요.';
    statusMsgEl.style.display = 'block';
  } finally {
    submitBtn.disabled = false;
    submitBtn.textContent = '문의 및 Q&A 접수하기';
  }
}

// -----------------------------------------------------------------------------
// 📢 공지사항 모달
// -----------------------------------------------------------------------------
function openNoticeModal() {
  const modal = document.getElementById('publicNoticeModal');
  if (modal) modal.style.display = 'flex';
}

function closeNoticeModal() {
  const modal = document.getElementById('publicNoticeModal');
  if (modal) modal.style.display = 'none';
}
