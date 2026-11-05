"""Build reviewed Chinese translations from English sources; preserve spec values/assets.

Run before packaging. English sources own the catalogue. zh.tsv translates copy,
product names and labels. Specification values are copied verbatim (except the
explicit unresolved-value phrase), so no numeric conversion is performed.
"""
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit
import json, posixpath, re, zipfile
from bs4 import BeautifulSoup, Doctype

ROOT = Path(__file__).resolve().parent.parent
BASE = 'https://ropureoem.com/'
TRANSLATIONS = dict(line.split('\t', 1) for line in (ROOT / 'scripts/i18n/zh.tsv').read_text().splitlines() if line.strip())
KEYS = sorted(TRANSLATIONS, key=len, reverse=True)
PATTERN = re.compile('|'.join(re.escape(k) for k in KEYS))

def translate(text):
    if text in TRANSLATIONS:
        return TRANSLATIONS[text]
    match = re.fullmatch(r'(\d+) specification rows from the ROPureOEM catalogue\.', text)
    if match:
        return f'ROPureOEM 目录中的 {match[1]} 行规格。'
    match = re.fullmatch(r'(\d+) models\. Specifications are confirmed per model and order\.', text)
    if match:
        return f'{match[1]} 款型号。规格按型号及订单确认。'
    match = re.fullmatch(r'Split-tank water softener, ([\d,]+) grain\. Photo shows the split-tank softener series; size varies by model\.', text)
    if match:
        return f'分罐式软水机，{match[1]} grain。图片展示分罐式软水机系列；尺寸因型号而异。'
    match = re.fullmatch(r'Represents the (WT-\w+) variant; (.+) options are confirmed per order\.', text)
    if match:
        labels={'cartridge and finish':'滤芯与表面处理','display and finish':'显示与表面处理','mounting and finish':'安装与表面处理'}
        return f'代表 {match[1]} 变体；{labels[match[2]]}选项按订单确认。'
    if text.startswith('Get a Quote for '):
        return '获取 '+text.removeprefix('Get a Quote for ')+' 报价'
    if text.startswith('More '):
        return '更多'+translate(text[5:])
    if text.startswith('← Back to '):
        return '← 返回'+translate(text[10:])
    return PATTERN.sub(lambda m: TRANSLATIONS[m[0]], text)

def relative(target, page):
    return posixpath.relpath(target, str(page.parent))

def add_languages(doc, page, chinese=False):
    for node in doc.select('.language-switch,link[hreflang]'):
        node.decompose()
    source = page.relative_to('zh') if chinese else page
    en = source.as_posix()
    zh = 'zh/'+en
    for lang, path in [('en',en),('zh',zh)]:
        url=BASE+('' if path=='index.html' else 'zh/' if path=='zh/index.html' else path)
        doc.head.append(doc.new_tag('link',rel='alternate',hreflang=lang,href=url))
    for parent in [doc.header,doc.footer]:
        nav=doc.new_tag('nav',attrs={'class':'language-switch','aria-label':'语言切换' if chinese else 'Language selection'})
        for lang,path in [('en',en),('zh',zh)]:
            a=doc.new_tag('a',href=relative(path,page),hreflang=lang,lang=lang,attrs={'data-language':lang})
            a.string=lang.upper()
            if (lang=='zh')==chinese:
                a['aria-current']='true'
            nav.append(a)
        if parent is doc.header:
            tools = doc.select_one('.header-tools')
            if tools is None:
                tools = doc.new_tag('div', attrs={'class':'header-tools'})
                search = doc.select_one('.header-search')
                search.wrap(tools)
            tools.append(nav)
        else:
            nav['class'] = ['wrap', 'language-switch']
            parent.append(nav)

def refresh_legacy_switches():
    # Historical previews use the maintained production language pair; assets stay local.
    def add(text, name):
        text=re.sub(r'<nav class="legacy-language-switch"[^>]*>.*?</nav>', '', text)
        en=BASE+('' if name=='index.html' else name)
        zh=BASE+('zh/' if name=='index.html' else 'zh/'+name)
        nav=f'<nav class="legacy-language-switch" aria-label="Language selection" style="display:flex;justify-content:flex-end;gap:16px;padding:12px"><a href="{en}" hreflang="en">EN</a><a href="{zh}" hreflang="zh">ZH</a></nav>'
        return text.replace('</header>',nav+'</header>').replace('</footer>',nav+'</footer>')
    for page in (ROOT/'preview/v5').rglob('*.html'):
        page.write_text(add(page.read_text(),page.relative_to(ROOT/'preview/v5').as_posix()))
    archive=ROOT/'releases/ropureoem-v5-preview.zip'
    with zipfile.ZipFile(archive) as z:
        entries=[(i,z.read(i.filename)) for i in z.infolist()]
    with zipfile.ZipFile(archive,'w') as z:
        for info,data in entries:
            if info.filename.endswith('.html'):data=add(data.decode(),info.filename).encode()
            z.writestr(info,data)

