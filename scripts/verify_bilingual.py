"""Validate the multilingual site: EN 90 / ZH 89 / ES 19 / PT 19 files; for the 19
phase-1 pages, EN/ZH/ES/PT symmetry (lang, canonical, hreflang group incl.
x-default, header/footer switchers), exactly one h1, no broken relative
links, no untranslated English residue and no Chinese leakage in the ES and PT
pages, valid JSON-LD, and a sitemap that lists exactly the published pages
(EN 65 + ZH 65 + ES 19 + PT 19 = 168).

Phase-1 new languages (it/ru/fr/ar/id, 19 pages each) and phase-2 product
pages (es/pt/it/ru/fr/ar/id, 69 RP-* pages each) are asserted in section 1b.
The assertions are written before those pages exist: a language whose edition
is missing — or present but incomplete (generation in progress) — is reported
SKIP (pending), not FAIL; once an edition is complete the count and the exact
file list are asserted, and the sitemap total grows with it
(168 + 19 per completed phase-1-new language + 69 per completed phase-2
language).

Run: python3 scripts/verify_bilingual.py   (from the repo root)
"""
from pathlib import Path
from urllib.parse import urlsplit, unquote
from bs4 import BeautifulSoup as BS
import json, re, sys, xml.etree.ElementTree as ET

ROOT = Path('.').resolve()
BASE = 'https://ropureoem.com/'
PHASE1 = [
    'index.html', 'products.html', 'videos.html', 'about.html', 'certification.html',
    'contact.html', 'get-quote.html', 'oem-odm.html',
    'products/under-sink.html', 'products/countertop.html', 'products/shower.html',
    'products/faucet.html', 'products/softener.html',
    'insights/index.html', 'insights/water-purifier-oem-moq.html',
    'insights/water-purifier-certification-europe.html',
    'insights/choose-flow-by-water-quality.html',
    'insights/under-sink-installation-space.html',
    'insights/voltage-plug-by-country.html',
]
# Text that is legitimately identical in English and Spanish/Portuguese (brands, codes,
# abbreviations, units, numbers, contact data). 'Menu' is the standard word in
# Brazilian Portuguese, identical in form to the English.
IDENTICAL_OK = re.compile(
    r'^(?:ROPureOEM|WhatsApp.*|info@ropureoem\.com|SKU:.*|RP-.*|OEM / ODM|OEM vs ODM|'
    r'EN|ZH|ES|FOB Shenzhen|MOQ.*|CE.*|UKCA.*|RoHS|REACH|CB.*|NSF.*|ACS|Menu|'
    r'Videos|.*\d.*|\+86.*|[\W_]*)$')

def url_for(lang, rel):
    prefix = '' if lang == 'en' else lang + '/'
    if rel == 'index.html':
        return BASE + prefix
    if rel.endswith('/index.html'):
        return BASE + prefix + rel[:-len('index.html')]
    return BASE + prefix + rel

def page_path(lang, rel):
    return (ROOT / rel) if lang == 'en' else (ROOT / lang / rel)

def resolve(page, href):
    return (ROOT / page.parent / unquote(urlsplit(href).path)).resolve()

def text_nodes(doc):
    from bs4 import Doctype
    out = []
    for node in doc.find_all(string=True):
        if isinstance(node, Doctype) or node.parent.name in ('script', 'style'):
            continue
        if node.find_parent(class_='language-switch'):
            continue
        if not node.strip():
            continue
        out.append(str(node).strip())
    return out

errors = []
def check(cond, msg):
    if not cond:
        errors.append(msg)

# --- 1. file counts (EN 90 incl. 404, ZH 89 incl. 404, ES 19, PT 19) ---
en_files = sorted(p.relative_to(ROOT).as_posix() for p in
                  [*ROOT.glob('*.html'), *ROOT.glob('products/*.html'), *ROOT.glob('insights/*.html')])
zh_files = sorted(p.relative_to(ROOT / 'zh').as_posix() for p in (ROOT / 'zh').rglob('*.html'))
es_files = sorted(p.relative_to(ROOT / 'es').as_posix() for p in (ROOT / 'es').rglob('*.html'))
pt_files = sorted(p.relative_to(ROOT / 'pt').as_posix() for p in (ROOT / 'pt').rglob('*.html'))
check(len(en_files) == 90, f'EN files {len(en_files)} != 90')
check(len(zh_files) == 89, f'ZH files {len(zh_files)} != 89')
check(len(es_files) == 19 and es_files == sorted(PHASE1), f'ES files {len(es_files)} != 19 phase-1')
check(len(pt_files) == 19 and pt_files == sorted(PHASE1), f'PT files {len(pt_files)} != 19 phase-1')
check(not (ROOT / 'es' / 'insights' / 'countertop-vs-under-sink-ro.html').exists(),
      'countertop article must not have an ES edition yet')
check(not (ROOT / 'pt' / 'insights' / 'countertop-vs-under-sink-ro.html').exists(),
      'countertop article must not have a PT edition yet')

