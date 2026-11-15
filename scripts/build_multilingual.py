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
from bs4 import BeautifulSoup, Comment, Doctype

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
              'it': 'Seleziona lingua', 'pt': 'Selecionar idioma', 'ru': 'Выбор языка',
              'fr': 'Sélection de la langue', 'ar': 'اختيار اللغة', 'id': 'Pilih bahasa',
              'ja': '言語を選択', 'de': 'Sprache wählen', 'th': 'เลือกภาษา'}
LANG_NAME = {'en': 'English', 'zh': 'Chinese', 'es': 'Spanish',
             'it': 'Italian', 'pt': 'Portuguese', 'ru': 'Russian',
             'fr': 'French', 'ar': 'Arabic', 'id': 'Indonesian',
             'ja': 'Japanese', 'de': 'German', 'th': 'Thai'}

# RTL languages (2026-11-15: Arabic is the only RTL language of the 9).
# Generated pages get dir="rtl" on <html>; the shared stylesheet carries the
# [dir="rtl"] overrides in styles/components.css. Arrows (→/←/↗/↑) are kept
# as-is: the wordlists already carry them in the translated strings.
RTL_LANGS = {'ar'}

TRANSLATIONS = {}
_tsv = ROOT / 'scripts' / 'i18n' / f'{LANG}.tsv'
if _tsv.exists():
    for line in _tsv.read_text().splitlines():
        if line.strip() and '\t' in line:
            k, v = line.split('\t', 1)
            TRANSLATIONS[k] = v
else:
    print(f'WARN no wordlist yet: {_tsv} — translating with fallbacks only',
          file=sys.stderr)


def _norm_key(k):
    """Normalise a TSV key / lookup string: strip surrounding space and one
    trailing period. 'X.' and 'X' are the same key; the full stop is restored
    (or dropped) to match the input at translate() time."""
    k = k.strip()
    return k[:-1] if k.endswith('.') else k


# Normalised lookup: the exact-form key wins when both 'X' and 'X.' exist.
NORM = {}
# Normalised keys whose WINNING TSV entry ended with '.': only for those may
# _pattern_sub drop the value's trailing period mid-sentence. A value ending
# in '.' whose key had no period (e.g. ru 'см.' = 'see', an abbreviation)
# must keep its period (2026-11-15: the old blanket strip turned
# 'см. RP-C01' into 'см RP-C01' in 65 ru head fields).
PERIOD_NORM = set()
for _k, _v in TRANSLATIONS.items():
    _nk = _norm_key(_k)
    if _nk not in NORM or _k == _nk:
        NORM[_nk] = _v
        if _k.endswith('.'):
            PERIOD_NORM.add(_nk)
        else:
            PERIOD_NORM.discard(_nk)
