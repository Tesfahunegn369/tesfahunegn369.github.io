(() => {
  const toggle = document.getElementById('menu-toggle');
  const nav = document.getElementById('primary-nav');
  const year = document.getElementById('current-year');
  const languageSelect = document.getElementById('language-select');

  if (year) year.textContent = new Date().getFullYear();

  toggle?.addEventListener('click', () => {
    const isOpen = nav.classList.toggle('open');
    toggle.setAttribute('aria-expanded', String(isOpen));
    toggle.setAttribute('aria-label', isOpen ? 'Close navigation' : 'Open navigation');
    toggle.textContent = isOpen ? '✕' : '☰';
  });

  nav?.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
      nav.classList.remove('open');
      toggle?.setAttribute('aria-expanded', 'false');
      if (toggle) {
        toggle.textContent = '☰';
        toggle.setAttribute('aria-label', 'Open navigation');
      }
    });
  });

  const sections = [...document.querySelectorAll('main section[id]')];
  const navLinks = [...document.querySelectorAll('.primary-nav a')];
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          navLinks.forEach(link => {
            const active = link.getAttribute('href') === `#${entry.target.id}`;
            link.classList.toggle('active', active);
            if (active) link.setAttribute('aria-current', 'location');
            else link.removeAttribute('aria-current');
          });
        }
      });
    }, { rootMargin: '-25% 0px -65% 0px', threshold: 0 });
    sections.forEach(section => observer.observe(section));
  }

  // Language selector: connect the visible selector to Google's actual widget.
  // English is the default. Amharic and Korean follow, then all other languages alphabetically.
  if (languageSelect) {
    const options = [...languageSelect.options];
    const pinned = ['en', 'am', 'ko'];
    const byName = (a, b) => a.textContent.localeCompare(b.textContent);
    const first = pinned.map(code => options.find(option => option.value === code)).filter(Boolean);
    const rest = options.filter(option => !pinned.includes(option.value)).sort(byName);
    languageSelect.replaceChildren(...first, ...rest);

    let savedLanguage = 'en';
    try {
      savedLanguage = localStorage.getItem('academic-site-language') || 'en';
      // Migrate the previous mistaken Zulu default to English for returning visitors.
      if (savedLanguage === 'zu' || !options.some(option => option.value === savedLanguage)) savedLanguage = 'en';
      localStorage.setItem('academic-site-language', savedLanguage);
    } catch (_) {
      savedLanguage = 'en';
    }
    languageSelect.value = savedLanguage;

    function writeTranslateCookie(code) {
      // The cookie is a fallback for Google Translate and also survives page reloads.
      if (code === 'en') {
        document.cookie = 'googtrans=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/; SameSite=Lax';
      } else {
        document.cookie = `googtrans=/en/${code}; path=/; SameSite=Lax`;
      }
    }

    function fireGoogleChange(combo, code) {
      // Some widget versions omit the source language (English) from their option list.
      combo.value = (code === 'en' && ![...combo.options].some(option => option.value === 'en')) ? '' : code;
      combo.dispatchEvent(new Event('change', { bubbles: true }));
      // Google Translate's widget needs a second event in some versions to restore source language.
      if (code === 'en') {
        window.setTimeout(() => combo.dispatchEvent(new Event('change', { bubbles: true })), 150);
      }
    }

    function applyLanguage(code, attempt = 0) {
      const combo = document.querySelector('#google_translate_element select.goog-te-combo')
        || document.querySelector('select.goog-te-combo');
      const hasTarget = combo && (code === 'en' || [...combo.options].some(option => option.value === code));
      if (hasTarget) {
        fireGoogleChange(combo, code);
        return true;
      }
      // The Google widget loads asynchronously. Retry for up to about 12 seconds.
      if (attempt < 40) {
        window.setTimeout(() => applyLanguage(code, attempt + 1), 300);
      }
      return false;
    }

    window.applySavedGoogleLanguage = () => {
      const code = languageSelect.value || savedLanguage || 'en';
      writeTranslateCookie(code);
      applyLanguage(code);
    };

    // Set the initial preference before Google's external script initializes.
    writeTranslateCookie(savedLanguage);
    languageSelect.addEventListener('change', () => {
      const code = languageSelect.value || 'en';
      savedLanguage = code;
      try { localStorage.setItem('academic-site-language', code); } catch (_) {}
      writeTranslateCookie(code);
      applyLanguage(code);
    });
  }
})();
