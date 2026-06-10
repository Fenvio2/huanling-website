// =============================================
// 幻灵 (HuanLing) - Corporate Website JS
// =============================================

document.addEventListener('DOMContentLoaded', () => {

  // --- Mobile Menu Toggle ---
  const menuToggle = document.querySelector('.menu-toggle');
  const navLinks = document.querySelector('.nav-links');

  if (menuToggle) {
    menuToggle.addEventListener('click', () => {
      menuToggle.classList.toggle('active');
      navLinks.classList.toggle('open');
    });

    // Close menu on link click
    document.querySelectorAll('.nav-links a').forEach(link => {
      link.addEventListener('click', () => {
        menuToggle.classList.remove('active');
        navLinks.classList.remove('open');
      });
    });
  }

  // --- Header Scroll Effect ---
  const header = document.querySelector('.header');
  let lastScroll = 0;

  window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;
    if (currentScroll > 50) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }
    lastScroll = currentScroll;
  });

  // --- Active Nav Link Highlighting ---
  const currentPath = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-links a').forEach(link => {
    const href = link.getAttribute('href');
    if (href === currentPath) {
      link.classList.add('active');
    }
  });

  // --- Fade-in Animation on Scroll (Intersection Observer) ---
  const fadeElements = document.querySelectorAll('.fade-in');

  if (fadeElements.length > 0) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    }, {
      threshold: 0.1,
      rootMargin: '0px 0px -50px 0px'
    });

    fadeElements.forEach(el => observer.observe(el));
  }

  // --- Stats Counter Animation ---
  const statNumbers = document.querySelectorAll('.stat-number');

  if (statNumbers.length > 0) {
    const counterObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const target = entry.target;
          const text = target.textContent;
          const numMatch = text.match(/[\d.]+/);
          if (numMatch) {
            const targetNum = parseFloat(numMatch[0]);
            const isDecimal = numMatch[0].includes('.');
            const duration = 2000;
            const startTime = performance.now();

            function animateCounter(currentTime) {
              const elapsed = currentTime - startTime;
              const progress = Math.min(elapsed / duration, 1);
              // ease-out cubic
              const eased = 1 - Math.pow(1 - progress, 3);
              const currentVal = eased * targetNum;

              if (isDecimal) {
                target.textContent = currentVal.toFixed(1) + (text.includes('+') ? '+' : '');
              } else {
                target.textContent = Math.floor(currentVal) + (text.includes('+') ? '+' : '');
              }

              if (progress < 1) {
                requestAnimationFrame(animateCounter);
              } else {
                target.textContent = text; // restore exact original text
              }
            }

            requestAnimationFrame(animateCounter);
          }
          counterObserver.unobserve(target);
        }
      });
    }, { threshold: 0.5 });

    statNumbers.forEach(el => counterObserver.observe(el));
  }

  // --- Contact Form Handler ---
  const contactForm = document.getElementById('contactForm');
  if (contactForm) {
    contactForm.addEventListener('submit', (e) => {
      e.preventDefault();

      const form = e.target;
      const name = form.querySelector('#name').value.trim();
      const email = form.querySelector('#email').value.trim();
      const subject = form.querySelector('#subject').value;
      const message = form.querySelector('#message').value.trim();

      if (!name || !email || !subject || !message) {
        alert('请填写所有必填字段');
        return;
      }

      const subjectLabels = {
        'create': '成为智能体创作者',
        'enterprise': '企业合作咨询',
        'technical': '技术支持',
        'feedback': '建议反馈',
        'other': '其他'
      };

      const mailSubject = `[幻灵咨询] ${subjectLabels[subject] || subject} - 来自 ${name}`;
      const mailBody = `姓名：${name}%0D%0A邮箱：${email}%0D%0A咨询类型：${subjectLabels[subject] || subject}%0D%0A%0D%0A留言内容：%0D%0A${message}`;

      const submitBtn = contactForm.querySelector('button[type="submit"]');
      const originalText = submitBtn.textContent;
      submitBtn.textContent = '正在打开邮件客户端...';
      submitBtn.disabled = true;

      // Open user's email client via mailto
      window.location.href = `mailto:2151586613@qq.com?subject=${encodeURIComponent(mailSubject)}&body=${mailBody}`;

      // Show success feedback
      setTimeout(() => {
        submitBtn.textContent = '已打开邮件客户端 ✓';
        submitBtn.style.background = 'linear-gradient(135deg, #10B981, #047857)';

        setTimeout(() => {
          submitBtn.textContent = originalText;
          submitBtn.style.background = '';
          submitBtn.disabled = false;
          form.reset();
        }, 3000);
      }, 800);
    });
  }

  // --- Floating Orbs Parallax Effect (Hero) ---
  const orbs = document.querySelectorAll('.floating-orb');
  if (orbs.length > 0) {
    document.querySelector('.hero')?.addEventListener('mousemove', (e) => {
      const x = (e.clientX / window.innerWidth - 0.5) * 20;
      const y = (e.clientY / window.innerHeight - 0.5) * 20;
      orbs.forEach((orb, i) => {
        const factor = (i + 1) * 0.3;
        orb.style.transform = `translate(${x * factor}px, ${y * factor}px)`;
      });
    });
  }

  console.log('🐦 幻灵官网已加载 — 用AI重塑智能体经济');
});
