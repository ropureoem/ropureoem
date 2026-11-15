"""Generate sitemap.xml from the actual files on disk, all languages.

Inclusion rule (per multilingual plan 2026-11-15, section 1.4/4): only published
pages. Excluded: 404.html, the 23 merged variant product pages (listed only
through their family pages), the unreleased countertop Insights article, and
any page that has no file in that language. lastmod is preserved from the
existing sitemap for URLs already listed; new URLs get today's date.
Format stays <loc> + <lastmod>, no hreflang in the sitemap.
"""
from pathlib import Path
from datetime import date
from xml.sax.saxutils import escape
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
BASE = 'https://ropureoem.com/'
TODAY = date.today().isoformat()

# 23 merged variant pages: listed only through their family pages, never in sitemap.
VARIANTS = {
    'RP-C02', 'RP-C05', 'RP-C06', 'RP-F03', 'RP-F04', 'RP-F05', 'RP-F07',
    'RP-F09', 'RP-F11', 'RP-F12', 'RP-F13', 'RP-S02', 'RP-S04', 'RP-S05',
    'RP-S06', 'RP-S08', 'RP-S09', 'RP-S13', 'RP-U10', 'RP-U13', 'RP-U25',
    'RP-W02', 'RP-W03',
}
EXCLUDED = {'404.html', 'insights/countertop-vs-under-sink-ro.html'}

def lang_pages(lang):
    """Relative EN paths that exist in this language and belong in the sitemap."""
    if lang == 'en':
        files = [*ROOT.glob('*.html'), *ROOT.glob('products/*.html'), *ROOT.glob('insights/*.html')]
        paths = sorted(p.relative_to(ROOT).as_posix() for p in files)
    else:
        base = ROOT / lang
        paths = sorted(p.relative_to(base).as_posix() for p in base.rglob('*.html'))
    out = []
    for rel in paths:
        if rel in EXCLUDED:
            continue
        if Path(rel).stem in VARIANTS:
            continue
        # The page must exist in English too (a translation never leads).
        if lang != 'en' and not (ROOT / rel).exists():
            continue
        out.append(rel)
    return out

def url_for(lang, rel):
    prefix = '' if lang == 'en' else lang + '/'
    if rel == 'index.html':
        return BASE + prefix
    if rel.endswith('/index.html'):
        return BASE + prefix + rel[:-len('index.html')]
    return BASE + prefix + rel

def main():
    old = {}
    sitemap = ROOT / 'sitemap.xml'
    if sitemap.exists():
        for url in ET.parse(sitemap).getroot().findall('{*}url'):
            loc = url.find('{*}loc').text
            lm = url.find('{*}lastmod')
            old[loc] = lm.text if lm is not None else TODAY
    langs = ['en', 'zh', 'es', 'pt', 'it', 'ru', 'ar', 'fr', 'id', 'ja', 'de', 'th']
    counts = {}
    urls = []
    for lang in langs:
        pages = lang_pages(lang)
        counts[lang] = len(pages)
        for rel in pages:
            urls.append((url_for(lang, rel), old.get(url_for(lang, rel), TODAY)))
    assert counts == {'en': 65, 'zh': 65, 'es': 65, 'pt': 65, 'it': 65, 'ru': 65, 'ar': 65, 'fr': 65, 'id': 65, 'ja': 65, 'de': 65, 'th': 48}, f'Unexpected sitemap counts: {counts}'
    assert len(urls) == len({u for u, _ in urls}) == 763
    assert not any('/404' in u or 'countertop-vs-under-sink' in u for u, _ in urls)
    assert not any('/RP-' in u and u.rsplit('/', 1)[-1][:-5] in VARIANTS for u, _ in urls)
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    xml += ''.join(f'  <url><loc>{escape(u)}</loc><lastmod>{lm}</lastmod></url>\n' for u, lm in urls)
    xml += '</urlset>\n'
    sitemap.write_text(xml)
    print(f'Generated sitemap.xml: {len(urls)} unique URLs '
          f'(en {counts["en"]} + zh {counts["zh"]} + es {counts["es"]} + pt {counts["pt"]} + it {counts["it"]} + ru {counts["ru"]} + ar {counts["ar"]} + fr {counts["fr"]} + id {counts["id"]} + ja {counts["ja"]} + de {counts["de"]} + th {counts["th"]}); '
          f'new URLs dated {TODAY}.')

if __name__ == '__main__':
    main()
