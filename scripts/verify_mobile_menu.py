"""Verify default-closed mobile menus and every close interaction on local port 8766."""
from pathlib import Path
import zipfile
from bs4 import BeautifulSoup as BS
from playwright.sync_api import sync_playwright

for prefix in ['', 'preview/v6/']:
 pages=[*Path(prefix or '.').glob('*.html'),*Path(prefix+'products').glob('*.html'),*Path(prefix+'zh').rglob('*.html')]
 assert len(pages)==150,(prefix,len(pages))
 for path in pages:
  menu=BS(path.read_text(),'html.parser').select_one('details.nav-menu')
  assert menu is not None and not menu.has_attr('open'),path
with zipfile.ZipFile('releases/ropureoem-v6-preview.zip') as archive:
 pages=[name for name in archive.namelist() if name.endswith('.html')]
 assert len(pages)==150
 for name in pages:
  menu=BS(archive.read(name),'html.parser').select_one('details.nav-menu')
  assert menu is not None and not menu.has_attr('open'),name
print('PASS: all 150 EN/ZH source pages, 150 preview pages and 150 archived pages omit the initial menu open attribute.')

Path('work').mkdir(exist_ok=True)
with sync_playwright() as pw:
 browser=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 base='http://127.0.0.1:8766/'
 # Initial HTML/CSS must remain closed even if the shared script never executes.
 no_js=browser.new_context(java_script_enabled=False,viewport={'width':390,'height':844})
 page=no_js.new_page()
 for prefix in ['', 'preview/v6/']:
  for language in ['', 'zh/']:
   page.goto(base+prefix+language+'index.html')
   assert not page.locator('.nav-menu > nav').is_visible()
   assert page.locator('.studio-hero').is_visible()
   page.locator('.nav-menu > summary').click()
   assert page.locator('.nav-menu > nav').is_visible()
   page.locator('.nav-menu > summary').click()
   assert not page.locator('.nav-menu > nav').is_visible()
 no_js.close()
 errors=[]
 context=browser.new_context()
 page=context.new_page()
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.on('response',lambda r:errors.append(f'{r.status} {r.url}') if r.status>=400 else None)
 def closed():
  assert not page.locator('.nav-menu').evaluate('(e)=>e.open')
  assert not page.locator('.nav-menu > nav').is_visible()
 def open_menu():
  page.locator('.nav-menu > summary').click()
  assert page.locator('.nav-menu > nav').is_visible()
 for prefix in ['', 'preview/v6/']:
  for width in [320,390,768,1024]:
   page.set_viewport_size({'width':width,'height':900})
   for language in ['', 'zh/']:
    for path in ['index.html','products/RP-C11.html']:
     assert page.goto(base+prefix+language+path).status==200
     closed()
     assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
     if width<700:
      tools=page.locator('.header-tools').bounding_box()
      search=page.locator('.header-search').bounding_box()
      switch=page.locator('.header-tools > .language-switch').bounding_box()
      field=page.locator('.header-search input').bounding_box()
      assert abs(tools['x']-search['x'])<1
      assert abs(switch['x']+switch['width']-tools['x']-tools['width'])<1
      assert abs(tools['width']-width+32)<1
      assert search['width']>190 and field['width']>150
      assert abs(search['y']+search['height']/2-switch['y']-switch['height']/2)<1

     if path=='index.html':
      assert page.locator('.studio-hero').is_visible()
      if prefix=='' and width==390:
       page.locator('.studio-hero img').evaluate('(e)=>e.decode()')
       page.screenshot(path='work/menu-closed-'+('zh' if language else 'en')+'-mobile.png')
     open_menu();page.locator('.nav-menu > summary').click();closed()
     open_menu();before=page.url;page.mouse.click(4,5);closed();assert page.url==before
     # Prevent navigation once to prove the click itself closes the menu.
     open_menu()
     page.locator('.nav-menu > nav > a').first.evaluate('(a)=>a.addEventListener("click",e=>e.preventDefault(),{once:true})')
     page.locator('.nav-menu > nav > a').first.click();closed()
     open_menu();page.locator('.products-menu > summary').click()
     page.locator('.products-menu a').first.evaluate('(a)=>a.addEventListener("click",e=>e.preventDefault(),{once:true})')
     page.locator('.products-menu a').first.click();closed()
     assert not page.locator('.products-menu').evaluate('(e)=>e.open')
     open_menu();page.keyboard.press('Escape');closed()
 # Desktop remains visible; shrinking to mobile closes a previously open menu.
 page.set_viewport_size({'width':1440,'height':1000});page.goto(base+'index.html')
 assert page.locator('.nav-menu > nav').is_visible()
 page.set_viewport_size({'width':390,'height':900})
 page.wait_for_function('!document.querySelector(".nav-menu").open');closed()
 open_menu();page.evaluate('dispatchEvent(new PageTransitionEvent("pageshow",{persisted:true}))');closed()
 # All five bottom-navigation destinations and both language switches still work.
 for language in ['', 'zh/']:
  targets=['index.html','products.html','get-quote.html','index.html#videos','contact.html']
  for index,target in enumerate(targets):
   page.goto(base+language+'index.html');open_menu()
   page.locator('.bottom-nav a').nth(index).click()
   assert page.url==base+language+target,(language,target,page.url)
   closed()
  page.goto(base+language+'index.html');closed()
  page.locator('header [data-language='+('en' if language else 'zh')+']').click()
  closed()
 assert not errors,errors
 browser.close()
print('PASS: 320/390/768/1024px EN/ZH home/product and preview; initial closed even without JS; Menu toggles, outside click, direct/nested links, Escape and history restore close; desktop/resizing, hero visibility, five bottom-nav destinations and language switches; full-width mobile search with longer input and EN/ZH at the right content edge; no overflow/JS/resource errors.')
