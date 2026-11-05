"""Check curated homepage models and unchanged catalogue; --browser uses local port 8766."""
from pathlib import Path
from bs4 import BeautifulSoup as BS
import subprocess,sys

baseline='2f9c2ca4c85f04d3923b8cb3457ff66156abed91'
models=['WT-CT21','WT-UR04','WT-CT19','WT-CT09']
def previous(path):return subprocess.check_output(['git','show',baseline+':'+str(path)])
# Every catalogue/category/model file, including accessory SEO, is byte-identical.
protected=[Path('products.html'),Path('zh/products.html'),*Path('products').glob('*.html'),*Path('zh/products').glob('*.html')]
for path in protected:assert path.read_bytes()==previous(path),path
for path in [Path('index.html'),Path('zh/index.html')]:
 doc=BS(path.read_text(),'html.parser');old=BS(previous(path),'html.parser')
 cards=doc.select('.featured .card')
 assert [n['data-sku'] for n in cards]==models,path
 assert not any(sku in path.read_text() for sku in ['WT-T27','WT-T25','WT-SH14']),path
 assert not doc.select('.featured [data-sku^="WT-T"],.featured [data-sku^="WT-SH"]'),path
 assert str(cards[0])==str(old.select_one('.featured [data-sku="WT-CT21"]')),path
 for selector in ['head','.studio-hero','#factory-gallery','header','footer','.bottom-nav']:
  assert str(doc.select_one(selector))==str(old.select_one(selector)),(path,selector)
 for card,sku in zip(cards,models):
  product=Path('zh/products' if path.parts[0]=='zh' else 'products')/(sku+'.html')
  detail=BS(product.read_text(),'html.parser')
  assert sku in detail.h1.get_text()
  assert card.select_one('.card-img')['href']=='products/'+sku+'.html'
  assert card.select_one('h3 a')['href']=='products/'+sku+'.html'
  assert card.select_one('.card-actions .btn-ghost')['href']=='products/'+sku+'.html'
  assert card.select_one('.card-actions a:last-child')['href']=='get-quote.html?model='+sku
  if sku!='WT-CT21':
   row=detail.select_one('.specs tr')
   expected=row.th.get_text(' ',strip=True)+('：' if path.parts[0]=='zh' else ': ')+row.td.get_text(' ',strip=True)
   assert card.select_one('.confirmed-spec').get_text()==expected,(path,sku)
print('PASS: four verified mainline models; CT21 retained; no faucet/shower models on either homepage; all catalogue/model/category files and SEO byte-identical; homepage head/header/footer/hero/gallery unchanged; correct model/quote links and source specification values.')

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
