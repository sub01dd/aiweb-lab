(() => {
  'use strict';

  const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;

  // -------- Header elevation on scroll --------
  const header = document.querySelector('.site-header');
  const onScroll = () => {
    if (!header) return;
    header.dataset.elevated = window.scrollY > 16 ? 'true' : 'false';
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // -------- Mobile nav (burger) --------
  const burger = document.querySelector('.burger');
  const nav = document.getElementById('site-nav');
  if (burger && nav) {
    const headerEl = document.querySelector('.site-header');
    const toggle = (force) => {
      const open = force ?? burger.getAttribute('aria-expanded') !== 'true';
      burger.setAttribute('aria-expanded', String(open));
      nav.dataset.open = String(open);
      burger.setAttribute('aria-label', open ? 'メニューを閉じる' : 'メニューを開く');
      const html = document.documentElement;
      if (open) {
        const sbw = window.innerWidth - html.clientWidth;
        document.body.style.overflow = 'hidden';
        html.style.overflow = 'hidden';
        document.body.style.paddingRight = sbw + 'px';
        if (headerEl) headerEl.style.paddingRight = sbw + 'px';
      } else {
        document.body.style.overflow = '';
        html.style.overflow = '';
        document.body.style.paddingRight = '';
        if (headerEl) headerEl.style.paddingRight = '';
      }
    };
    burger.addEventListener('click', () => toggle());
    nav.querySelectorAll('a').forEach(a => a.addEventListener('click', () => toggle(false)));
    matchMedia('(min-width: 901px)').addEventListener('change', e => {
      if (e.matches) toggle(false);
    });
    // Esc to close
    document.addEventListener('keydown', e => {
      if (e.key === 'Escape' && burger.getAttribute('aria-expanded') === 'true') toggle(false);
    });
    // Click outside to close
    document.addEventListener('click', e => {
      if (burger.getAttribute('aria-expanded') !== 'true') return;
      if (nav.contains(e.target) || burger.contains(e.target)) return;
      toggle(false);
    });
  }

  // -------- Sticky CTA (mobile) — IntersectionObserver based --------
  const sticky = document.querySelector('.sticky-cta');
  const heroEl = document.querySelector('.hero');
  const contactEl = document.getElementById('contact');
  if (sticky && heroEl && 'IntersectionObserver' in window) {
    const state = { heroVisible: true, contactVisible: false };
    const apply = () => sticky.classList.toggle('show', !state.heroVisible && !state.contactVisible);
    new IntersectionObserver(([e]) => { state.heroVisible = e.isIntersecting; apply(); },
      { rootMargin: '-80px 0px 0px 0px' }).observe(heroEl);
    if (contactEl) {
      new IntersectionObserver(([e]) => { state.contactVisible = e.isIntersecting; apply(); },
        { rootMargin: '0px 0px -20% 0px' }).observe(contactEl);
    }
  }

  // -------- Reveal on scroll --------
  const reveals = document.querySelectorAll('.reveal');
  if (reveals.length && !reduceMotion && 'IntersectionObserver' in window) {
    const io = new IntersectionObserver((entries, obs) => {
      entries.forEach(e => {
        if (e.isIntersecting) {
          e.target.classList.add('in');
          obs.unobserve(e.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    reveals.forEach(el => io.observe(el));
  } else {
    reveals.forEach(el => el.classList.add('in'));
  }

  // -------- Magnetic button (hero CTA) --------
  if (!reduceMotion && matchMedia('(hover: hover) and (pointer: fine)').matches) {
    document.querySelectorAll('.magnet').forEach(btn => {
      btn.style.transition = 'transform .25s cubic-bezier(.2,.7,.2,1)';
      btn.addEventListener('pointermove', e => {
        const r = btn.getBoundingClientRect();
        const x = (e.clientX - r.left - r.width / 2) * 0.25;
        const y = (e.clientY - r.top - r.height / 2) * 0.25;
        btn.style.transform = `translate(${x}px, ${y}px)`;
      });
      btn.addEventListener('pointerleave', () => {
        btn.style.transform = '';
      });
    });
  }

  // -------- GA4 helper --------
  const trackGA = (name, params = {}) => {
    if (typeof gtag === 'function') gtag('event', name, params);
  };

  // -------- Form submit: mailto fallback + GA (single listener, no double-fire) --------
  document.querySelectorAll('form.contact-form').forEach(f => {
    f.addEventListener('submit', (e) => {
      const action = f.getAttribute('action') || '';
      if (action.includes('REPLACE_WITH_YOUR_FORM_ID')) {
        e.preventDefault();
        const get = n => f.querySelector(`[name="${n}"]`)?.value || '';
        const subject = encodeURIComponent('【aiweb】無料相談のご相談');
        const body = encodeURIComponent(
          `お名前: ${get('name')}\nメール: ${get('email')}\n業種: ${get('industry')}\nプラン: ${get('plan')}\n\n${get('message')}`
        );
        const ok = window.confirm('フォーム送信は準備中です。メールクライアントを開いて送信しますか？\n（OKでメール作成画面が開きます）');
        if (ok) {
          trackGA('generate_lead', { form_id: 'contact_mailto', value: 1 });
          location.href = `mailto:tai028780@gmail.com?subject=${subject}&body=${body}`;
        }
        return;
      }
      trackGA('generate_lead', { form_id: 'contact', value: 1 });
    });
  });

  // -------- Primary CTA clicks (exclude form submit to avoid double counting) --------
  document.querySelectorAll('.btn-primary:not(.submit), .plan-cta, .nav-cta').forEach(a => {
    a.addEventListener('click', () => {
      trackGA('cta_click', {
        cta_text: (a.textContent || '').trim().slice(0, 40),
        location: a.closest('section')?.id || 'header'
      });
    });
  });

  // -------- FAQ: only one open at a time --------
  document.querySelectorAll('.faq-item').forEach(d => {
    d.addEventListener('toggle', () => {
      if (d.open) {
        document.querySelectorAll('.faq-item[open]').forEach(o => {
          if (o !== d) o.open = false;
        });
      }
    });
  });
})();