KEYS = sorted(NORM, key=len, reverse=True)
# Substring matching uses the normalised keys (len >= 5): sentence keys that
# end with '.' were previously excluded entirely, so a node containing such a
# sentence as a prefix — e.g. the MOQ lede, which continues past the TSV key
# — never matched (2026-11-15: 9 untranslated residues in es/).
LONG_KEYS = [k for k in KEYS if len(k) >= 5]
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
    'it': {'January': 'gennaio', 'February': 'febbraio', 'March': 'marzo', 'April': 'aprile',
           'May': 'maggio', 'June': 'giugno', 'July': 'luglio', 'August': 'agosto',
           'September': 'settembre', 'October': 'ottobre', 'November': 'novembre',
           'December': 'dicembre'},
    # Russian months are genitive (as in '7 ноября 2026 г.'); ' г.' is added
    # by the date format, not the month name.
    'ru': {'January': 'января', 'February': 'февраля', 'March': 'марта', 'April': 'апреля',
           'May': 'мая', 'June': 'июня', 'July': 'июля', 'August': 'августа',
           'September': 'сентября', 'October': 'октября', 'November': 'ноября',
           'December': 'декабря'},
    'fr': {'January': 'janvier', 'February': 'février', 'March': 'mars', 'April': 'avril',
           'May': 'mai', 'June': 'juin', 'July': 'juillet', 'August': 'août',
           'September': 'septembre', 'October': 'octobre', 'November': 'novembre',
           'December': 'décembre'},
    'ar': {'January': 'يناير', 'February': 'فبراير', 'March': 'مارس', 'April': 'أبريل',
           'May': 'مايو', 'June': 'يونيو', 'July': 'يوليو', 'August': 'أغسطس',
           'September': 'سبتمبر', 'October': 'أكتوبر', 'November': 'نوفمبر',
           'December': 'ديسمبر'},
    'id': {'January': 'Januari', 'February': 'Februari', 'March': 'Maret', 'April': 'April',
           'May': 'Mei', 'June': 'Juni', 'July': 'Juli', 'August': 'Agustus',
           'September': 'September', 'October': 'Oktober', 'November': 'November',
           'December': 'Desember'},
    'ja': {'January': '1月', 'February': '2月', 'March': '3月', 'April': '4月',
           'May': '5月', 'June': '6月', 'July': '7月', 'August': '8月',
           'September': '9月', 'October': '10月', 'November': '11月',
           'December': '12月'},
    'de': {'January': 'Januar', 'February': 'Februar', 'March': 'März', 'April': 'April',
           'May': 'Mai', 'June': 'Juni', 'July': 'Juli', 'August': 'August',
           'September': 'September', 'October': 'Oktober', 'November': 'November',
           'December': 'Dezember'},
    'th': {'January': 'มกราคม', 'February': 'กุมภาพันธ์', 'March': 'มีนาคม', 'April': 'เมษายน',
           'May': 'พฤษภาคม', 'June': 'มิถุนายน', 'July': 'กรกฎาคม', 'August': 'สิงหาคม',
           'September': 'กันยายน', 'October': 'ตุลาคม', 'November': 'พฤศจิกายน',
           'December': 'ธันวาคม'},
}
MONTHS = MONTHS_BY_LANG.get(LANG, MONTHS_BY_LANG['es'])
# Date order per language (templates use {d} day, {m} month, {y} year).
DATE_FMT = {
    'es': '{d} de {m} de {y}', 'pt': '{d} de {m} de {y}',
    'it': '{d} {m} {y}', 'fr': '{d} {m} {y}', 'id': '{d} {m} {y}',
    'ar': '{d} {m} {y}', 'ru': '{d} {m} {y} г.',
    'ja': '{y}年{m}{d}日', 'de': '{d}. {m} {y}', 'th': '{d} {m} {y}',
}

