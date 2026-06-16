/* Nebula Geo Technologies — Main JS */

// Navbar scroll effect
const navbar = document.querySelector('.navbar');
window.addEventListener('scroll', () => {
  navbar && navbar.classList.toggle('scrolled', window.scrollY > 50);
});

// Active nav link
document.querySelectorAll('.navbar-nav .nav-link').forEach(link => {
  if (link.href === window.location.href) link.classList.add('active');
});

// Reveal on scroll
const revealEls = document.querySelectorAll('.reveal');
const revealObs = new IntersectionObserver((entries) => {
  entries.forEach((e, i) => {
    if (e.isIntersecting) {
      setTimeout(() => e.target.classList.add('visible'), i * 80);
      revealObs.unobserve(e.target);
    }
  });
}, { threshold: 0.1 });
revealEls.forEach(el => revealObs.observe(el));

// Counter animation
function animateCounter(el, target, suffix = '') {
  let current = 0;
  const step = target / 60;
  const timer = setInterval(() => {
    current += step;
    if (current >= target) { current = target; clearInterval(timer); }
    el.textContent = Math.floor(current) + suffix;
  }, 25);
}

const counterObs = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      const el = e.target;
      const target = parseInt(el.dataset.target);
      const suffix = el.dataset.suffix || '';
      animateCounter(el, target, suffix);
      counterObs.unobserve(el);
    }
  });
}, { threshold: 0.5 });
document.querySelectorAll('.counter').forEach(el => counterObs.observe(el));

// Contact form AJAX
const contactForm = document.getElementById('contactForm');
if (contactForm) {
  contactForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const btn = contactForm.querySelector('button[type="submit"]');
    const msgDiv = document.getElementById('formMsg');
    btn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Sending...';
    btn.disabled = true;
    try {
      const fd = new FormData(contactForm);
      const res = await fetch(contactForm.action || window.location.href, {
        method: 'POST',
        body: fd,
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
      });
      const data = await res.json();
      if (data.success) {
        msgDiv.innerHTML = `<div class="alert-nebula"><i class="fas fa-check-circle"></i>${data.message}</div>`;
        contactForm.reset();
      } else {
        msgDiv.innerHTML = `<div class="alert-nebula alert-nebula-err"><i class="fas fa-exclamation-circle"></i>${data.message}</div>`;
      }
    } catch {
      msgDiv.innerHTML = `<div class="alert-nebula alert-nebula-err"><i class="fas fa-exclamation-circle"></i>Something went wrong. Please try again.</div>`;
    }
    btn.innerHTML = '<i class="fas fa-paper-plane me-2"></i>Send Message';
    btn.disabled = false;
    setTimeout(() => { msgDiv.innerHTML = ''; }, 6000);
  });
}

// Portfolio filter
document.querySelectorAll('.filter-btn[data-cat]').forEach(btn => {
  btn.addEventListener('click', function(e) {
    e.preventDefault();
    const cat = this.dataset.cat;
    document.querySelectorAll('.filter-btn[data-cat]').forEach(b => b.classList.remove('active'));
    this.classList.add('active');
    document.querySelectorAll('.port-item').forEach(item => {
      const show = cat === 'all' || item.dataset.cat === cat;
      item.style.display = show ? '' : 'none';
    });
  });
});

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener('click', e => {
    const target = document.querySelector(a.getAttribute('href'));
    if (target) {
      e.preventDefault();
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });
});

// Typing effect for hero
const typingEl = document.getElementById('typingText');
if (typingEl) {
  const words = ['Solutions', 'Innovation', 'Excellence', 'Growth'];
  let wi = 0, ci = 0, del = false;
  setInterval(() => {
    const w = words[wi];
    if (!del) {
      typingEl.textContent = w.slice(0, ++ci);
      if (ci === w.length) { del = true; setTimeout(() => {}, 1500); }
    } else {
      typingEl.textContent = w.slice(0, --ci);
      if (ci === 0) { del = false; wi = (wi + 1) % words.length; }
    }
  }, 120);
}
