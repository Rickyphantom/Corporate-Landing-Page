/**
 * SecOps 기업 랜딩 페이지 메인 스크립트
 * - 화면 중앙 기준 거리 기반 텍스트/섹션 부드러운 투명도(Opacity) 제어
 * - 스크롤에 따른 사이드바 Active 메뉴 하이라이트 동기화
 */

document.addEventListener('DOMContentLoaded', () => {
  const sections = document.querySelectorAll('.content-section');
  const navLinks = document.querySelectorAll('.sidebar-nav .nav-item');

  function updateScrollEffects() {
    const windowHeight = window.innerHeight;
    const windowCenter = windowHeight / 2;

    let closestSection = null;
    let minDistance = Infinity;

    sections.forEach((sec) => {
      const rect = sec.getBoundingClientRect();
      const secCenter = rect.top + rect.height / 2;

      const distance = Math.abs(windowCenter - secCenter);

      // ✨ 여백이 늘어난 만큼 감지 거리(maxDistance)도 화면 높이의 60% 폭으로 확장
      const maxDistance = windowHeight * 0.6;
      let opacity = 1 - distance / maxDistance;

      if (opacity < 0.1) opacity = 0.1; // 완전히 사라지지 않고 은은하게 유지
      if (opacity > 1) opacity = 1;

      sec.style.opacity = opacity;

      // 화면 중앙에 가장 가까운 섹션 추적
      if (distance < minDistance) {
        minDistance = distance;
        closestSection = sec;
      }
    });

    // 사이드바 활성 네비게이션 메뉴 갱신
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

  // 스크롤 및 창 크기 변경 시 이벤트 리스너 등록
  window.addEventListener('scroll', updateScrollEffects, { passive: true });
  window.addEventListener('resize', updateScrollEffects, { passive: true });

  // 초기 로드 시 1회 즉시 실행
  updateScrollEffects();
});
