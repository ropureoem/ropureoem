"""Validate real bilingual pages, all numeric specs, asset reuse and same-page navigation."""
from pathlib import Path
from urllib.parse import urlsplit, unquote
from bs4 import BeautifulSoup as BS
import json, re, sys, xml.etree.ElementTree as ET

root=Path('.').resolve()
english=sorted([*Path('.').glob('*.html'),*Path('products').glob('*.html')])
chinese=sorted(Path('zh').rglob('*.html'))
assert len(english)==len(chinese)==75

def url(p):return 'https://ropureoem.com/'+('' if str(p)=='index.html' else 'zh/' if str(p)=='zh/index.html' else str(p))
def resolve(p,href):return (root/p.parent/unquote(urlsplit(href).path)).resolve()

for p in english:
 z=Path('zh')/p
 en=BS(p.read_text(),'html.parser');zh=BS(z.read_text(),'html.parser')
 assert en.html['lang']=='en' and zh.html['lang']=='zh'
 assert not en.select('meta[name=robots]'),p
 robots=zh.select('head meta[name=robots]')
 assert len(robots)==1 and robots[0]['content']=='noindex, nofollow',z
 assert en.select_one('.header-tools > .language-switch') and zh.select_one('.header-tools > .language-switch')
 assert re.search('[\u4e00-\u9fff]',zh.h1.get_text()),z
 assert re.search('[\u4e00-\u9fff]',zh.title.get_text()),z
 assert len(zh.select('h1'))==1
 for page,doc in [(p,en),(z,zh)]:
  assert doc.select_one('link[rel=canonical]')['href']==url(page)
  assert {n['hreflang']:n['href'] for n in doc.select('link[hreflang]')}=={'en':url(p),'zh':url(z)},page
  for area in ['header','footer']:
   links=doc.select(area+' .language-switch a')
   assert [a.get_text(strip=True) for a in links]==['EN','ZH'],page
   assert [resolve(page,a['href']) for a in links]==[(root/p).resolve(),(root/z).resolve()],page
  assert not re.search('Cheehwa Yan|>RU<|>KK<',str(doc))
  for node in doc.select('[href],[src],[action]'):
   for attr in ['href','src','action']:
    val=node.get(attr,'');u=urlsplit(val)
    if not val or u.scheme or u.netloc:continue
    target=resolve(page,val) if u.path else root/page
    assert target.exists(),(page,val)
    if u.fragment and target.suffix=='.html':assert BS(target.read_text(),'html.parser').find(id=unquote(u.fragment)),(page,val)
  for node in doc.select('script[type="application/ld+json"]'):json.loads(node.string)
 assert [resolve(p,n['src']) for n in en.select('img')]==[resolve(z,n['src']) for n in zh.select('img')],p
 # Numeric specs and every value/unit are copied rather than converted.
 en_values=[n.get_text(' ',strip=True) for n in en.select('.specs td')]
 zh_values=[n.get_text(' ',strip=True).replace('按订单确认（Confirmed per order）','Confirmed per order') for n in zh.select('.specs td')]
 assert en_values==zh_values,p
 labels=zh.select('.specs th')
 assert all(re.search('[\u4e00-\u9fff]',n.get_text()) for n in labels),p
 assert re.findall(r'\d+(?:[.,]\d+)*',en.select_one('.lede').get_text() if en.select_one('.lede') else '')==re.findall(r'\d+(?:[.,]\d+)*',zh.select_one('.lede').get_text() if zh.select_one('.lede') else ''),p
 assert [n.get_text() for n in en.select('[name=model] option') if n.get('value') not in ['',None]]!=[] or p.name!='get-quote.html'
 if p.name=='get-quote.html':
  assert [n.get('value') for n in en.select('[name=model] option')]==[n.get('value') for n in zh.select('[name=model] option')]
 if p.name.startswith('RP-'):
  assert re.search('[\u4e00-\u9fff]',zh.select_one('.lede').get_text())
  assert re.findall('RP-[A-Z0-9]+',en.h1.get_text())==re.findall('RP-[A-Z0-9]+',zh.h1.get_text())