# Regex fallbacks for strings that are generated, not in the TSV: the product
# photograph alt text and the 'N models. Specifications…' lede. Wording matches
# each language's TSV entries for the same sentences (e.g. de 'je Modell',
# ja '仕様はモデル・ご注文ごとに確認いたします').
# Stage-2 product pages (2026-11-15): the same treatment for the product
# heading, quote button, 'More …' / '← Back to …' headings and the
# 'N specification rows from the ROPureOEM catalogue.' line. These are
# templated per model / count, so a regex beats one TSV key per model.
PHOTO_TEXT = {
    'es': 'Fotografía del producto {id}', 'pt': 'Foto do produto {id}',
    'it': 'Foto del prodotto {id}', 'ru': 'Фото продукта {id}',
    'fr': 'Photo du produit {id}', 'ar': 'صورة المنتج {id}',
    'id': 'Foto produk {id}', 'ja': '{id}の製品写真', 'de': 'Produktfoto {id}',
    'th': 'ภาพถ่ายผลิตภัณฑ์ {id}',
}
ABOUT_TEXT = {
    'es': 'Acerca de {id}', 'pt': 'Sobre {id}', 'it': 'Informazioni su {id}',
    'ru': 'О {id}', 'fr': 'À propos de {id}', 'ar': 'حول {id}',
    'id': 'Tentang {id}', 'ja': '{id}について', 'de': 'Über {id}',
    'th': 'เกี่ยวกับ {id}',
}
QUOTE_TEXT = {
    'es': 'Solicitar presupuesto para {id}', 'pt': 'Solicitar orçamento para {id}',
    'it': 'Richiedi un preventivo per {id}', 'ru': 'Запросить цену для {id}',
    'fr': 'Demander un devis pour {id}', 'ar': 'اطلب عرض سعر لـ {id}',
    'id': 'Minta penawaran untuk {id}', 'ja': '{id}の見積もりを依頼する',
    'de': 'Angebot anfordern für {id}', 'th': 'ขอใบเสนอราคาสำหรับ {id}',
}
MORE_TEXT = {
    'es': 'Más {rest}', 'pt': 'Mais {rest}', 'it': 'Altri {rest}',
    'ru': 'Ещё {rest}', 'fr': 'Plus de {rest}', 'ar': 'المزيد من {rest}',
    'id': 'Lebih banyak {rest}', 'ja': 'その他の{rest}', 'de': 'Weitere {rest}',
    'th': '{rest} เพิ่มเติม',
}
BACK_TEXT = {
    'es': '← Volver a {rest}', 'pt': '← Voltar para {rest}',
    'it': '← Torna a {rest}', 'ru': '← Назад к {rest}',
    'fr': '← Retour à {rest}', 'ar': '← عودة إلى {rest}',
    'id': '← Kembali ke {rest}', 'ja': '← {rest}に戻る',
    'de': '← Zurück zu {rest}', 'th': '← กลับไปที่ {rest}',
}
SPEC_ROWS_TEXT = {
    'es': '{n} filas de especificaciones del catálogo de ROPureOEM.',
    'pt': '{n} linhas de especificações do catálogo da ROPureOEM.',
    'it': '{n} righe di specifiche dal catalogo ROPureOEM.',
    'ru': '{n} строк спецификаций из каталога ROPureOEM.',
    'fr': '{n} lignes de spécifications du catalogue ROPureOEM.',
    'ar': '{n} صفوف مواصفات من كتالوج ROPureOEM.',
    'id': '{n} baris spesifikasi dari katalog ROPureOEM.',
    'ja': 'ROPureOEMカタログの仕様 {n} 行。',
    'de': '{n} Spezifikationszeilen aus dem ROPureOEM-Katalog.',
    'th': '{n} แถวข้อมูลจำเพาะจากแคตตาล็อก ROPureOEM.',
}
MODELS_TEXT = {
    'es': '{n} modelos. Especificaciones confirmadas por modelo y pedido.',
    'pt': '{n} modelos. Especificações confirmadas por modelo e pedido.',
    'it': '{n} modelli. Specifiche confermate per modello e ordine.',
    'fr': '{n} modèles. Spécifications confirmées par modèle et par commande.',
    'id': '{n} model. Spesifikasi dikonfirmasi per model dan pesanan.',
    'ja': '{n}モデル。仕様はモデル・ご注文ごとに確認いたします。',
    'de': '{n} Modelle. Spezifikationen werden je Modell und Auftrag bestätigt.',
    'th': '{n} รุ่น ข้อมูลจำเพาะได้รับการยืนยันตามรุ่นและคำสั่งซื้อ.',
}


def _models_sentence(n):
    """'N models. Specifications are confirmed per model and order.' with
    correct number agreement. Russian: 1 модель / 2–4 модели / 5+ моделей.
    Arabic: 1 موديل واحد / 2 موديلان (dual) / 3–10 موديلات / 11+ موديلًا."""
    if LANG == 'ru':
        if n % 10 == 1 and n % 100 != 11:
            noun = 'модель'
        elif n % 10 in (2, 3, 4) and n % 100 not in (12, 13, 14):
            noun = 'модели'
        else:
            noun = 'моделей'
        return (f'{n} {noun}. Характеристики подтверждаются '
                'для каждой модели и заказа.')
    if LANG == 'ar':
        if n == 1:
            head = 'موديل واحد'
        elif n == 2:
            head = 'موديلان'
        elif 3 <= n <= 10:
            head = f'{n} موديلات'
        else:
            head = f'{n} موديلًا'
        return f'{head}. تُؤكَّد المواصفات لكل موديل وطلب.'
    return MODELS_TEXT.get(LANG, MODELS_TEXT['es']).format(n=n)


