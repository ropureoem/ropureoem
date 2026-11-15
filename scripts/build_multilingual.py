"""Build a new language edition from the English sources (phase 1: Spanish).

Generalisation of build_bilingual.py: input is an English page + target language,
output is <lang>/ with the same filename. Recomputes ../ relative paths, rebuilds
the language switcher and the hreflang group, writes a self-referencing canonical.
Only the pages listed in PHASE1 are generated; English sources are never
re-translated. Counterpart EN/ZH pages get their switcher + hreflang updated
surgically (regex, byte-preserving elsewhere) — only for pages that have an
<lang> edition.

Link rule for generated pages: an internal .html link points at the <lang>
edition when that page exists, otherwise at the English edition (never at a
missing file). Shared resources (assets/styles/images/script.js) are referenced
from the site root with ../ or ../../.

Usage: python3 scripts/build_multilingual.py [es] [--update-counterparts]
"""
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit
import json, posixpath, re, sys
from bs4 import BeautifulSoup, Doctype

ROOT = Path(__file__).resolve().parent.parent
BASE = 'https://ropureoem.com/'
LANG = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith('--') else 'es'
UPDATE_COUNTERPARTS = '--update-counterparts' in sys.argv

# Phase 1 (2026-11-15 plan 8.2): home + 7 business + 5 category + insights index + 5 articles.
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

ARIA_LABEL = {'en': 'Language selection', 'zh': '语言切换', 'es': 'Selección de idioma',
              'it': 'Seleziona lingua', 'pt': 'Selecionar idioma', 'ru': 'Выбор языка'}
LANG_NAME = {'en': 'English', 'zh': 'Chinese', 'es': 'Spanish',
             'it': 'Italian', 'pt': 'Portuguese', 'ru': 'Russian'}

TRANSLATIONS = {}
_tsv = ROOT / 'scripts' / 'i18n' / f'{LANG}.tsv'
for line in _tsv.read_text().splitlines():
    if line.strip() and '\t' in line:
        k, v = line.split('\t', 1)
        TRANSLATIONS[k] = v
KEYS = sorted(TRANSLATIONS, key=len, reverse=True)
# Short keys (len < 5) are exact-match only: substring use would corrupt
# technical tokens (e.g. 'UK' inside 'UKCA', 'EU' inside nothing else but safe).
LONG_KEYS = [k for k in KEYS if len(k) >= 5 and not k.endswith('.')]
PATTERN = re.compile('|'.join(re.escape(k) for k in LONG_KEYS)) if LONG_KEYS else None

MONTHS_BY_LANG = {
    'es': {'January': 'enero', 'February': 'febrero', 'March': 'marzo', 'April': 'abril',
           'May': 'mayo', 'June': 'junio', 'July': 'julio', 'August': 'agosto',
           'September': 'septiembre', 'October': 'octubre', 'November': 'noviembre',
           'December': 'diciembre'},
    'pt': {'January': 'janeiro', 'February': 'fevereiro', 'March': 'março', 'April': 'abril',
           'May': 'maio', 'June': 'junho', 'July': 'julho', 'August': 'agosto',
           'September': 'setembro', 'October': 'outubro', 'November': 'novembro',
           'December': 'dezembro'},
}
MONTHS = MONTHS_BY_LANG.get(LANG, MONTHS_BY_LANG['es'])

def translate(text):
    if text in TRANSLATIONS:
        return TRANSLATIONS[text]
    m = re.fullmatch(r'(RP-[A-Z0-9-]+) product photograph', text)
    if m:
        return f'Foto do produto {m[1]}' if LANG == 'pt' else f'Fotografía del producto {m[1]}'
    m = re.fullmatch(r'(\d+) models\. Specifications are confirmed per model and order\.', text)
    if m:
        if LANG == 'pt':
            return f'{m[1]} modelos. Especificações confirmadas por modelo e pedido.'
        return f'{m[1]} modelos. Especificaciones confirmadas por modelo y pedido.'
    m = re.fullmatch(r'(\d+) (January|February|March|April|May|June|July|August|September|October|November|December) (\d{4})', text)
    if m:
        return f'{m[1]} de {MONTHS[m[2]]} de {m[3]}'
    if PATTERN:
        return PATTERN.sub(lambda m: TRANSLATIONS[m[0]], text)
    return text

def relative(target, page):
    return posixpath.relpath(target, str(page.parent))

def url_for(lang, rel):
    """Absolute URL of a page in a language; any index.html uses directory form."""
    prefix = '' if lang == 'en' else lang + '/'
    if rel == 'index.html':
        return BASE + prefix
    if rel.endswith('/index.html'):
        return BASE + prefix + rel[:-len('index.html')]
    return BASE + prefix + rel

