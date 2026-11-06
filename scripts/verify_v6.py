"""Release checks. Run from repository root; --browser uses local port 8766."""
from pathlib import Path
from bs4 import BeautifulSoup as BS
import json,re,subprocess,hashlib,sys
from urllib.parse import urlsplit,unquote
from revision_support import historical_bytes,current_name,current_bytes
root=Path('.');pages=list(root.glob('*.html'))+list(root.glob('products/*.html'))
assert len(pages)==75
models=list(root.glob('products/RP-*.html'));assert len(models)==62
baseline='ba76b9874196fe91b049f770090d516ad2adf5da'
def before(p):return historical_bytes(baseline,p)
for p in list(Path('public/brand').glob('*'))+[Path('robots.txt'),Path('CNAME'),Path('.github/workflows/static.yml')]:assert p.read_bytes()==before(p),str(p)
# Public v5 copy permits contact cleanup and links to maintained language pairs.
def clean_contact(data):
 text=data.decode()
 text=re.sub(r'Cheehwa Yan<br\s*/?>','',text)
 return text.replace('Cheehwa Yan, ','').replace('Cheehwa Yan','ROPureOEM').replace(' (placeholder — to be confirmed)','').encode()
def without_legacy_switches(data):
 if b'legacy-language-switch' not in data:return data
 return re.sub(rb'<nav class="legacy-language-switch"[^>]*>.*?</nav>',b'',data)
for path in subprocess.check_output(['git','ls-tree','-r','--name-only',baseline,'preview/v5']).decode().splitlines():
 path=current_name(path)
 original=before(path)
 assert without_legacy_switches(Path(path).read_bytes())==(clean_contact(original) if Path(path).suffix in ['.html','.txt','.md'] else original),path
import io,zipfile
with zipfile.ZipFile(io.BytesIO(before('releases/ropureoem-v5-preview.zip'))) as oldzip, zipfile.ZipFile('releases/ropureoem-v5-preview.zip') as current:
 assert [current_name(n) for n in oldzip.namelist()]==current.namelist()
 for name in oldzip.namelist():
  original=current_bytes(oldzip.read(name),name)
  name=current_name(name)
  assert without_legacy_switches(current.read(name))==(clean_contact(original) if Path(name).suffix in ['.html','.txt','.md'] else original),name
approved={e['output'] for e in json.loads(Path('docs/brand/product-image-audit.json').read_text())['images'] if e['status']=='pass'}
factory_audit=json.loads(Path('docs/brand/homepage-factory-image-audit.json').read_text())
factory_images={e['output'] for e in factory_audit['images']}
assert len(factory_images)==3 and all(e['status']=='pass' for e in factory_audit['images'])
for entry in factory_audit['images']:
 assert hashlib.sha256(Path(entry['output']).read_bytes()).hexdigest()==entry['sha256']
 assert entry['dimensions']==[1536,1024]
approved|=factory_images
home=BS(Path('index.html').read_text(),'html.parser')
home_factory={e['output'] for e in factory_audit['images'] if e['placement']=='index.html#factory-gallery'}
about_factory={e['output'] for e in factory_audit['images'] if e['placement']=='about.html#factory-dispatch'}
assert len(home_factory)==2 and len(about_factory)==1 and home_factory.isdisjoint(about_factory)
assert home_factory|about_factory==factory_images
assert {img['src'] for img in home.select('#factory-gallery img')}==home_factory
assert {img['src'] for img in BS(Path('about.html').read_text(),'html.parser').select('#factory-dispatch img')}==about_factory
assert 'AI-generated' not in Path('index.html').read_text() and 'AI 生成' not in Path('index.html').read_text()
assert home.select_one('.studio-hero').find_next_sibling('section')['id']=='factory-gallery'
assert [n['data-sku'] for n in home.select('.featured .card')]==['RP-C11','RP-U03','RP-C09','RP-C04']

