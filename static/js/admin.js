/**
 * SecOps Admin Portal - Client-Side Controller
 */

// 페이지 로드 시 인증 상태 확인
document.addEventListener('DOMContentLoaded', () => {
  const token = sessionStorage.getItem('secops_admin_auth');
  if (token === 'authenticated') {
    showAdminDashboard();
  } else {
    showAuthModal();
  }
});

function showAuthModal() {
  document.getElementById('authModal').style.display = 'flex';
  document.getElementById('adminApp').style.display = 'none';
  document.getElementById('adminPasswordInput').focus();
}

function showAdminDashboard() {
  document.getElementById('authModal').style.display = 'none';
  document.getElementById('adminApp').style.display = 'block';
  loadAdminStats();
  loadAdminInquiries();
  loadAdminFaqs();
  loadAdminPreRegs();
  loadAdminNotices();
  loadAdminContents();
}

async function handleAdminAuth() {
  const password = document.getElementById('adminPasswordInput').value;
  const errorMsgEl = document.getElementById('authErrorMsg');

  try {
    const response = await fetch('/api/admin/verify-password', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ password })
    });

    const res = await response.json();
    if (response.ok && res.success) {
      sessionStorage.setItem('secops_admin_auth', 'authenticated');
      errorMsgEl.style.display = 'none';
      showAdminDashboard();
    } else {
      errorMsgEl.textContent = res.detail || '비밀번호가 올바르지 않습니다.';
      errorMsgEl.style.display = 'block';
    }
  } catch (err) {
    errorMsgEl.textContent = '인증 요청 중 오류가 발생했습니다.';
    errorMsgEl.style.display = 'block';
  }
}

function handleAdminLogout() {
  sessionStorage.removeItem('secops_admin_auth');
  location.reload();
}

function switchAdminTab(tabName) {
  document.querySelectorAll('.admin-tab-btn').forEach(btn => btn.classList.remove('active'));
  document.querySelectorAll('.admin-tab-content').forEach(content => content.classList.remove('active'));

  const targetTab = document.getElementById(`tab-${tabName}`);
  if (targetTab) {
    targetTab.classList.add('active');
  }

  // 탭 버튼 active 제어
  const clickedBtn = Array.from(document.querySelectorAll('.admin-tab-btn'))
    .find(b => b.getAttribute('onclick').includes(tabName));
  if (clickedBtn) clickedBtn.classList.add('active');
}

// -----------------------------------------------------------------------------
// 📊 01. 통계 데이터 불러오기
// -----------------------------------------------------------------------------
async function loadAdminStats() {
  try {
    const res = await fetch('/api/admin/stats').then(r => r.json());
    if (res.success && res.data) {
      document.getElementById('statInquiries').textContent = res.data.total_inquiries;
      document.getElementById('statPendingInquiries').textContent = res.data.pending_inquiries;
      document.getElementById('statPreRegs').textContent = res.data.total_pre_regs;
      document.getElementById('statNotices').textContent = res.data.total_notices;
      document.getElementById('statFaqs').textContent = res.data.total_faqs;

      const pendingBadge = document.getElementById('pendingBadge');
      if (res.data.pending_inquiries > 0) {
        pendingBadge.textContent = res.data.pending_inquiries;
        pendingBadge.style.display = 'inline-block';
      } else {
        pendingBadge.style.display = 'none';
      }
    }
  } catch (err) {
    console.error('Failed to load stats', err);
  }
}

// -----------------------------------------------------------------------------
// 💬 02. 문의 내역 관리
// -----------------------------------------------------------------------------
let inquiriesCache = [];