def available_langs(rel):
    langs = ['en']
    # Every language edition that exists for this page, in canonical order.
    # The target language counts when it is in PHASE1 (generated this run).
    for lang in ['zh', 'es', 'it', 'pt', 'ru']:
        if (ROOT / lang / rel).exists() or (lang == LANG and rel in PHASE1):
            langs.append(lang)
    return langs

def rebuild_languages(doc, page, current_lang, langs):
    """Strip old switchers + hreflang, rebuild for the langs that exist."""
    for node in doc.select('.language-switch,link[hreflang]'):
        node.decompose()
    en_rel = str(page.relative_to(ROOT / LANG)) if current_lang == LANG else str(page)
    # hreflang group: x-default (English) + one link per existing language.
    for lang in ['x-default'] + langs:
        target_lang = 'en' if lang == 'x-default' else lang
        href = url_for(target_lang, en_rel)
        doc.head.append(doc.new_tag('link', rel='alternate', hreflang=lang, href=href))
    for parent in [doc.header, doc.footer]:
        if parent is None:
            continue
        nav = doc.new_tag('nav', attrs={'class': 'language-switch',
                                         'aria-label': ARIA_LABEL[current_lang]})
        for lang in langs:
            target = (lang + '/' + en_rel) if lang != 'en' else en_rel
            a = doc.new_tag('a', href=relative(target, page), hreflang=lang, lang=lang,
                            attrs={'data-language': lang})
            a.string = lang.upper()
            if lang == current_lang:
                a['aria-current'] = 'true'
            nav.append(a)
        if parent is doc.header:
            tools = doc.select_one('.header-tools')
            if tools is None:
                tools = doc.new_tag('div', attrs={'class': 'header-tools'})
                search = doc.select_one('.header-search')
                search.wrap(tools)
            tools.append(nav)
        else:
            # Footer switcher lives inside the Contact column, right after
            # the Contact link (2026-11-15: moved out of the page bottom so
            # it stays reachable above the mobile bottom nav). No `wrap`
            # class inside the footer grid cell.
            contact = parent.select_one('.footer-in a[href$="contact.html"]')
            if contact is not None:
                contact.insert_after(nav)
            else:
                parent.append(nav)

def es_target_exists(rel):
    return rel in PHASE1 or (ROOT / LANG / rel).exists()

def rewrite_link(val, page):
    """Rewrite one internal href/src/action from an English source page to the
    generated <lang> page. Returns the new value."""
    u = urlsplit(val)
    if u.scheme or u.netloc or not u.path:
        return val
    src_rel = str(page.relative_to(ROOT / LANG))  # English source path, e.g. products/x.html
    resolved = posixpath.normpath(posixpath.join(str(Path(src_rel).parent), u.path))
    if resolved.endswith('.html'):
        target = (LANG + '/' + resolved) if es_target_exists(resolved) else resolved
    else:
        target = resolved  # shared resource at site root
    return urlunsplit(('', '', relative(target, page), u.query, u.fragment))

def translate_json_ld(value, canonical):
    if isinstance(value, dict):
        out = {}
        for k, v in value.items():
            if k == 'url' and isinstance(v, str) and v.startswith(BASE):
                out[k] = v
            elif k == '@id' and isinstance(v, str) and v.startswith(BASE):
                out[k] = canonical
            elif k == 'availableLanguage' and isinstance(v, list):
                out[k] = ['English', LANG_NAME[LANG]]
            else:
                out[k] = translate_json_ld(v, canonical)
        return out
    if isinstance(value, list):
        return [translate_json_ld(v, canonical) for v in value]
    if isinstance(value, str):
        if value.startswith(BASE):
            return value
        return translate(value)
    return value