for p in pages:
 s=BS(p.read_text(),'html.parser');assert len(s.select('h1'))==1,str(p)
 assert s.select_one('.header-search input[name=q]') and s.select_one('.bottom-nav') and s.select_one('.footer-help')
 assert s.select_one('details.help-widget > summary.help')
 assert s.select_one('.help-panel [data-contact=whatsapp]')['href']=='https://wa.me/8618928823858'
 assert (p.parent/urlsplit(s.select_one('.help-panel [data-contact=email]')['href']).path).resolve()==Path('get-quote.html').resolve()
 assert len(s.select('.help-panel a'))==2
 for n in s.select('[href], [src], [action]'):
  for attr in ['href','src','action']:
   val=n.get(attr)
   if not val:continue
   u=urlsplit(val)
   if u.scheme or u.netloc:continue
   target=p.parent/unquote(u.path) if u.path else p
   assert target.exists(),(str(p),val)
   if u.fragment and target.suffix=='.html':assert BS(target.read_text(),'html.parser').find(id=unquote(u.fragment)),(str(p),val)
 for img in s.select('img'):
  src=(p.parent/img['src']).resolve();assert 'public/brand' in str(src) or str(src.relative_to(Path.cwd())) in approved,(p,img)
 for ld in s.select('script[type="application/ld+json"]'):
  d=json.loads(ld.string)
  if 'image' in d:assert d['image'].replace('https://ropureoem.com/','') in approved
 # Word boundaries avoid false positives in e.g. REACH and specifications.
 text=s.get_text(' ',strip=True)+' '+str(s.select('script'))
 assert not re.search(r'water\s*tech|\b(?:NSF|PFAS|BPA|ACS|WRAS|SGS|TUV|TÜV|EAC|RAVEN|W[e]Chat)\b|tawk\.to|\bMOQ\s*[:：]?\s*\d|[$€£]\s*\d',text,re.I),str(p)
 if p in models:
  old=BS(clean_contact(before(p)),'html.parser')
  assert [r.get_text(' ',strip=True) for r in s.select('.specs tr')]==[r.get_text(' ',strip=True) for r in old.select('.specs tr')],str(p)
  assert s.select_one('.lede').get_text()==old.select_one('.lede').get_text()
 elif str(p) not in ['index.html','products.html','contact.html']:
  old=BS(clean_contact(before(p)),'html.parser')
  # Existing non-home main paragraphs, headings and model descriptions remain.
  for n in old.main.select('p,h1,h2,h3,li,td,th'):
   t=n.get_text(' ',strip=True)
   if str(p)=='about.html':t=t.replace('water purifier OEM / ODM supplier','water purifier OEM / ODM manufacturer')
   if t and not n.find_parent('article') and not (str(p)=='products/countertop.html' and n.name=='h1'):
    assert t in s.main.get_text(' ',strip=True),(str(p),t)
assert len(BS(Path('products.html').read_text(),'html.parser').select('.card'))==62
print('PASS: 75 pages; 62 models; all spec rows retained; all local links/fragments; JSON-LD; images; prohibited terms; protected brand/Pages/v5 image bytes.')
# Per-model provenance, output hashes, pending allowlist and immutable v6 content.
from PIL import Image
import zipfile,posixpath
entries=json.loads(Path('docs/brand/product-image-audit.json').read_text())['images']
by_sku={e['sku']:e for e in entries};assert len(by_sku)==62
v6_baseline='b0fd0d3d4ccf5a1601d23341e64b5017a0994f8c'
with zipfile.ZipFile('releases/ropureoem-v5-preview.zip') as v5zip:
 for e in entries:
  sku=e['sku'];page='products/'+sku+'.html'
  for v in e['v5_evidence']:
   if v['kind']=='commit':
    html=before(Path(page));data=before(Path(v['path']))
   elif v['kind']=='zip':html=v5zip.read(page);data=v5zip.read(v['path'])
   else:html=Path('preview/v5',page).read_bytes();data=Path('preview/v5',v['path']).read_bytes()
   assert hashlib.sha256(historical_bytes(baseline,page,raw=True)).hexdigest()==v['page_sha256']
   assert without_legacy_switches(html) in [before(Path(page)),clean_contact(before(Path(page)))]
   ref=BS(html,'html.parser').select_one('.product-img img')['src']
   assert ref==v['reference'] and posixpath.normpath(posixpath.join('products',ref))==e['source']
   assert hashlib.sha256(data).hexdigest()==e['source_sha256']==v['sha256']
  assert hashlib.sha256(Path(e['source']).read_bytes()).hexdigest()==e['source_sha256']
  s=BS(Path(page).read_text(),'html.parser')
  if e['status']=='pass':
   assert hashlib.sha256(Path(e['output']).read_bytes()).hexdigest()==e['output_sha256']
   assert list(Image.open(e['output']).size)==e['dimensions']
   assert s.select_one('.product-img img')['src']=='../'+e['output']
  else:assert s.select_one('.product-img .image-pending span').text==sku and e['reason']
  if sku in ['RP-C11','RP-S06','RP-F10','RP-F11']:
   assert Path(e['output']).read_bytes()==historical_bytes(v6_baseline,e['output'])
