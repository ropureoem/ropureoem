"""Verify the two-choice help disclosure on all EN/ZH pages and local HTTP."""
from pathlib import Path
from urllib.parse import urlsplit
from bs4 import BeautifulSoup as BS
from playwright.sync_api import sync_playwright
import json,zipfile

for prefix in ['', 'preview/v6/']:
 pages=[*Path(prefix or '.').glob('*.html'),*Path(prefix+'products').glob('*.html'),*Path(prefix+'zh').rglob('*.html')]
 assert len(pages)==150
 for path in pages:
  doc=BS(path.read_text(),'html.parser')
  widgets=doc.select('details.help-widget');assert len(widgets)==1,path
  widget=widgets[0];assert not widget.has_attr('open'),path
  assert widget.select_one('summary.help') and not widget.select_one('summary.help').has_attr('href'),path
  assert len(widget.select('a'))==2,path
  assert widget.select_one('[data-contact=whatsapp]')['href']=='https://wa.me/8618928823858',path
  email=widget.select_one('[data-contact=email]')
  target=(path.parent/urlsplit(email['href']).path).resolve()
  expected=Path(prefix+('zh/' if doc.html['lang']=='zh' else '')+'get-quote.html').resolve()
  assert target==expected and 'info@ropureoem.com' in email.get_text(),path
with zipfile.ZipFile('releases/ropureoem-v6-preview.zip') as archive:
 for name in archive.namelist():
  if name.endswith('.html'):
   widget=BS(archive.read(name),'html.parser').select_one('details.help-widget')
   assert widget and not widget.has_attr('open') and len(widget.select('a'))==2,name
print('PASS: all 150 source/preview/archived EN/ZH pages default to a closed native help disclosure, with exactly two labelled contact links and correct language-relative quote destinations.')

Path('work').mkdir(exist_ok=True)
reference=json.loads(Path('work/help-style-baseline.json').read_text()) if Path('work/help-style-baseline.json').exists() else []
style_keys=['fontSize','fontWeight','lineHeight','padding','border','borderRadius','backgroundColor','color','bottom','right']
with sync_playwright() as pw:
 browser=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 base='http://127.0.0.1:8766/'
 no_js=browser.new_context(java_script_enabled=False,viewport={'width':390,'height':900})
 p=no_js.new_page()
 for language in ['', 'zh/']:
  p.goto(base+language+'index.html');p.locator('.help').click()
  assert p.locator('.help-panel [data-contact=whatsapp]').is_visible()
  assert p.locator('.help-panel [data-contact=email]').is_visible()
  p.locator('.help').click();assert not p.locator('.help-panel').is_visible()
 no_js.close()
 context=browser.new_context();page=context.new_page();errors=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.on('response',lambda r:errors.append(f'{r.status} {r.url}') if r.status>=400 else None)
 for prefix in ['', 'preview/v6/']:
  for width in [320,390,768,1440]:
   page.set_viewport_size({'width':width,'height':900})
   for language in ['', 'zh/']:
    for path in ['index.html','products/RP-C11.html']:
     assert page.goto(base+prefix+language+path).status==200
     panel=page.locator('.help-panel');trigger=page.locator('.help')
     assert not panel.is_visible()
     if prefix=='' and path=='index.html':
      for sample in reference:
       if sample['width']==width and sample['language']==language:
        box=trigger.bounding_box()
        assert all(abs(box[k]-sample['box'][k])<1 for k in ['x','y','width','height']),(sample,box)
        style=trigger.evaluate('(e,keys)=>{const s=getComputedStyle(e);return Object.fromEntries(keys.map(k=>[k,s[k]]))}',style_keys)
        assert style==sample['style'],(sample,style)
     before=page.url
     if prefix=='' and path=='index.html' and width==390:
      page.screenshot(path='work/mobile-ui-'+('zh' if language else 'en')+'-closed.png')
     trigger.click();assert page.url==before
     assert panel.is_visible() and panel.locator('a').count()==2
     assert panel.locator('[data-contact=whatsapp]').is_visible()
     assert panel.locator('[data-contact=email]').is_visible()
     assert panel.locator('[data-contact=whatsapp]').inner_text()=='WhatsApp'
     assert panel.locator('[data-contact=email] span').inner_text()==('邮件联系' if language else 'Email us')
     box=panel.bounding_box();assert box['x']>=0 and box['x']+box['width']<=width and box['y']>=0
     assert box['y']+box['height']<trigger.bounding_box()['y']
     if prefix=='' and path=='index.html' and width==390:
      page.screenshot(path='work/mobile-ui-'+('zh' if language else 'en')+'-help-open.png')
     trigger.click();assert not panel.is_visible()
     trigger.click();page.mouse.click(4,5);assert not panel.is_visible()
     trigger.click();page.keyboard.press('Escape');assert not panel.is_visible()
     assert trigger.evaluate('(e)=>e===document.activeElement')
     page.keyboard.press('Enter');assert panel.is_visible()
     panel.locator('[data-contact=email]').click()
     assert page.url==base+prefix+language+'get-quote.html'
     assert page.locator('#quote-form').is_visible()
     assert not page.locator('.help-panel').is_visible()
 assert not errors,errors
 browser.close()
print('PASS: 320/390/768/1440px EN/ZH home/product and preview; both contact options appear on click without navigation, quote form opens, native no-JS fallback, keyboard/Escape/outside/toggle close; floating trigger position/dimensions/colours/fonts match pre-change 390/1440px measurements; no overflow/JS/resource failures. No external chat service is opened by the test.')
