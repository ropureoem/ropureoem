"""Verify the supplied interim clip is unchanged and its native player works locally (use scripts/serve_preview.py for seeking)."""
from pathlib import Path
from bs4 import BeautifulSoup as BS
from playwright.sync_api import sync_playwright
import hashlib,json,subprocess,zipfile

asset='assets/video/p90-1-product.mp4'
expected_size=18365143
expected_hash='8a8c877ecd8a466333f54eeea543d38ef5d97b19012ae2b4a8b33f4e3af298f4'
for path in [Path(asset),Path('preview/v6')/asset]:
 assert path.stat().st_size==expected_size,path
 assert hashlib.sha256(path.read_bytes()).hexdigest()==expected_hash,path
assert not Path('.github/workflows/fetch-p90-video.yml').exists()
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration,size:stream=codec_name,width,height','-of','json',asset]))
assert probe['streams'][0]['width']==720 and probe['streams'][0]['height']==1280
assert abs(float(probe['format']['duration'])-87.605)<.01
for prefix in ['', 'preview/v6/']:
 for language in ['', 'zh/']:
  path=Path(prefix+language+'index.html');doc=BS(path.read_text(),'html.parser')
  video=doc.select_one('#videos video')
  assert video and video.has_attr('controls') and video.has_attr('playsinline') and video['preload']=='metadata',path
  assert not video.has_attr('autoplay') and not video.has_attr('loop'),path
  assert (path.parent/video['src']).resolve()==Path(prefix+asset).resolve(),path
  assert not doc.select('#videos .video-poster'),path
  assert 'Footage pending' not in doc.select_one('#videos').get_text(),path
  assert '影像待提供' not in doc.select_one('#videos').get_text(),path
with zipfile.ZipFile('releases/ropureoem-v6-preview.zip') as archive:
 assert archive.testzip() is None
 assert archive.namelist().count(asset)==1
 assert len(archive.read(asset))==expected_size
 assert hashlib.sha256(archive.read(asset)).hexdigest()==expected_hash
 for name in ['index.html','zh/index.html']:
  assert BS(archive.read(name),'html.parser').select_one('#videos video[controls][preload=metadata]'),name
print('PASS: root/preview/ZIP match the original 18,365,143-byte clip and SHA-256; 87.605s, 720x1280; EN/ZH native controls/metadata/inline attributes, no autoplay/loop, old poster absent; one-off workflow removed.')

Path('work').mkdir(exist_ok=True)
with sync_playwright() as pw:
 browser=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 page=browser.new_page();errors=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.on('response',lambda r:errors.append(f'{r.status} {r.url}') if r.status>=400 else None)
 for base in ['http://127.0.0.1:8766/','http://127.0.0.1:8766/preview/v6/']:
  for width in [390,1440]:
   page.set_viewport_size({'width':width,'height':900})
   for language in ['', 'zh/']:
    assert page.goto(base+language+'index.html').status==200
    player=page.locator('#videos video')
    assert player.evaluate('(v)=>v.paused&&!v.autoplay&&v.controls&&v.preload==="metadata"')
    if width<700:
     assert not page.locator('#videos').is_visible()
     page.locator('.bottom-nav a').nth(3).click()
    else:page.goto(base+language+'index.html#videos')
    assert page.locator('#videos').is_visible()
    page.wait_for_function('(()=>{const v=document.querySelector("#videos video");return v.videoWidth===720&&v.videoHeight===1280&&v.readyState>=2})()',timeout=20000)
    assert player.evaluate('(v)=>v.paused&&v.currentTime===0&&v.error===null')
    player.evaluate('(v)=>v.scrollIntoView({block:"center",behavior:"instant"})')
    box=player.bounding_box()
    assert abs(box['width']/box['height']-720/1280)<.01,box
    assert player.evaluate('(v)=>getComputedStyle(v).objectFit')=='contain'
    # Click the browser's native play/pause control; no programmatic play call.
    player.click(position={'x':30,'y':box['height']-26})
    page.wait_for_function('(()=>{const v=document.querySelector("#videos video");return !v.paused&&v.currentTime>.2&&v.error===null})()',timeout=15000)
    player.click(position={'x':30,'y':box['height']-26})
    page.wait_for_function('document.querySelector("#videos video").paused')
    player.evaluate('(v)=>v.currentTime=10')
    page.wait_for_function('(()=>{const v=document.querySelector("#videos video");return !v.seeking&&v.currentTime>=9.9&&v.readyState>=2&&v.error===null})()')
    if base.endswith(':8766/') and width==390:
     page.locator('#videos').screenshot(path='work/p90-player-'+('zh' if language else 'en')+'.png')
 assert not errors,errors
 browser.close()
print('PASS: EN/ZH source and preview at 390/1440px; initial paused, mobile Videos reveal, metadata 720x1280, full-frame contain, actual native-control click starts/pauses playback and seeking works; no media/JS/resource errors.')