def _fix_trailing_period(result, text):
    """Make the replacement's final period match the input's: a normalised
    lookup must not add a period the source did not have, nor drop one it had.
    A CJK sentence-final mark (。/！/？) already closes the sentence, so no
    ASCII period is appended after it (2026-11-15: ja metas rebuilt as
    'モデル。.' instead of 'モデル。')."""
    if text.endswith('.') and not result.endswith(('.', '。', '！', '？', '!', '?')):
        return result + '.'
    if not text.endswith('.') and result.endswith('.'):
        return result[:-1]
    return result


def _pattern_sub(text):
    """Substring substitution with normalised keys. A key's own trailing period
    must not leak into the middle of a longer sentence: when the match is
    followed by more text, the replacement's final period is dropped (the
    source's own punctuation stays). Only keys that themselves ended with '.'
    get this treatment — a value like ru 'см.' (abbreviation 'see') keeps its
    period when its key had none."""
    def repl(m):
        val = NORM[m[0]]
        after = text[m.end():m.end() + 1]
        if val.endswith('.') and m[0] in PERIOD_NORM and after:
            val = val[:-1]
        return val
    # A replacement ending in a CJK full stop leaves the source's ASCII
    # period stranded ('モデル。.'): collapse it (2026-11-15, ja rebuild).
    return PATTERN.sub(repl, text).replace('。.', '。')


def translate(text):
    if text in TRANSLATIONS:
        return TRANSLATIONS[text]
    nk = _norm_key(text)
    if nk in NORM:
        return _fix_trailing_period(NORM[nk], text)
    m = re.fullmatch(r'(RP-[A-Z0-9-]+) product photograph', text)
    if m:
        return PHOTO_TEXT.get(LANG, PHOTO_TEXT['es']).format(id=m[1])
    m = re.fullmatch(r'About (RP-[A-Z0-9-]+)', text)
    if m:
        return ABOUT_TEXT.get(LANG, ABOUT_TEXT['es']).format(id=m[1])
    m = re.fullmatch(r'Get a Quote for (RP-[A-Z0-9-]+)', text)
    if m:
        return QUOTE_TEXT.get(LANG, QUOTE_TEXT['es']).format(id=m[1])
    m = re.fullmatch(r'More (.+)', text)
    if m:
        return MORE_TEXT.get(LANG, MORE_TEXT['es']).format(rest=translate(m[1]))
    m = re.fullmatch(r'← Back to (.+)', text)
    if m:
        return BACK_TEXT.get(LANG, BACK_TEXT['es']).format(rest=translate(m[1]))
    m = re.fullmatch(r'(\d+) specification rows from the ROPureOEM catalogue\.', text)
    if m:
        return SPEC_ROWS_TEXT.get(LANG, SPEC_ROWS_TEXT['es']).format(n=m[1])
    m = re.fullmatch(r'(\d+) models\. Specifications are confirmed per model and order\.', text)
    if m:
        return _models_sentence(int(m[1]))
    m = re.fullmatch(r'(\d+) (January|February|March|April|May|June|July|August|September|October|November|December) (\d{4})', text)
    if m:
        return DATE_FMT.get(LANG, DATE_FMT['es']).format(d=m[1], m=MONTHS[m[2]], y=m[3])
    if PATTERN:
        return _pattern_sub(text)
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
    # The switcher lists the site's full language set (user-fixed 2026-11-15):
    # EN, ZH, ES, PT, IT, RU, AR, FR, ID, JA, DE, TH — even before every edition
    # of this page exists. Links resolve once that language batch lands
    # (verify_bilingual.py gates not-yet-generated editions as SKIP, not FAIL).
    return ['en', 'zh', 'es', 'pt', 'it', 'ru', 'ar', 'fr', 'id', 'ja', 'de', 'th']