async function loadAdminInquiries() {
  const filter = document.getElementById('inquiryStatusFilter').value;
  const tbody = document.getElementById('inquiriesTableBody');
  tbody.innerHTML = '<tr><td colspan="8" class="text-center">조회 중...</td></tr>';

  try {
    const url = filter ? `/api/admin/inquiries?status_filter=${filter}` : '/api/admin/inquiries';
    const res = await fetch(url).then(r => r.json());

    if (res.success && res.data) {
      inquiriesCache = res.data;
      if (res.data.length === 0) {
        tbody.innerHTML = '<tr><td colspan="8" class="text-center text-muted">등록된 문의 건이 없습니다.</td></tr>';
        return;
      }

      tbody.innerHTML = res.data.map(item => `
        <tr>
          <td>#${item.id}</td>
          <td><strong>${escapeHtml(item.name)}</strong></td>
          <td>${escapeHtml(item.email)}<br><small class="text-muted">${escapeHtml(item.phone)}</small></td>
          <td>${escapeHtml(item.company || '-')}</td>
          <td><span class="badge-type">${escapeHtml(item.inquiry_type)}</span></td>
          <td>
            <select class="form-select form-select-sm status-select status-${item.status}" onchange="updateInquiryStatus(${item.id}, this.value)">
              <option value="PENDING" ${item.status === 'PENDING' ? 'selected' : ''}>대기중</option>
              <option value="IN_PROGRESS" ${item.status === 'IN_PROGRESS' ? 'selected' : ''}>처리중</option>
              <option value="COMPLETED" ${item.status === 'COMPLETED' ? 'selected' : ''}>완료</option>
            </select>
          </td>
          <td><small>${item.created_at}</small></td>
          <td>
            <button onclick="viewInquiryDetail(${item.id})" class="btn btn-secondary btn-sm">보기</button>
            <button onclick="deleteInquiry(${item.id})" class="btn btn-danger btn-sm">삭제</button>
          </td>
        </tr>
      `).join('');
    }
  } catch (err) {
    tbody.innerHTML = '<tr><td colspan="8" class="text-center text-danger">문의 데이터를 불러오지 못했습니다.</td></tr>';
  }
}

async function updateInquiryStatus(id, newStatus) {
  try {
    const res = await fetch(`/api/admin/inquiries/${id}/status`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status: newStatus })
    }).then(r => r.json());

    if (res.success) {
      loadAdminStats();
      loadAdminInquiries();
    } else {
      alert(res.detail || '상태 변경 실패');
    }
  } catch (err) {
    alert('오류가 발생했습니다.');
  }
}

function viewInquiryDetail(id) {
  const item = inquiriesCache.find(i => i.id === id);
  if (!item) return;

  document.getElementById('viewInquiryName').textContent = item.name;
  document.getElementById('viewInquiryEmail').textContent = item.email;
  document.getElementById('viewInquiryPhone').textContent = item.phone;
  document.getElementById('viewInquiryCompany').textContent = item.company || '없음';
  document.getElementById('viewInquiryType').textContent = item.inquiry_type;
  document.getElementById('viewInquiryDate').textContent = item.created_at;
  document.getElementById('viewInquiryMessage').textContent = item.message;

  openModal('modalViewInquiry');
}

async function deleteInquiry(id) {
  if (!confirm(`ID #${id} 문의 건을 삭제하시겠습니까?`)) return;

  try {
    const res = await fetch(`/api/admin/inquiries/${id}`, { method: 'DELETE' }).then(r => r.json());
    if (res.success) {
      alert('삭제되었습니다.');
      loadAdminStats();
      loadAdminInquiries();
    }
  } catch (err) {
    alert('삭제 처리 중 오류가 발생했습니다.');
  }
}

// -----------------------------------------------------------------------------
// ❓ 03. FAQ (Q&A) 관리
// -----------------------------------------------------------------------------
let faqsCache = [];

async function loadAdminFaqs() {
  const tbody = document.getElementById('faqsTableBody');
  tbody.innerHTML = '<tr><td colspan="7" class="text-center">조회 중...</td></tr>';

  try {
    const res = await fetch('/api/admin/faqs').then(r => r.json());
    if (res.success && res.data) {
      faqsCache = res.data;
      if (res.data.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="text-center text-muted">등록된 FAQ가 없습니다.</td></tr>';
        return;
      }

      tbody.innerHTML = res.data.map(item => `
        <tr>
          <td>#${item.id}</td>
          <td>${item.order_num}</td>
          <td><span class="badge-cat">${escapeHtml(item.category)}</span></td>
          <td><strong>${escapeHtml(item.question)}</strong></td>
          <td>${item.is_active ? '<span class="text-success">공개</span>' : '<span class="text-muted">비공개</span>'}</td>
          <td><small>${item.created_at}</small></td>
          <td>
            <button onclick="editFaqModal(${item.id})" class="btn btn-secondary btn-sm">수정</button>
            <button onclick="deleteFaq(${item.id})" class="btn btn-danger btn-sm">삭제</button>
          </td>
        </tr>
      `).join('');
    }
  } catch (err) {
    tbody.innerHTML = '<tr><td colspan="7" class="text-center text-danger">FAQ 데이터를 불러오지 못했습니다.</td></tr>';
  }
}

function editFaqModal(id) {
  const item = faqsCache.find(f => f.id === id);
  if (!item) return;

  document.getElementById('faqModalTitle').textContent = '❓ FAQ 수정';
  document.getElementById('faqFormId').value = item.id;
  document.getElementById('faqCategory').value = item.category;
  document.getElementById('faqQuestion').value = item.question;
  document.getElementById('faqAnswer').value = item.answer;
  document.getElementById('faqOrderNum').value = item.order_num;
  document.getElementById('faqIsActive').checked = item.is_active;

  openModal('modalAddFaq');
}