def generate():
    pages=sorted([*ROOT.glob('*.html'),*ROOT.glob('products/*.html')])
    missing=set()
    for source in pages:
        path=source.relative_to(ROOT)
        en=BeautifulSoup(source.read_text(),'html.parser')
        add_languages(en,path)
        source.write_text(str(en))
        zh=BeautifulSoup(str(en),'html.parser')
        zh.html['lang']='zh'
        # Chinese pages are for human review, excluded from search indexing.
        for node in zh.select('meta[name=robots]'):
            node.decompose()
        robots = zh.new_tag('meta', attrs={'name':'robots','content':'noindex, nofollow'})
        zh.head.insert(1, robots)
        for node in zh.find_all(string=True):
            if isinstance(node,Doctype) or node.parent.name in ['script','style'] or not node.strip():
                continue
            # Preserve all specification values and units; translate labels only.
            if node.find_parent('td'):
                node.replace_with(str(node).replace('Confirmed per order','按订单确认（Confirmed per order）'))
                continue
            translated=translate(str(node).strip())
            if translated==str(node).strip() and re.search(r'[A-Za-z]{3}',translated) and not re.fullmatch(r'(?:ROPureOEM|WhatsApp.*|info@ropureoem.com|SKU:.*|WT-.*|OEM / ODM|EN|ZH)',translated):
                missing.add(translated)
            node.replace_with(translated)
        if path.name.startswith('WT-'):
            zh.h1.string='产品型号：'+en.h1.get_text()
        target=Path('zh')/path
        for node in zh.select('[href],[src],[action]'):
            if node.has_attr('data-language') or node.get('rel')==['alternate']:
                continue
            for attr in ['href','src','action']:
                val=node.get(attr)
                if not val:continue
                u=urlsplit(val)
                if u.scheme or u.netloc or not u.path:continue
                resolved=posixpath.normpath(posixpath.join(str(path.parent),u.path))
                if resolved.endswith('.html'):resolved='zh/'+resolved
                node[attr]=urlunsplit(('', '', relative(resolved,target),u.query,u.fragment))
        for node in zh.select('[placeholder],[aria-label],img[alt]'):
            for attr in ['placeholder','aria-label','alt']:
                if node.has_attr(attr):node[attr]=translate(node[attr])
        canonical=BASE+('zh/' if path.name=='index.html' else 'zh/'+path.as_posix())
        zh.select_one('link[rel=canonical]')['href']=canonical
        for node in zh.select('meta[property="og:url"]'):node['content']=canonical
        for node in zh.select('meta[name=description],meta[property="og:description"],meta[property="og:title"]'):
            node['content']=zh.title.get_text() if node.get('property')=='og:title' else zh.title.get_text()+'。'+(zh.select_one('.lede') or zh.h1).get_text(' ',strip=True)
        def translated_data(value):
            if isinstance(value,dict):return {k:(canonical if k=='url' and isinstance(v,str) and v.startswith(BASE) else translated_data(v)) for k,v in value.items()}
            if isinstance(value,list):return [translated_data(v) for v in value]
            if isinstance(value,str) and not urlsplit(value).scheme:return translate(value)
            return value
        for node in zh.select('script[type="application/ld+json"]'):
            data=translated_data(json.loads(node.string))
            # Metadata follows the rendered Chinese document; image URLs stay English/shared.
            if data.get('@type')=='Organization':data['contactPoint']['availableLanguage']=['English','Chinese']
            node.string=json.dumps(data,ensure_ascii=False)
        add_languages(zh,target,True)
        dest=ROOT/target
        dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_text(str(zh))
    refresh_legacy_switches()
    print(f'Generated {len(pages)} Chinese pages; {len(pages)} English pairs with EN/ZH header/footer links and hreflang.')
    if missing:
        print('Untranslated copy requiring review:',json.dumps(sorted(missing),ensure_ascii=False))

if __name__=='__main__':generate()