# --- 1b. phase-1 new languages (it/ru/fr/ar/id x 19) + phase-2 product pages
# (es/pt/it/ru/fr/ar/id x 69 RP-* pages). See docstring: missing or
# incomplete editions SKIP as pending; completed editions are asserted exactly.
PHASE1_NEW_LANGS = ['it', 'ru', 'fr', 'ar', 'id']
PHASE2_LANGS = ['es', 'pt', 'it', 'ru', 'fr', 'ar', 'id']
PHASE2 = sorted(p.name for p in (ROOT / 'products').glob('RP-*.html'))
check(len(PHASE2) == 69, f'phase-2 product pages {len(PHASE2)} != 69')
skipped = []
complete_p1_new, complete_p2 = [], []
for lang in PHASE1_NEW_LANGS:
    d = ROOT / lang
    if not d.exists():
        skipped.append(f'{lang}/ phase-1 (19 pages): not generated yet')
        continue
    files = sorted(p.relative_to(d).as_posix() for p in d.rglob('*.html'))
    if len(files) < len(PHASE1):
        skipped.append(f'{lang}/ phase-1: in progress ({len(files)}/19 pages)')
        continue
    check(files == sorted(PHASE1), f'{lang.upper()} files {len(files)} != 19 phase-1')
    check(not (d / 'insights' / 'countertop-vs-under-sink-ro.html').exists(),
          f'countertop article must not have a {lang.upper()} edition yet')
    complete_p1_new.append(lang)
for lang in PHASE2_LANGS:
    d = ROOT / lang / 'products'
    if not d.exists():
        skipped.append(f'{lang}/products/ phase-2 (69 pages): not generated yet')
        continue
    files = sorted(p.name for p in d.glob('RP-*.html'))
    if len(files) < len(PHASE2):
        skipped.append(f'{lang}/products/ phase-2: in progress ({len(files)}/69 pages)')
        continue
    check(files == PHASE2, f'{lang.upper()} product files {len(files)} != 69 phase-2')
    complete_p2.append(lang)

# --- 2. per-page checks for the 19 ---
for rel in PHASE1:
    en = BS(page_path('en', rel).read_text(), 'html.parser')
    zh = BS(page_path('zh', rel).read_text(), 'html.parser')
    es = BS(page_path('es', rel).read_text(), 'html.parser')
    pt = BS(page_path('pt', rel).read_text(), 'html.parser')
    expected_hreflang = {'x-default': url_for('en', rel), 'en': url_for('en', rel),
                         'zh': url_for('zh', rel), 'es': url_for('es', rel),
                         'pt': url_for('pt', rel)}
    for lang, doc in [('en', en), ('zh', zh), ('es', es), ('pt', pt)]:
        check(doc.html['lang'] == lang, f'{lang}/{rel}: lang={doc.html.get("lang")}')
        check(len(doc.select('h1')) == 1, f'{lang}/{rel}: {len(doc.select("h1"))} h1')
        check(doc.select_one('link[rel=canonical]')['href'] == url_for(lang, rel),
              f'{lang}/{rel}: canonical mismatch')
        check({n['hreflang']: n['href'] for n in doc.select('link[hreflang]')} == expected_hreflang,
              f'{lang}/{rel}: hreflang group not symmetric')
        for area in ['header', 'footer']:
            links = doc.select(area + ' .language-switch a')
            check([a.get_text(strip=True) for a in links] == ['EN', 'ZH', 'ES', 'PT'],
                  f'{lang}/{rel} {area}: switcher labels {[a.get_text(strip=True) for a in links]}')
            targets = [resolve(page_path(lang, rel), a['href']) for a in links]
            expect = [page_path(l, rel).resolve() for l in ['en', 'zh', 'es', 'pt']]
            check(targets == expect, f'{lang}/{rel} {area}: switcher hrefs {targets} != {expect}')
            cur = [a for a in links if a.get('aria-current') == 'true']
            check(len(cur) == 1 and cur[0].get('data-language') == lang,
                  f'{lang}/{rel} {area}: aria-current wrong')
        check(doc.select_one('.language-switch')['aria-label'] ==
              {'en': 'Language selection', 'zh': '语言切换', 'es': 'Selección de idioma',
               'pt': 'Selecionar idioma'}[lang],
              f'{lang}/{rel}: switcher aria-label wrong')
        for node in doc.select('script[type="application/ld+json"]'):
            try:
                json.loads(node.string)
            except Exception as e:
                check(False, f'{lang}/{rel}: bad JSON-LD: {e}')
        # every relative link resolves to a real file; fragments exist
        for node in doc.select('[href],[src],[action]'):
            for attr in ['href', 'src', 'action']:
                val = node.get(attr, '')
                u = urlsplit(val)
                if not val or u.scheme or u.netloc:
                    continue
                target = resolve(page_path(lang, rel), val) if u.path else page_path(lang, rel)
                check(target.exists(), f'{lang}/{rel}: broken {attr}={val}')
                if u.fragment and target.suffix == '.html':
                    check(BS(target.read_text(), 'html.parser').find(id=unquote(u.fragment)),
                          f'{lang}/{rel}: missing fragment {val}')
        # numbers preserved in the lede
        en_lede = en.select_one('.lede')
        for other_lang, other_doc in [('es', es), ('pt', pt)]:
            other_lede = other_doc.select_one('.lede')
            if en_lede and other_lede:
                check(re.findall(r'\d+(?:[.,]\d+)*', en_lede.get_text()) ==
                      re.findall(r'\d+(?:[.,]\d+)*', other_lede.get_text()),
                      f'{other_lang}/{rel}: lede numbers differ from EN')
    # --- 3. ES/PT translation residue: node-by-node vs EN ---
    for other_lang, other_doc in [('es', es), ('pt', pt)]:
        en_texts, other_texts = text_nodes(en), text_nodes(other_doc)
        check(len(en_texts) == len(other_texts),
              f'{other_lang}/{rel}: text-node count {len(other_texts)} != EN {len(en_texts)}')
        for e, s in zip(en_texts, other_texts):
            if e == s and re.search(r'[A-Za-z]{3}', e) and not IDENTICAL_OK.match(e):
                check(False, f'{other_lang}/{rel}: untranslated residue: {e!r}')
            check(not re.search(r'[\u4e00-\u9fff]', s), f'{other_lang}/{rel}: Chinese leakage: {s!r}')
        raw = page_path(other_lang, rel).read_text()
        check(not re.search(r'[\u4e00-\u9fff]', raw), f'{other_lang}/{rel}: CJK characters in file')
        check('translate-zh-params' not in raw, f'{other_lang}/{rel}: stray reference')

