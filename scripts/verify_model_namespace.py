"""Validate the final 62-model namespace, public text/paths and downloadable archives.

Run from repository root. --browser checks local HTTP on port 8766. Immutable
Git history and ignored developer scratch are outside the published-site scope.
"""
from pathlib import Path
import json,re,sys,zipfile
from bs4 import BeautifulSoup as BS
from revision_support import historical_bytes,revision_paths

root=Path('.')
expected={f'RP-{letter}{index:02d}' for letter,count in [('C',14),('U',18),('F',13),('S',14),('W',3)] for index in range(1,count+1)}
forbidden=bytes((87,84,45))
obsolete=re.compile(rb'(?<![A-Za-z0-9])(?:CT|UR|SH|WS|T)[0-9]{2}\b|\bRP-[0-9]{4}\b')
issues=[];text_count=0;archive_count=0

def inspect(name,data):
 global text_count
 if forbidden in name.encode() or obsolete.search(name.encode()):issues.append(('path',name))
 try:text=data.decode('utf-8')
 except UnicodeDecodeError:return
 text_count+=1
 if forbidden in data or obsolete.search(data):issues.append(('content',name))
 for model in re.findall(r'\bRP-[A-Z]*[0-9]+\b',text):
  if model not in expected:issues.append(('unknown model',name,model))

for path in root.rglob('*'):
 if not path.is_file() or any(part in ['.git','work','__pycache__'] for part in path.parts):continue
 inspect(str(path),path.read_bytes())
 if path.suffix=='.zip':
  with zipfile.ZipFile(path) as archive:
   assert archive.testzip() is None,path
   for name in archive.namelist():
    if not name.endswith('/'):inspect(str(path)+'!'+name,archive.read(name));archive_count+=1
assert not issues,issues
for prefix in ['', 'zh/', 'preview/v5/', 'preview/v6/', 'preview/v6/zh/']:
 models={p.stem for p in Path(prefix+'products').glob('RP-*.html')}
 assert models==expected,(prefix,models^expected)
for prefix in ['', 'zh/', 'preview/v6/', 'preview/v6/zh/']:
 catalogue=BS(Path(prefix+'products.html').read_text(),'html.parser')
 assert {n['data-sku'] for n in catalogue.select('.card')}==expected,prefix
 quote=BS(Path(prefix+'get-quote.html').read_text(),'html.parser')
 assert {n['value'] for n in quote.select('[name=model] option') if n.get('value','').startswith('RP-')}==expected,prefix
# Independently prove all parameter rows and English SEO copy survive the migration.
revision='7faf36a35fc7b564f6e8c5d63ec2f0463198aee2'
rows=0
for p in sorted(Path('products').glob('RP-*.html')):
 doc=BS(p.read_text(),'html.parser');old=BS(historical_bytes(revision,p),'html.parser')
 assert [str(n) for n in doc.select('.specs tr')]==[str(n) for n in old.select('.specs tr')],p
 rows+=len(doc.select('.specs tr'))
 assert doc.h1.get_text()==p.stem,p
 assert doc.select_one('link[rel=canonical]')['href']=='https://ropureoem.com/'+str(p),p
 for selector in ['title','h1','meta[name=description]','meta[name=keywords]','link[hreflang]','link[rel=canonical]']:
  assert [str(n) for n in doc.select(selector)]==[str(n) for n in old.select(selector)],(p,selector)
assert rows==462,rows
import xml.etree.ElementTree as ET
urls=[n.text for n in ET.parse('sitemap.xml').findall('{*}url/{*}loc')]
assert len(urls)==len(set(urls))==75 and not any('/zh/' in u for u in urls)
assert {u.rsplit('/',1)[-1][:-5] for u in urls if '/products/RP-' in u}==expected
assert not [p for p in root.rglob('*.csv') if not any(part in ['.git','work','__pycache__'] for part in p.parts)], 'Internal CSV must never enter the published repository'
print(f'PASS: 62 models in C14/U18/F13/S14/W3; 462 parameter rows unchanged; final metadata/canonical/hreflang; search cards and quote options; sitemap 75 EN / 0 ZH; 0 obsolete identifiers/paths across {text_count} UTF-8 files and {archive_count} archive entries; no CSV published.')

if '--browser' in sys.argv:
 from playwright.sync_api import sync_playwright
 with sync_playwright() as pw:
  browser=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
  page=browser.new_page(viewport={'width':390,'height':900})
  base='http://127.0.0.1:8766/'
  samples=['RP-C11','RP-U02','RP-F11','RP-S06','RP-W01']
  history=revision_paths(revision)
  for model in samples:
   for language in ['', 'zh/']:
    path=language+'products/'+model+'.html'
    assert page.goto(base+path).status==200,path
    assert model in page.locator('h1').inner_text(),path
    if language:assert page.locator('meta[name=robots]').get_attribute('content')=='noindex, nofollow'
    old_path=history[path]
    response=page.request.get(base+old_path)
    assert response.status==404,(old_path,response.status)
    assert forbidden.decode() not in response.text(),old_path
   assert page.goto(base+'products.html?q='+model).status==200
   assert page.locator('.card:visible').count()==1,model
   assert page.locator('.card:visible').get_attribute('data-sku')==model
   page.goto(base+'get-quote.html?model='+model)
   assert page.locator('[name=model]').input_value()==model
   page.locator('header [data-language=zh]').click()
   assert page.locator('[name=model]').input_value()==model
  # No historical product route remains anywhere in either current language tree.
  for model in sorted(expected):
   for prefix in ['', 'zh/']:
    assert not Path(history[prefix+'products/'+model+'.html']).exists()
  page.goto(base+'products/RP-C11.html')
  assert page.title()==BS(Path('products/RP-C11.html').read_text(),'html.parser').title.get_text()
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
  browser.close()
 print('PASS: five-category RP pages 200; corresponding former routes 404 without retired identifiers; all 124 old product files absent; RP search results and quote prefill/EN-ZH switching on 390px local HTTP.')