def rebuild_languages(doc, page, current_lang, langs):
    """Strip old switchers + hreflang, rebuild for the full language set."""
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

def _looks_untranslated(s):
    """True when a string that translate() left unchanged still looks like
    English copy needing review. Brand/code/unit tokens are fine as-is; the
    old blanket `.*\\d+.*` exclusion is gone — it hid every residue that
    contained a number (the MOQ lede has '200' and '40', so it never surfaced)."""
    if not re.search(r'[A-Za-z]{3}', s):
        return False
    return not re.fullmatch(
        r'(?:ROPureOEM|WhatsApp.*|info@ropureoem\.com|SKU:.*|RP-.*|'
        r'OEM / ODM|EN|ZH|ES|PT|IT|RU|FR|AR|ID|JA|DE|TH|FOB Shenzhen|MOQ.*|CE.*|UKCA.*|RoHS|'
        r'REACH|GPD.*|\+86.*|[\W_\d]*)', s)


def _json_ld_texts(value):
    """(key, string) pairs for translatable JSON-LD copy: name / description /
    headline / answer text. Schema enums (@type), URLs and ids are excluded."""
    if isinstance(value, dict):
        for k, v in value.items():
            if k in ('name', 'description', 'headline', 'text'):
                if isinstance(v, str):
                    yield k, v
                else:
                    yield from _json_ld_texts(v)
            elif k not in ('@type', '@context', '@id', 'url', 'image',
                           'datePublished', 'dateModified', 'availableLanguage'):
                yield from _json_ld_texts(v)
    elif isinstance(value, list):
        for v in value:
            yield from _json_ld_texts(v)


