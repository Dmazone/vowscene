(() => {
  const supported = ['en', 'ko', 'zh', 'ja', 'es', 'fr'];
  const key = 'vowscene-language-v1';
  const rows = window.VS_TRANSLATION_ROWS || [];
  const dictionaries = Object.fromEntries(supported.slice(1).map(lang => [lang, new Map()]));
  for (const row of rows) {
    if (row.length !== supported.length) continue;
    supported.slice(1).forEach((lang, i) => dictionaries[lang].set(row[0], row[i + 1]));
  }
  const originalText = new WeakMap();
  const originalAttributes = new WeakMap();
  const originalLinks = new WeakMap();
  const langFromUrl = new URL(location.href).searchParams.get('lang');
  let saved = 'en';
  try { saved = localStorage.getItem(key) || 'en'; } catch {}
  let current = supported.includes(langFromUrl) ? langFromUrl : supported.includes(saved) ? saved : 'en';
  const t = (source) => dictionaries[current]?.get(source) || source;
  window.siteT = t;
  window.siteLanguage = () => current;

  function translateText() {
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    let node;
    while ((node = walker.nextNode())) {
      if (['SCRIPT', 'STYLE', 'NOSCRIPT', 'SVG'].includes(node.parentElement?.tagName)) continue;
      if (!originalText.has(node)) originalText.set(node, node.nodeValue);
      const source = originalText.get(node);
      const phrase = source.trim();
      if (phrase && (current === 'en' || dictionaries[current].has(phrase))) {
        node.nodeValue = source.replace(phrase, t(phrase));
      }
    }
    for (const element of document.querySelectorAll('[placeholder],[alt],[aria-label],[title]')) {
      if (!originalAttributes.has(element)) {
        originalAttributes.set(element, Object.fromEntries(['placeholder', 'alt', 'aria-label', 'title'].filter(a => element.hasAttribute(a)).map(a => [a, element.getAttribute(a)])));
      }
      for (const [attribute, source] of Object.entries(originalAttributes.get(element))) element.setAttribute(attribute, t(source));
    }
    document.title = t(document.titleSource || (document.titleSource = document.title));
  }

  function updateLinks() {
    for (const anchor of document.querySelectorAll('a[href]')) {
      if (!originalLinks.has(anchor)) originalLinks.set(anchor, anchor.getAttribute('href'));
      const source = originalLinks.get(anchor);
      if (!source || /^(#|https?:|mailto:|tel:)/i.test(source) || /\.(pdf|png|jpe?g)([?#]|$)/i.test(source)) continue;
      const url = new URL(source, location.href);
      if (url.origin !== location.origin) continue;
      if (current === 'en') url.searchParams.delete('lang');
      else url.searchParams.set('lang', current);
      anchor.href = url.href;
    }
  }

  function setLanguage(lang, userChoice = false) {
    if (!supported.includes(lang)) return;
    current = lang;
    document.documentElement.lang = lang === 'zh' ? 'zh-Hans' : lang;
    document.querySelectorAll('.site-language').forEach(select => { select.value = lang; });
    translateText();
    updateLinks();
    if (userChoice) {
      try { localStorage.setItem(key, lang); } catch {}
      const url = new URL(location.href);
      if (lang === 'en') url.searchParams.delete('lang'); else url.searchParams.set('lang', lang);
      history.replaceState(null, '', url);
      document.dispatchEvent(new CustomEvent('site-language-change', { detail: { lang } }));
    }
  }
  window.setSiteLanguage = setLanguage;
  document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.site-language').forEach(select => select.addEventListener('change', event => setLanguage(event.target.value, true)));
    setLanguage(current);
  });
})();