def generate_page(rel):
    source = ROOT / rel
    target = ROOT / LANG / rel
    doc = BeautifulSoup(source.read_text(), 'html.parser')
    for menu in doc.select('details.nav-menu'):
        menu.attrs.pop('open', None)
    doc.html['lang'] = LANG
    missing = set()
    for node in doc.find_all(string=True):
        if isinstance(node, Doctype) or node.parent.name in ('script', 'style') or not node.strip():
            continue
        translated = translate(str(node).strip())
        if (translated == str(node).strip() and str(node).strip() not in TRANSLATIONS
                and re.search(r'[A-Za-z]{3}', translated)
                and not re.fullmatch(r'(?:ROPureOEM|WhatsApp.*|info@ropureoem\.com|SKU:.*|RP-.*|'
                                     r'OEM / ODM|EN|ZH|ES|FOB Shenzhen|MOQ.*|CE.*|UKCA.*|RoHS|'
                                     r'REACH|GPD.*|.*\d+.*)', translated)):
            missing.add(translated)
        node.replace_with(translated)
    for node in doc.select('[placeholder],[aria-label],img[alt]'):
        for attr in ['placeholder', 'aria-label', 'alt']:
            if node.has_attr(attr):
                node[attr] = translate(node[attr])
    canonical = url_for(LANG, rel)
    if doc.select_one('link[rel=canonical]'):
        doc.select_one('link[rel=canonical]')['href'] = canonical
    for node in doc.select('meta[property="og:url"]'):
        node['content'] = canonical
    for node in doc.select('meta[name=description],meta[property="og:description"]'):
        node['content'] = translate(node['content'])
    for node in doc.select('meta[property="og:title"]'):
        node['content'] = translate(node['content'])
    for node in doc.select('script[type="application/ld+json"]'):
        data = translate_json_ld(json.loads(node.string), canonical)
        node.string = json.dumps(data, ensure_ascii=False)
    # Rewrite internal links after translation (switcher links excluded: they
    # are rebuilt below; alternate links are rebuilt below).
    for node in doc.select('[href],[src],[action]'):
        if node.has_attr('data-language') or node.get('rel') == ['alternate']:
            continue
        for attr in ['href', 'src', 'action']:
            val = node.get(attr)
            if val:
                node[attr] = rewrite_link(val, target)
    rebuild_languages(doc, target, LANG, available_langs(rel))
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(str(doc))
    return missing

# --- surgical counterpart update (EN/ZH pages): regex only, rest untouched ---
SWITCHER_RE = re.compile(r'(<nav[^>]*class="[^"]*language-switch[^"]*"[^>]*>)(.*?)(</nav>)', re.S)
# Full hreflang run: x-default + every language edition present on the page.
HREFLANG_RUN_RE = re.compile(r'(?:<link[^>]*hreflang="(?:x-default|en|zh|es|it|pt|ru)"[^>]*/>\s*)+')

def counterpart_href(lang, rel, from_lang):
    """Relative href from a page in from_lang to the same page in lang."""
    if lang == 'en':
        tgt = rel
    else:
        tgt = lang + '/' + rel
    if from_lang == 'en':
        base = Path(rel).parent
    else:
        base = Path(from_lang) / Path(rel).parent
    return posixpath.relpath(tgt, str(base))

def update_counterpart(rel, from_lang):
    path = (ROOT / from_lang / rel) if from_lang != 'en' else (ROOT / rel)
    text = path.read_text()
    langs = available_langs(rel)
    # hreflang group: x-default + one per existing language.
    group = ''.join(
        f'<link href="{url_for("en" if l == "x-default" else l, rel)}" hreflang="{l}" rel="alternate"/>\n'
        for l in ['x-default'] + langs)
    new_text, n_href = HREFLANG_RUN_RE.subn(group.rstrip('\n'), text, count=1)
    if n_href == 0:
        print(f'WARN no hreflang run found in {path}')
        text = text
    else:
        text = new_text
    # switcher navs (header + footer): keep existing anchors, add missing langs.
    def fix_switcher(m):
        open_tag, inner, close = m.group(1), m.group(2), m.group(3)
        soup = BeautifulSoup(inner, 'html.parser')
        have = {a.get('data-language') for a in soup.find_all('a')}
        for lang in langs:
            if lang in have:
                continue
            a = soup.new_tag('a', href=counterpart_href(lang, rel, from_lang),
                             hreflang=lang, lang=lang, attrs={'data-language': lang})
            a.string = lang.upper()
            soup.append(a)
        # Normalise hrefs of existing anchors too (EN insights had none for ZH).
        for a in soup.find_all('a'):
            a['href'] = counterpart_href(a['data-language'], rel, from_lang)
        return open_tag + ''.join(str(x) for x in soup.contents) + close
    text, n_sw = SWITCHER_RE.subn(fix_switcher, text)
    if n_sw == 0:
        print(f'WARN no switcher found in {path}')
    path.write_text(text)
    return n_href, n_sw

def main():
    all_missing = set()
    for rel in PHASE1:
        missing = generate_page(rel)
        all_missing |= missing
        print(f'generated {LANG}/{rel}')
    if UPDATE_COUNTERPARTS:
        for rel in PHASE1:
            # Every existing edition of the page gets the new language in its
            # switcher + hreflang group (EN + ZH + ES for the pt run; the
            # generated edition itself is skipped).
            for from_lang in ['en', 'zh', 'es']:
                if from_lang == LANG:
                    continue
                if from_lang != 'en' and not (ROOT / from_lang / rel).exists():
                    continue
                update_counterpart(rel, from_lang)
        print('counterparts updated (EN + ZH + ES switchers/hreflang for the 19 pages)')
    print(f'Generated {len(PHASE1)} {LANG} pages.')
    if all_missing:
        print('Untranslated copy requiring review:', json.dumps(sorted(all_missing), ensure_ascii=False))

if __name__ == '__main__':
    main()