urls=[n.text for n in ET.parse('sitemap.xml').findall('{*}url/{*}loc')]
assert len(urls)==len(set(urls))==75 and set(urls)=={url(p) for p in english}
print('PASS: 75 EN sitemap URLs, 0 ZH; noindex 75/75 ZH, 0/75 EN; all reciprocal header/footer switches/hreflang/canonicals; Chinese titles/headings/spec labels; identical specification values, models, units and image sources; all links/fragments.')

if '--browser' in sys.argv:
 from playwright.sync_api import sync_playwright
 base='http://127.0.0.1:8766/'+('preview/v6/' if '--preview' in sys.argv else '')
 errors=[]
 with sync_playwright() as pw:
  browser=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
  page=browser.new_page(viewport={'width':1440,'height':1000})
  page.on('pageerror',lambda e:errors.append(str(e)))
  page.on('response',lambda r:errors.append(str(r.status)+' '+r.url) if r.status>=400 else None)
  def check_header(page):
   boxes=[page.locator(selector).bounding_box() for selector in ['.header-search','.header-tools > .language-switch']]
   search,switch=boxes
   assert abs(search['y']+search['height']/2-switch['y']-switch['height']/2)<2,boxes
   assert switch['x']>=search['x']+search['width'],boxes
   if page.viewport_size['width']>=700:assert search['width']<=191,boxes
   assert page.locator('.header-tools > .language-switch a').evaluate_all('(links)=>links.every(a=>getComputedStyle(a).backgroundColor==="rgba(0, 0, 0, 0)" && a.getBoundingClientRect().height<=32)')
   if page.viewport_size['width']<700:
    tools=page.locator('.header-tools').bounding_box()
    assert abs(search['x']-tools['x'])<1,boxes
    assert abs(switch['x']+switch['width']-tools['x']-tools['width'])<1,boxes
    assert search['width']>190,boxes
    logo=page.locator('.header-in > .logo').bounding_box()
    quote=page.locator('.header-in > .quote').bounding_box()
    assert abs(logo['y']+logo['height']/2-quote['y']-quote['height']/2)<2
    assert search['y']>=quote['y']+quote['height']
  for width in [320,390,699,700,768,1024,1100,1199,1200,1440]:
   page.set_viewport_size({'width':width,'height':900})
   for path in ['index.html','products/RP-F02.html','contact.html']:
    assert page.goto(base+path).status==200
    check_header(page)
    page.locator('header [data-language=zh]').click()
    assert page.url==base+'zh/'+path
    assert page.locator('html').get_attribute('lang')=='zh'
    check_header(page)
    assert re.search('[\u4e00-\u9fff]',page.locator('h1').inner_text())
    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),(width,path)
    page.locator('footer [data-language=en]').click()
    assert page.url==base+path
    assert page.locator('html').get_attribute('lang')=='en'
   page.goto(base+'zh/products.html?range=hot-cold-ice')
   assert page.locator('.card:visible').count()==14
   assert '14 款型号' in page.locator('#result-count').inner_text()
   page.locator('#q').fill('龙头')
   page.locator('[name=range]').select_option('faucet')
   assert page.locator('.card:visible').count()==13
   page.locator('header [data-language=en]').click()
   assert 'q=' in page.url and page.locator('.card:visible').count()==0 # Chinese search is preserved, English text has no Chinese match.
   page.goto(base+'zh/get-quote.html?model=RP-F02')
   assert page.locator('[name=model]').input_value()=='RP-F02'
   page.locator('header [data-language=en]').click()
   assert page.locator('[name=model]').input_value()=='RP-F02'
  page.goto(base+'zh/index.html');page.screenshot(path='work/zh-home.png',full_page=True)
  browser.close()
 assert not errors,errors
 print('PASS: Chromium EN↔ZH same-page navigation (home/product/contact), 320–1440px; full-width mobile search + right-aligned inline EN/ZH on the same row; Chinese content; Chinese range/search/count; language-switch query and quote-model preservation; no JS/resource errors.')
