"""Release checks. Run from repository root; --browser uses local port 8766."""
from pathlib import Path
from bs4 import BeautifulSoup as BS
import json,re,subprocess,hashlib,sys
from urllib.parse import urlsplit,unquote
root=Path('.');pages=list(root.glob('*.html'))+list(root.glob('products/*.html'))
assert len(pages)==75
models=list(root.glob('products/WT-*.html'));assert len(models)==62
baseline='ba76b9874196fe91b049f770090d516ad2adf5da'
def before(p):return subprocess.check_output(['git','show',baseline+':'+str(p)])
for p in list(Path('public/brand').glob('*'))+[Path('sitemap.xml'),Path('robots.txt'),Path('CNAME'),Path('.github/workflows/static.yml')]:assert p.read_bytes()==before(p),str(p)
for path in subprocess.check_output(['git','ls-tree','-r','--name-only',baseline,'preview/v5','releases/ropureoem-v5-preview.zip']).decode().splitlines():assert Path(path).read_bytes()==before(path),path
approved={e['output'] for e in json.loads(Path('docs/brand/product-image-audit.json').read_text())['images'] if e['status']=='pass'}
for p in pages:
 s=BS(p.read_text(),'html.parser');assert len(s.select('h1'))==1,str(p)
 assert s.select_one('.header-search input[name=q]') and s.select_one('.bottom-nav') and s.select_one('.footer-help')
 assert s.select_one('.help')['href']=='https://wa.me/8618928823858'
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
 assert not re.search(r'water\s*tech|watertechoem|\b(?:NSF|PFAS|BPA|ACS|WRAS|SGS|TUV|TÜV|EAC|RAVEN|WeChat)\b|tawk\.to|\bMOQ\s*[:：]?\s*\d|[$€£]\s*\d',text,re.I),str(p)
 if p in models:
  old=BS(before(p),'html.parser')
  assert [r.get_text(' ',strip=True) for r in s.select('.specs tr')]==[r.get_text(' ',strip=True) for r in old.select('.specs tr')],str(p)
  assert s.select_one('.lede').get_text()==old.select_one('.lede').get_text()
 elif str(p) not in ['index.html','products.html']:
  old=BS(before(p),'html.parser')
  # Existing non-home main paragraphs, headings and model descriptions remain.
  for n in old.main.select('p,h1,h2,h3,li,td,th'):
   t=n.get_text(' ',strip=True)
   if t and not n.find_parent('article'):
    assert t in s.main.get_text(' ',strip=True),(str(p),t)
assert len(BS(Path('products.html').read_text(),'html.parser').select('.card'))==62
print('PASS: 75 pages; 62 models; all spec rows retained; all local links/fragments; JSON-LD; images; prohibited terms; protected brand/Pages/v5 bytes.')
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
  go('index.html');assert not page.locator('.video-section').is_visible();page.screenshot(path='work/home-desktop.png',full_page=True)
  go('products/WT-T13.html');assert page.locator('.product-img').inner_text()=='Product image pending\nWT-T13';assert page.locator('.specs tr').count()==8
  go('products/WT-CT21.html');page.screenshot(path='work/product-desktop.png',full_page=True)
  for key,count in [('under-sink',17),('countertop',14),('softener',4),('shower',14),('faucet',13),('hot-cold-ice',14)]:
   go('products.html?range='+key);assert page.locator('.card:visible').count()==count,(key,page.locator('#result-count').inner_text())
  go('products.html?q=WT-T13');assert page.locator('.card:visible').count()==1
  go('products.html?q=Water+Softening');assert page.locator('.card:visible').count()==4
  go('products.html?q=zznomatch');assert page.locator('#empty-state').is_visible();assert page.locator('.card:visible').count()==0
  page.locator('.clear-filters').click();assert page.locator('.card:visible').count()==62
  page.locator('#q').fill('WT-CT21');assert page.locator('.card:visible').count()==1
  go('get-quote.html?model=WT-T13');assert page.locator('select[name=model]').input_value()=='WT-T13'
  # CDP observes the mailto navigation without sending email.
  from urllib.parse import parse_qs
  session=page.context.new_cdp_session(page);session.send('Page.enable');events=[]
  session.on('Page.frameRequestedNavigation',lambda e:events.append(e))
  page.locator('[name=name]').fill('Preview Tester');page.locator('[name=email]').fill('buyer@example.com');page.locator('[name=market]').fill('EU');page.locator('[name=message]').fill('Silver housing sample');page.locator('#quote-form button').click();page.wait_for_timeout(100)
  urls=[e['url'] for e in events if e['url'].startswith('mailto:')];assert urls
  u=urlsplit(urls[0]);mail=parse_qs(u.query);assert u.path=='info@ropureoem.com';assert 'WT-T13' in mail['subject'][0] and 'EU' in mail['subject'][0];assert 'Silver housing sample' in mail['body'][0]
  for width in [320,390,768,1024]:
   page.set_viewport_size({'width':width,'height':844});go('index.html')
   if width<700:
    assert page.locator('.bottom-nav').is_visible();assert page.locator('.category-grid').evaluate('(e)=>getComputedStyle(e).gridTemplateColumns.split(" ").length')==2
    assert page.locator('.featured').evaluate('(e)=>getComputedStyle(e).gridTemplateColumns.split(" ").length')==2
    assert page.locator('.video-section').is_visible();assert page.locator('video,iframe').count()==0
    page.locator('.bottom-nav a',has_text='Products').click();assert page.url.endswith('products.html')
    page.locator('.bottom-nav a',has_text='Get Quote').click();assert page.url.endswith('get-quote.html')
    page.locator('.bottom-nav a',has_text='Videos').click();assert page.url.endswith('index.html#videos')
    page.locator('.bottom-nav a',has_text='Contact').click();assert page.url.endswith('contact.html')
    go('index.html');page.locator('.nav-menu>summary').click();assert page.locator('.nav-menu nav').is_visible();page.keyboard.press('Escape');assert not page.locator('.nav-menu nav').is_visible()
    if width==390:page.screenshot(path='work/home-mobile.png',full_page=True)
   go('products/WT-T13.html');go('products/WT-CT21.html');go('products.html')
  # Shared header GET search from nested page.
  go('products/WT-T13.html');page.locator('#site-search').fill('WT-CT21');page.locator('.header-search button').click();assert page.locator('.card:visible').count()==1
  b.close()
 assert not failures,failures
 assert not requests,requests
 print('PASS: Chromium HTTP renders; 320/390/768/1024/1440px; six filters; SKU/category search; empty/clear; nested header search; quote prefill; bottom-nav destinations; menu/Escape; no console errors or HTTP failures.')