def generate_page(rel):
    source = ROOT / rel
    target = ROOT / LANG / rel
    doc = BeautifulSoup(source.read_text(), 'html.parser')
    # --- Wave-2 regression guard (2026-11-15, item 6) ---
    # The 23 merged/retired stubs and 14 family pages got their titles/metas
    # fixed directly in the <lang> HTML (commit 7d1a922), because the English
    # meta is built from lede fragments in forms no TSV key matches
    # (lowercased first word, '; see RP-XX' suffix, truncated first sentence).
    # If a rebuild re-translates a head field to exactly the English source
    # (translate() changed nothing) while the existing <lang> page already
    # carries a translated value, keep the existing value instead of shipping
    # English residue, and flag the English string for TSV coverage.
    # Partial residue (boilerplate translated, head clause not) is covered by
    # the TSV fragment keys added with this guard, not by this fallback.
    _EN_HEAD = {}
    _OLD_HEAD = {}
    if target.exists():
        _old = BeautifulSoup(target.read_text(), 'html.parser')
        def _head_val(d, sel, attr=None):
            n = d.select_one(sel) if sel else d.title
            if n is None:
                return None
            return n['content'] if attr else n.get_text()
        _OLD_HEAD = {
            'title': _head_val(_old, None),
            'meta': _head_val(_old, 'meta[name=description]', 'content'),
            'og:title': _head_val(_old, 'meta[property="og:title"]', 'content'),
            'og:description': _head_val(_old, 'meta[property="og:description"]', 'content'),
        }
    _EN_HEAD = {
        'title': doc.title.get_text() if doc.title else None,
        'meta': (doc.select_one('meta[name=description]') or {}).get('content'),
        'og:title': (doc.select_one('meta[property="og:title"]') or {}).get('content'),
        'og:description': (doc.select_one('meta[property="og:description"]') or {}).get('content'),
    }
    for menu in doc.select('details.nav-menu'):
        menu.attrs.pop('open', None)
    doc.html['lang'] = LANG
    if LANG in RTL_LANGS:
        doc.html['dir'] = 'rtl'
    missing = set()
    for node in doc.find_all(string=True):
        # HTML comments are invisible dev notes (e.g. '<!-- RP-F03 merged into
        # RP-F02 -->'): translating them via replace_with() strips the comment
        # markers and the text becomes visible on the page (2026-11-15: es
        # RP-C02 shipped 'RP-C02 fusionado en RP-C01' as visible text between
        # </head> and <body>). Leave comments byte-identical, like Doctype.
        if isinstance(node, (Doctype, Comment)) or node.parent.name in ('script', 'style') or not node.strip():
            continue
        translated = translate(str(node).strip())
        if translated == str(node).strip() and _looks_untranslated(translated):
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
        if node['content'] == translate(node['content']) and _looks_untranslated(node['content']):
            missing.add(node['content'])
        node['content'] = translate(node['content'])
    for node in doc.select('meta[property="og:title"]'):
        if node['content'] == translate(node['content']) and _looks_untranslated(node['content']):
            missing.add(node['content'])
        node['content'] = translate(node['content'])
    # Wave-2 regression guard: restore the existing translated head value when
    # the fresh translation is byte-identical to the English source.
    if _OLD_HEAD:
        def _restore(sel, field, attr=None):
            node = doc.select_one(sel) if sel else doc.title
            if node is None:
                return
            cur = node['content'] if attr else node.get_text()
            en = _EN_HEAD.get(field)
            old = _OLD_HEAD.get(field)
            if en is not None and cur == en and old is not None and old != en:
                if attr:
                    node['content'] = old
                else:
                    node.string = old
                print(f'WARNING {LANG}/{rel} [{field}]: fresh translation is '
                      f'English; kept existing translated value')
                missing.add(en)
        _restore(None, 'title')
        _restore('meta[name=description]', 'meta', 'content')
        _restore('meta[property="og:title"]', 'og:title', 'content')
        _restore('meta[property="og:description"]', 'og:description', 'content')
    for node in doc.select('script[type="application/ld+json"]'):
        data = json.loads(node.string)
        # JSON-LD copy was never checked for residues: the two untranslated
        # certification answers shipped silently (2026-11-15). Compare the
        # descriptive strings before/after translation.
        before = {v for _, v in _json_ld_texts(data)}
        data = translate_json_ld(data, canonical)
        for _, v in _json_ld_texts(data):
            if v in before and _looks_untranslated(v):
                missing.add(v)
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
HREFLANG_RUN_RE = re.compile(r'(?:<link[^>]*hreflang="(?:x-default|en|zh|es|it|pt|ru|fr|ar|id|ja|de|th)"[^>]*/>\s*)+')

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
        # Keep anchors in canonical 12-language order (EN, ZH, ES, PT, IT,
        # RU, AR, FR, ID, JA, DE, TH) even when a language is appended later.
        order = {'en': 0, 'zh': 1, 'es': 2, 'pt': 3, 'it': 4, 'ru': 5,
                 'ar': 6, 'fr': 7, 'id': 8, 'ja': 9, 'de': 10, 'th': 11}
        anchors = sorted(soup.find_all('a'),
                         key=lambda a: order.get(a.get('data-language'), 99))
        return open_tag + ''.join(str(a) for a in anchors) + close
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
            # switcher + hreflang group (all 11 languages; editions that do
            # not exist yet for this page are skipped by the exists-guard).
            for from_lang in ['en', 'zh', 'es', 'pt', 'it', 'ru', 'ar',
                              'fr', 'id', 'ja', 'de']:
                if from_lang == LANG:
                    continue
                if from_lang != 'en' and not (ROOT / from_lang / rel).exists():
                    continue
                update_counterpart(rel, from_lang)
        print('counterparts updated (all existing editions: switchers/hreflang for the 19 pages)')
    print(f'Generated {len(PHASE1)} {LANG} pages.')
    if all_missing:
        print('Untranslated copy requiring review:', json.dumps(sorted(all_missing), ensure_ascii=False))

if __name__ == '__main__':
    main()