async function submitFaqForm() {
  const id = document.getElementById('faqFormId').value;
  const payload = {
    category: document.getElementById('faqCategory').value,
    question: document.getElementById('faqQuestion').value,
    answer: document.getElementById('faqAnswer').value,
    order_num: parseInt(document.getElementById('faqOrderNum').value) || 0,
    is_active: document.getElementById('faqIsActive').checked
  };

  const url = id ? `/api/admin/faqs/${id}` : '/api/admin/faqs';
  const method = id ? 'PUT' : 'POST';

  try {
    const res = await fetch(url, {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    }).then(r => r.json());

    if (res.success) {
      closeModal('modalAddFaq');
      loadAdminStats();
      loadAdminFaqs();
      resetFaqForm();
    } else {
      alert(res.detail || '저장 실패');
    }
  } catch (err) {
    alert('처리 중 오류가 발생했습니다.');
  }
}

function resetFaqForm() {
  document.getElementById('faqModalTitle').textContent = '❓ FAQ 작성';
  document.getElementById('faqFormId').value = '';
  document.getElementById('faqForm').reset();
}

async function deleteFaq(id) {
  if (!confirm('정말 이 FAQ 항목을 삭제하시겠습니까?')) return;

  try {
    const res = await fetch(`/api/admin/faqs/${id}`, { method: 'DELETE' }).then(r => r.json());
    if (res.success) {
      loadAdminStats();
      loadAdminFaqs();
    }
  } catch (err) {
    alert('삭제 중 오류가 발생했습니다.');
  }
}

// -----------------------------------------------------------------------------
// 🚀 04. 사전 예약 및 구독자
// -----------------------------------------------------------------------------
async function loadAdminPreRegs() {
  const filter = document.getElementById('preRegFilter').value;
  const tbody = document.getElementById('preRegsTableBody');
  tbody.innerHTML = '<tr><td colspan="6" class="text-center">조회 중...</td></tr>';

  try {
    const url = filter ? `/api/admin/pre-registrations?reg_type=${filter}` : '/api/admin/pre-registrations';
    const res = await fetch(url).then(r => r.json());

    if (res.success && res.data) {
      if (res.data.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" class="text-center text-muted">등록된 구독자 데이터가 없습니다.</td></tr>';
        return;
      }

      tbody.innerHTML = res.data.map(item => `
        <tr>
          <td>#${item.id}</td>
          <td><strong>${escapeHtml(item.email)}</strong></td>
          <td>${escapeHtml(item.phone || '-')}</td>
          <td><span class="badge-type">${item.reg_type === 'PRE_REGISTER' ? '🚀 사전예약' : '📧 뉴스레터'}</span></td>
          <td>${escapeHtml(item.interest || '-')}</td>
          <td><small>${item.created_at}</small></td>
        </tr>
      `).join('');
    }
  } catch (err) {
    tbody.innerHTML = '<tr><td colspan="6" class="text-center text-danger">목록을 불러오지 못했습니다.</td></tr>';
  }
}

// -----------------------------------------------------------------------------
// 📢 05. 공지사항 관리
// -----------------------------------------------------------------------------
let noticesCache = [];

async function loadAdminNotices() {
  const tbody = document.getElementById('noticesTableBody');
  tbody.innerHTML = '<tr><td colspan="7" class="text-center">조회 중...</td></tr>';

  try {
    const res = await fetch('/api/admin/notices').then(r => r.json());
    if (res.success && res.data) {
      noticesCache = res.data;
      if (res.data.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="text-center text-muted">등록된 공지사항이 없습니다.</td></tr>';
        return;
      }

      tbody.innerHTML = res.data.map(item => `
        <tr>
          <td>#${item.id}</td>
          <td><span class="badge-notice">${escapeHtml(item.badge_text)}</span></td>
          <td><strong>${escapeHtml(item.title)}</strong></td>
          <td>${item.is_pinned ? '📌 고정' : '-'}</td>
          <td>${item.is_active ? '<span class="text-success">게시중</span>' : '<span class="text-muted">숨김</span>'}</td>
          <td><small>${item.created_at}</small></td>
          <td>
            <button onclick="editNoticeModal(${item.id})" class="btn btn-secondary btn-sm">수정</button>
            <button onclick="deleteNotice(${item.id})" class="btn btn-danger btn-sm">삭제</button>
          </td>
        </tr>
      `).join('');
    }
  } catch (err) {
    tbody.innerHTML = '<tr><td colspan="7" class="text-center text-danger">공지사항 데이터를 불러오지 못했습니다.</td></tr>';
  }
}

