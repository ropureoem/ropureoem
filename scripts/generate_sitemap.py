"""Generate the requested full HTML inventory (including the standalone 404 page).

There are 62 models, five category documents, seven top-level business pages,
and one 404 document. Query-string catalogue filters are not separate pages.
Chinese counterparts under zh/ are included. Historical previews are excluded;
each language index.html uses its canonical directory URL.
"""
from pathlib import Path
from xml.sax.saxutils import escape

root = Path(__file__).resolve().parent.parent
pages = sorted([*root.glob('*.html'), *root.glob('products/*.html'), *root.glob('zh/**/*.html')])
urls = ['https://ropureoem.com/' + (p.relative_to(root).parent.as_posix().replace('.', '') + '/' if p.name == 'index.html' and p.parent != root else '' if p.name == 'index.html' else p.relative_to(root).as_posix()) for p in pages]
assert len(urls) == len(set(urls))
xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
xml += ''.join('  <url><loc>' + escape(url) + '</loc></url>\n' for url in urls)
xml += '</urlset>\n'
(root / 'sitemap.xml').write_text(xml)
print(f'Generated sitemap.xml: {len(urls)} unique URLs')