# SEO/contact changes must leave images, placeholders, model specs and layout intact.
image_baseline='c8d5ab654ec030f2eb08113ec90245818d1cc4d4'
for p in pages:
 s=BS(p.read_text(),'html.parser')
 old=BS(historical_bytes(image_baseline,p),'html.parser')
 for selector in ['img','.image-pending','.specs','.card','.product-img']:
  # Homepage additions and curated mainline cards have dedicated checks; other imagery/cards stay identical.
  def retained(doc):
   return [str(n) for n in doc.select(selector) if not (
    (str(p)=='index.html' and (
     (selector=='img' and n.find_parent(id='factory-gallery')) or
     (selector in ['img','.card'] and n.find_parent(class_='featured')))) or
    (str(p)=='about.html' and selector=='img' and n.find_parent(id='factory-dispatch')))]
  assert retained(s)==retained(old),(p,selector)
 assert 'Cheehwa Yan' not in p.read_text()
 assert not s.select('.languages,[aria-label="Languages"]')
 assert not [n for n in s.select('header button,footer button,header a,footer a') if n.get_text(strip=True) in ['RU','KK']]
 for ld in s.select('script[type="application/ld+json"]'):json.loads(ld.string)
# Every source/product image and image audit remains identical to latest main.
for path in subprocess.check_output(['git','ls-tree','-r','--name-only',image_baseline,'assets','public','docs/brand/product-image-audit.json','docs/brand/product-image-audit.md']).decode().splitlines():
 path=current_name(path)
 assert Path(path).read_bytes()==historical_bytes(image_baseline,path),path
# English SEO must remain identical to main before the review-only Chinese policy.
seo_baseline='2571a9905dd34c9389ce238d52c2f3269cf4ef01'
for p in pages:
 current=BS(p.read_text(),'html.parser')
 previous=BS(historical_bytes(seo_baseline,p),'html.parser')
 for selector in ['title','h1','meta[name=description]','meta[name=keywords]','link[hreflang]','link[rel=canonical]']:
  assert [str(n) for n in current.select(selector)]==[str(n) for n in previous.select(selector)],(p,selector)
 assert not current.select('meta[name=robots]'),p
print('PASS: all 75 English titles/H1/descriptions/keywords/hreflang/canonical unchanged.')
import xml.etree.ElementTree as ET
urls=[n.text for n in ET.parse('sitemap.xml').findall('{*}url/{*}loc')]
expected={'https://ropureoem.com/'+('' if p.name=='index.html' else str(p)) for p in pages}
assert len(urls)==75 and len(set(urls))==75 and set(urls)==expected
keywords={
 'index.html':['oem water purifier manufacturer','oem water filter manufacturer'],
 'oem-odm.html':['oem water filter manufacturer','ultra high purity purifier','water purifier parts','water purification parts','water filter components','industrial reverse osmosis hot water'],
 'products/countertop.html':['hot and cold water purifier'],
 'products.html':['portable water purifier market'],
}
for path,phrases in keywords.items():
 html=Path(path).read_text().lower()
 for phrase in phrases:assert phrase in html,(path,phrase)
assert 'oem water purifier manufacturer' in BS(Path('index.html').read_text(),'html.parser').h1.get_text().lower()
with zipfile.ZipFile('releases/ropureoem-v6-preview.zip') as z:
 assert z.testzip() is None
 assert sum(n.endswith('.html') for n in z.namelist())==150
 for n in z.namelist():assert z.read(n)==Path('preview/v6',n).read_bytes()
print('PASS: v5 three-source provenance; 45 photo/17 justified pending; SHA-256/dimensions; protected four outputs; unchanged v6 images/specs; SEO/contact cleanup; 75 English sitemap URLs (0 ZH); ZIP bytes/integrity.')