# --- 4. the two pre-existing defects are fixed ---
for rel in ['insights/index.html', 'insights/water-purifier-oem-moq.html',
            'insights/water-purifier-certification-europe.html',
            'insights/choose-flow-by-water-quality.html',
            'insights/under-sink-installation-space.html',
            'insights/voltage-plug-by-country.html']:
    doc = BS(page_path('en', rel).read_text(), 'html.parser')
    langs = [a.get('data-language') for a in doc.select('header .language-switch a')]
    check(langs == ['en', 'zh', 'es', 'pt'], f'en/{rel}: insights switcher {langs}')
for rel in ['zh/index.html', 'zh/videos.html']:
    check('../insights/index.html' not in (ROOT / rel).read_text(),
          f'{rel}: still links to English insights index')
    check('href="insights/index.html"' in (ROOT / rel).read_text(),
          f'{rel}: missing corrected insights link')
# countertop article untouched: EN-only, EN-only switcher/hreflang
ct = BS((ROOT / 'insights' / 'countertop-vs-under-sink-ro.html').read_text(), 'html.parser')
check([a.get('data-language') for a in ct.select('header .language-switch a')] == ['en'],
      'countertop article switcher changed')
check(ct.select('link[hreflang]') == [],
      'countertop article hreflang changed (it has none)')

# --- 5. sitemap ---
tree = ET.parse(ROOT / 'sitemap.xml')
urls = [n.text for n in tree.getroot().findall('{*}url/{*}loc')]
expected_sitemap = 168 + 19 * len(complete_p1_new) + 69 * len(complete_p2)
check(len(urls) == len(set(urls)) == expected_sitemap,
      f'sitemap has {len(urls)} urls, expected {expected_sitemap} '
      f'(168 + 19*{len(complete_p1_new)} phase-1-new + 69*{len(complete_p2)} phase-2)')
check(not any('404' in u or 'countertop-vs-under-sink' in u for u in urls),
      'sitemap contains excluded page')
for rel in PHASE1:
    check(url_for('es', rel) in urls, f'sitemap missing es {rel}')
    check(url_for('pt', rel) in urls, f'sitemap missing pt {rel}')
for lang in complete_p1_new:
    for rel in PHASE1:
        check(url_for(lang, rel) in urls, f'sitemap missing {lang} {rel}')
for lang in complete_p2:
    for name in PHASE2:
        check(url_for(lang, 'products/' + name) in urls,
              f'sitemap missing {lang} products/{name}')
for url in urls:
    check(url.startswith(BASE), f'sitemap url outside site: {url}')
for url in tree.getroot().findall('{*}url'):
    check(url.find('{*}lastmod') is not None and url.find('{*}lastmod').text,
          'sitemap entry without lastmod')

if errors:
    print(f'FAIL: {len(errors)} checks failed:')
    for e in errors:
        print(' -', e)
    sys.exit(1)
print('PASS: EN 90 / ZH 89 / ES 19 / PT 19 files; 19 pages EN/ZH/ES/PT symmetric '
      '(lang, canonical, x-default+en+zh+es+pt hreflang, header/footer EN/ZH/ES/PT '
      'switchers, 1 h1); no broken relative links; no untranslated English '
      'residue or Chinese leakage in ES/PT; both pre-existing defects fixed; '
      'countertop article untouched; sitemap '
      f'{expected_sitemap} URLs (168 + 19*{len(complete_p1_new)} phase-1-new '
      f'+ 69*{len(complete_p2)} phase-2).')
if skipped:
    print('SKIP (pending, not yet generated):')
    for s in skipped:
        print(' -', s)