function editNoticeModal(id) {
  const item = noticesCache.find(n => n.id === id);
  if (!item) return;

  document.getElementById('noticeModalTitle').textContent = '📢 공지사항 수정';
  document.getElementById('noticeFormId').value = item.id;
  document.getElementById('noticeTitle').value = item.title;
  document.getElementById('noticeBadge').value = item.badge_text;
  document.getElementById('noticeContent').value = item.content;
  document.getElementById('noticeIsPinned').checked = item.is_pinned;
  document.getElementById('noticeIsActive').checked = item.is_active;

  openModal('modalAddNotice');
}

async function submitNoticeForm() {
  const id = document.getElementById('noticeFormId').value;
  const payload = {
    title: document.getElementById('noticeTitle').value,
    badge_text: document.getElementById('noticeBadge').value || 'NOTICE',
    content: document.getElementById('noticeContent').value,
    is_pinned: document.getElementById('noticeIsPinned').checked,
    is_active: document.getElementById('noticeIsActive').checked
  };

  const url = id ? `/api/admin/notices/${id}` : '/api/admin/notices';
  const method = id ? 'PUT' : 'POST';

  try {
    const res = await fetch(url, {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    }).then(r => r.json());

    if (res.success) {
      closeModal('modalAddNotice');
      loadAdminStats();
      loadAdminNotices();
      resetNoticeForm();
    } else {
      alert(res.detail || '저장 실패');
    }
  } catch (err) {
    alert('처리 중 오류가 발생했습니다.');
  }
}

function resetNoticeForm() {
  document.getElementById('noticeModalTitle').textContent = '📢 공지사항 작성';
  document.getElementById('noticeFormId').value = '';
  document.getElementById('noticeForm').reset();
}

async function deleteNotice(id) {
  if (!confirm('이 공지사항을 삭제하시겠습니까?')) return;

  try {
    const res = await fetch(`/api/admin/notices/${id}`, { method: 'DELETE' }).then(r => r.json());
    if (res.success) {
      loadAdminStats();
      loadAdminNotices();
    }
  } catch (err) {
    alert('삭제 중 오류가 발생했습니다.');
  }
}

// -----------------------------------------------------------------------------
// ⚙️ 06. 동적 랜딩 콘텐츠
// -----------------------------------------------------------------------------
async function loadAdminContents() {
  try {
    const res = await fetch('/api/admin/contents').then(r => r.json());
    if (res.success && res.data) {
      if (res.data.hero_title) document.getElementById('content_hero_title').value = res.data.hero_title;
      if (res.data.hero_subtitle) document.getElementById('content_hero_subtitle').value = res.data.hero_subtitle;
      if (res.data.stat_detection_rate) document.getElementById('content_stat_detection_rate').value = res.data.stat_detection_rate;
      if (res.data.stat_response_time) document.getElementById('content_stat_response_time').value = res.data.stat_response_time;
      if (res.data.stat_daily_attacks) document.getElementById('content_stat_daily_attacks').value = res.data.stat_daily_attacks;
    }
  } catch (err) {
    console.error('Failed to load landing contents', err);
  }
}

async function saveLandingContents() {
  const contents = {
    hero_title: document.getElementById('content_hero_title').value,
    hero_subtitle: document.getElementById('content_hero_subtitle').value,
    stat_detection_rate: document.getElementById('content_stat_detection_rate').value,
    stat_response_time: document.getElementById('content_stat_response_time').value,
    stat_daily_attacks: document.getElementById('content_stat_daily_attacks').value
  };

  try {
    const res = await fetch('/api/admin/contents', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ contents })
    }).then(r => r.json());

    if (res.success) {
      alert('동적 콘텐츠 설정이 업데이트되었습니다!');
    } else {
      alert(res.detail || '저장 오류');
    }
  } catch (err) {
    alert('콘텐츠 저장 중 오류가 발생했습니다.');
  }
}

// -----------------------------------------------------------------------------
// 🛠️ 헬퍼 유틸리티
// -----------------------------------------------------------------------------
function openModal(id) {
  document.getElementById(id).style.display = 'flex';
}

function closeModal(id) {
  document.getElementById(id).style.display = 'none';
  if (id === 'modalAddFaq') resetFaqForm();
  if (id === 'modalAddNotice') resetNoticeForm();
}

function escapeHtml(str) {
  if (!str) return '';
  return str.replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
}