if '--browser' in sys.argv:
 from playwright.sync_api import sync_playwright
 failures=[];requests=[]
 with sync_playwright() as pw:
  b=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox']);page=b.new_page(viewport={'width':1440,'height':1000})
  page.on('pageerror',lambda e:failures.append(str(e)))
  page.on('response',lambda r:requests.append(r.url) if r.status>=400 else None)
  base='http://127.0.0.1:8766/'+('preview/v6/' if '--preview' in sys.argv else '')
  def go(url):
   response=page.goto(base+url);assert response.status==200
   assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),url
   assert page.locator('img').evaluate_all('async (imgs)=>{await Promise.all(imgs.map(i=>{i.loading="eager";return i.decode().catch(()=>{});}));return imgs.every(i=>i.complete&&i.naturalWidth>0);}'),url
   if url=='index.html':
    assert page.locator('#factory-gallery img').count()==2
    assert page.locator('#factory-gallery').is_visible()
    assert page.locator('#factory-gallery img').evaluate_all('(imgs)=>imgs.every(i=>i.naturalWidth===1536 && i.naturalHeight===1024 && getComputedStyle(i).objectFit==="contain")')
    columns=page.locator('.factory-gallery').evaluate('(e)=>getComputedStyle(e).gridTemplateColumns.split(" ").length')
    assert columns==2,columns
  go('index.html');assert page.locator('.video-section').is_visible();page.screenshot(path='work/home-desktop.png',full_page=True)
  go('products/RP-F02.html');assert page.locator('.product-img img').get_attribute('src')=='../assets/products/RP-F02.png';assert page.locator('.specs tr').count()==8
  go('products/RP-C11.html');page.screenshot(path='work/product-desktop.png',full_page=True)
  for key,count in [('under-sink',17),('countertop',14),('softener',4),('shower',14),('faucet',13),('hot-cold-ice',14)]:
   go('products.html?range='+key);assert page.locator('.card:visible').count()==count,(key,page.locator('#result-count').inner_text())
  go('products.html?q=RP-F02');assert page.locator('.card:visible').count()==1
  go('products.html?q=Water+Softening');assert page.locator('.card:visible').count()==4
  go('products.html?q=zznomatch');assert page.locator('#empty-state').is_visible();assert page.locator('.card:visible').count()==0
  page.locator('.clear-filters').click();assert page.locator('.card:visible').count()==62
  page.locator('#q').fill('RP-C11');assert page.locator('.card:visible').count()==1
  go('get-quote.html?model=RP-F02');assert page.locator('select[name=model]').input_value()=='RP-F02'
  # CDP observes the mailto navigation without sending email.
  from urllib.parse import parse_qs
  session=page.context.new_cdp_session(page);session.send('Page.enable');events=[]
  session.on('Page.frameRequestedNavigation',lambda e:events.append(e))
  page.locator('[name=name]').fill('Preview Tester');page.locator('[name=email]').fill('buyer@example.com');page.locator('[name=market]').fill('EU');page.locator('[name=message]').fill('Silver housing sample');page.locator('#quote-form button').click();page.wait_for_timeout(100)
  urls=[e['url'] for e in events if e['url'].startswith('mailto:')];assert urls
  u=urlsplit(urls[0]);mail=parse_qs(u.query);assert u.path=='info@ropureoem.com';assert 'RP-F02' in mail['subject'][0] and 'EU' in mail['subject'][0];assert 'Silver housing sample' in mail['body'][0]
  for width in [320,390,768,1024]:
   page.set_viewport_size({'width':width,'height':844});go('index.html')
   if width<700:
    assert page.locator('.bottom-nav').is_visible();assert not page.locator('.category-grid').is_visible()
    assert page.locator('.featured').evaluate('(e)=>getComputedStyle(e).gridTemplateColumns.split(" ").length')==2
    assert not page.locator('.video-section').is_visible();assert page.locator('#videos video[controls][preload=metadata]').count()==1;assert page.locator('iframe,video[autoplay]').count()==0
    page.locator('.bottom-nav a',has_text='Products').click();assert page.url.endswith('products.html')
    page.locator('.bottom-nav a',has_text='Get Quote').click();assert page.url.endswith('get-quote.html')
    page.locator('.bottom-nav a',has_text='Videos').click();assert page.url.endswith('index.html#videos');assert page.locator('#videos').is_visible()
    page.locator('.bottom-nav a',has_text='Contact').click();assert page.url.endswith('contact.html')
    go('index.html');page.locator('.nav-menu>summary').click();assert page.locator('.nav-menu nav').is_visible();page.keyboard.press('Escape');assert not page.locator('.nav-menu nav').is_visible()
    if width==390:page.screenshot(path='work/home-mobile.png',full_page=True)
   go('products/RP-F02.html');go('products/RP-C11.html');go('products.html')
  # Shared header GET search from nested page.
  go('products/RP-F02.html');page.locator('#site-search').fill('RP-C11');page.locator('.header-search button').click();assert page.locator('.card:visible').count()==1
  b.close()
 assert not failures,failures
 assert not requests,requests
 print('PASS: Chromium HTTP renders; 320/390/768/1024/1440px; six filters; SKU/category search; empty/clear; nested header search; quote prefill; bottom-nav destinations; menu/Escape; no console errors or HTTP failures.')
