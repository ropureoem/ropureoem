"""Verify the compact two-scene homepage gallery and warehouse photo on About."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright

Path('work').mkdir(exist_ok=True)
results=[]
with sync_playwright() as pw:
 browser=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 page=browser.new_page();errors=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.on('response',lambda r:errors.append(f'{r.status} {r.url}') if r.status>=400 else None)
 for base in ['http://127.0.0.1:8766/','http://127.0.0.1:8766/preview/v6/']:
  for width in [320,390,768,1280,1440]:
   page.set_viewport_size({'width':width,'height':900})
   for language in ['', 'zh/']:
    path=language+'index.html';assert page.goto(base+path).status==200
    gallery=page.locator('#factory-gallery');imgs=gallery.locator('img')
    assert imgs.count()==2
    assert imgs.evaluate_all('imgs=>imgs.map(i=>i.src.split("/").pop())')==['purifier-assembly.webp','container-loading.webp']
    assert imgs.evaluate_all('async imgs=>{await Promise.all(imgs.map(i=>i.decode()));return imgs.every(i=>i.naturalWidth===1536&&i.naturalHeight===1024)}')
    boxes=[imgs.nth(i).bounding_box() for i in range(2)]
    assert abs(boxes[0]['y']-boxes[1]['y'])<1
    assert all(abs(box['width']/box['height']-1.5)<.01 for box in boxes)
    assert max(box['height'] for box in boxes)<210
    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
    if width<700:
     assert gallery.bounding_box()['height']<240
     assert not gallery.locator('.section-heading').is_visible()
     assert not page.locator('.workspace-search').is_visible()
     assert not page.locator('.category-grid').is_visible()
     assert not page.locator('.home-certification').is_visible()
     assert not page.locator('#videos').is_visible()
     assert page.locator('.featured .card:visible').count()==4
     assert page.locator('.featured .confirmed-spec:visible,.featured .sku:visible,.featured .fine:visible').count()==0
     assert page.locator('.featured .card-actions a:visible').count()==4
     assert page.locator('.home-process li:visible').count()==3
     for core in ['.studio-hero','.home-featured','.home-process','.inquiry']:
      assert page.locator(core).is_visible(),core
     assert page.locator('.site-footer .language-switch').is_visible()
     # The simplified default page still reveals the original video target on demand.
     page.locator('.bottom-nav a').nth(3).click()
     assert page.url.endswith('index.html#videos') and page.locator('#videos').is_visible()
     assert page.goto(base+path).status==200
    else:
     assert page.locator('.workspace-search').is_visible()
     assert page.locator('.category-grid').is_visible()
     assert page.locator('.home-certification').is_visible()
     assert page.locator('.featured .confirmed-spec:visible').count()==4
     assert page.locator('.featured .card-actions a:visible').count()==8
    if base.endswith(':8766/') and width in [390,1440]:
     page.evaluate('window.scrollTo({top:Math.max(0,document.querySelector("#factory-gallery").getBoundingClientRect().top+scrollY-120),behavior:"instant"})')
     gallery.screenshot(path='work/factory-'+('mobile' if width==390 else 'desktop')+'-'+('zh' if language else 'en')+'.png')
     if width==390:
      # Full-page reading evidence omits fixed overlays only during the screenshot.
      page.screenshot(path='work/home-simple-mobile-'+('zh' if language else 'en')+'.png',full_page=True,style='.bottom-nav,.help-widget{visibility:hidden!important}')
    results.append({'base':base,'path':path,'width':width,'gallery_height':gallery.bounding_box()['height'],'images':boxes,'result':'PASS'})
    # Corresponding language switch remains intact.
    page.locator('header [data-language='+('en' if language else 'zh')+']').click()
    assert page.url==base+('index.html' if language else 'zh/index.html')
    assert page.goto(base+language+'about.html').status==200
    warehouse=page.locator('#factory-dispatch img');assert warehouse.count()==1
    assert warehouse.get_attribute('src').endswith('/warehouse-dispatch.webp')
    assert warehouse.evaluate('async i=>{await i.decode();return i.naturalWidth===1536&&i.naturalHeight===1024}')
    assert page.locator('#factory-dispatch .fine').is_visible()
    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
 assert not errors,errors
 browser.close()
Path('work/factory-layout-results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
print('PASS: 320/390/768/1280/1440px EN/ZH source and preview; exactly two distinct full-frame homepage scenes in one compact row; warehouse photo only on About; mobile core content simplified, video target and language switching work; desktop discovery/certification/full product cards remain; no overflow/JS/resource failures.')
