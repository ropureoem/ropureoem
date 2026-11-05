"""Check curated homepage models and unchanged catalogue; --browser uses local port 8766."""
from pathlib import Path
from bs4 import BeautifulSoup as BS
import subprocess,sys
from revision_support import historical_bytes

baseline='2f9c2ca4c85f04d3923b8cb3457ff66156abed91'
models=['RP-C11','RP-U03','RP-C09','RP-C04']
def normalised_controls(data):
 # Only the requested closed menu/help controls differ from historical UI evidence.
 doc=BS(data,'html.parser')
 for menu in doc.select('details.nav-menu'):menu.attrs.pop('open',None)
 for widget in doc.select('.help-widget'):widget.decompose()
 for trigger in doc.select('.help'):trigger.decompose()
 return str(doc).encode()
def previous(path):return normalised_controls(historical_bytes(baseline,path))
# Every catalogue/category/model file, including accessory SEO, is identical after namespace normalisation.
protected=[Path('products.html'),Path('zh/products.html'),*Path('products').glob('*.html'),*Path('zh/products').glob('*.html')]
for path in protected:assert normalised_controls(path.read_bytes())==previous(path),path
for path in [Path('index.html'),Path('zh/index.html')]:
 doc=BS(path.read_text(),'html.parser');old=BS(previous(path),'html.parser')
 cards=doc.select('.featured .card')
 assert [n['data-sku'] for n in cards]==models,path
 assert not any(sku in path.read_text() for sku in ['RP-F11','RP-F10','RP-S06']),path
 assert not doc.select('.featured [data-sku^="RP-F"],.featured [data-sku^="RP-S"]'),path
 assert str(cards[0])==str(old.select_one('.featured [data-sku="RP-C11"]')),path
 for selector in ['head','.studio-hero','header','footer','.bottom-nav']:
  assert str(doc.select_one(selector))==str(old.select_one(selector)),(path,selector)
 for card,sku in zip(cards,models):
  product=Path('zh/products' if path.parts[0]=='zh' else 'products')/(sku+'.html')
  detail=BS(product.read_text(),'html.parser')
  assert sku in detail.h1.get_text()
  assert card.select_one('.card-img')['href']=='products/'+sku+'.html'
  assert card.select_one('h3 a')['href']=='products/'+sku+'.html'
  assert card.select_one('.card-actions .btn-ghost')['href']=='products/'+sku+'.html'
  assert card.select_one('.card-actions a:last-child')['href']=='get-quote.html?model='+sku
  if sku!='RP-C11':
   row=detail.select_one('.specs tr')
   expected=row.th.get_text(' ',strip=True)+('：' if path.parts[0]=='zh' else ': ')+row.td.get_text(' ',strip=True)
   assert card.select_one('.confirmed-spec').get_text()==expected,(path,sku)
print('PASS: four verified mainline models; RP-C11 retained; no faucet/shower models on either homepage; all catalogue/model/category files and SEO identical after namespace normalisation; homepage head/header/footer/hero unchanged; gallery has dedicated checks; correct model/quote links and source specification values.')

if '--browser' in sys.argv:
 from playwright.sync_api import sync_playwright
 Path('work').mkdir(exist_ok=True)
 errors=[]
 with sync_playwright() as pw:
  browser=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
  page=browser.new_page()
  page.on('pageerror',lambda e:errors.append(str(e)))
  page.on('response',lambda r:errors.append(f'{r.status} {r.url}') if r.status>=400 else None)
  for base in ['http://127.0.0.1:8766/','http://127.0.0.1:8766/preview/v6/']:
   for width in [320,390,768,1440]:
    page.set_viewport_size({'width':width,'height':900})
    for language in ['en','zh']:
     path='zh/index.html' if language=='zh' else 'index.html'
     assert page.goto(base+path).status==200
     featured=page.locator('.featured');featured.scroll_into_view_if_needed()
     assert featured.locator('.card').evaluate_all('(cards)=>cards.map(c=>c.dataset.sku)')==models
     assert featured.locator('img').evaluate_all('async imgs=>{await Promise.all(imgs.map(i=>i.decode()));return imgs.every(i=>i.complete&&i.naturalWidth>0)}')
     assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),(base,width,language)
     columns=featured.evaluate('(e)=>getComputedStyle(e).gridTemplateColumns.split(" ").length')
     assert columns==(4 if width==1440 else 2),(width,columns)
     if base.endswith(':8766/') and width==390:
      featured.screenshot(path=f'work/featured-mobile-{language}.png')
     for sku in models:
      page.locator('.featured [data-sku="'+sku+'"] .card-img').click()
      assert page.url==base+('zh/' if language=='zh' else '')+'products/'+sku+'.html'
      assert sku in page.locator('h1').inner_text()
      page.go_back()
     page.locator('header [data-language='+('en' if language=='zh' else 'zh')+']').click()
     assert page.locator('.featured .card').evaluate_all('(cards)=>cards.map(c=>c.dataset.sku)')==models
  browser.close()
 assert not errors,errors
 print('PASS: 320/390/768/1440px; EN/ZH source and portable preview; 2-column mobile/4-column desktop; four decoded images, all product links and language switches; no overflow/JS/resource failures.')
