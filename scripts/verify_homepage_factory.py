"""Verify the EN/ZH homepage gallery over local HTTP on port 8766, including the ZIP preview tree."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright
Path('work').mkdir(exist_ok=True)
results=[]
with sync_playwright() as pw:
 b=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 page=b.new_page()
 errors=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.on('response',lambda r:errors.append(f'{r.status} {r.url}') if r.status>=400 else None)
 for base in ['http://127.0.0.1:8766/','http://127.0.0.1:8766/preview/v6/']:
  for width in [1280,1440]:
   page.set_viewport_size({'width':width,'height':1000})
   for path in ['index.html','zh/index.html']:
    assert page.goto(base+path).status==200
    gallery=page.locator('#factory-gallery')
    gallery.scroll_into_view_if_needed()
    imgs=gallery.locator('img')
    assert imgs.count()==3
    assert imgs.evaluate_all('async imgs=>{await Promise.all(imgs.map(i=>i.decode()));return imgs.every(i=>i.naturalWidth===1536&&i.naturalHeight===1024)}')
    assert gallery.is_visible()
    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
    boxes=[imgs.nth(i).bounding_box() for i in range(3)]
    assert max(b['y'] for b in boxes)-min(b['y'] for b in boxes)<1
    assert all(abs(b['width']/b['height']-1.5)<.01 for b in boxes)
    assert gallery.locator('.factory-disclosure').is_visible()
    title=page.title();h1=page.locator('h1').inner_text()
    results.append({'base':base,'path':path,'width':width,'title':title,'h1':h1,'images':boxes,'result':'PASS'})
    if base.endswith(':8766/') and width==1440:
     gallery.screenshot(path='work/factory-desktop-'+('zh' if path.startswith('zh/') else 'en')+'.png')
    # Verify actual paired navigation from the new section's homepage.
    language='en' if path.startswith('zh/') else 'zh'
    page.locator('header [data-language='+language+']').click()
    assert page.url==base+('index.html' if language=='en' else 'zh/index.html')
 assert not errors,errors
 b.close()
Path('work/factory-desktop-results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
print('PASS: 1280/1440px; EN/ZH and portable preview; three full-frame decoded images in one row; no overflow/JS/resource errors; actual header language switches.')
