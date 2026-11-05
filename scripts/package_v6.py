"""Create portable static preview without including historical archives recursively."""
from pathlib import Path
import shutil,zipfile
from bs4 import BeautifulSoup
from urllib.parse import urlsplit,unquote
import subprocess,sys
import xml.etree.ElementTree as ET
subprocess.run([sys.executable, 'scripts/build_bilingual.py'], check=True)
subprocess.run([sys.executable, 'scripts/generate_sitemap.py'], check=True)
root=Path('.');dest=root/'preview/v6'
# A clean rebuild prevents deleted product URLs/assets surviving regeneration.
if dest.exists():shutil.rmtree(dest)
dest.mkdir(parents=True)
files=[*root.glob('*.html'),*root.glob('*.txt'),*root.glob('*.css'),*root.glob('*.js'),root/'CNAME',root/'sitemap.xml',root/'README.md',root/'STATUS.md']
for p in files:shutil.copy2(p,dest/p.name)
for name in ['assets','public','styles','products','docs','zh','images']:
 shutil.copytree(root/name,dest/name,dirs_exist_ok=True)
# Every resource must resolve inside the portable directory.
for page in dest.rglob('*.html'):
 soup=BeautifulSoup(page.read_text(),'html.parser')
 for node in soup.select('[href],[src],[action]'):
  for attr in ['href','src','action']:
   u=urlsplit(node.get(attr,''))
   if u.scheme or u.netloc:continue
   target=(page.parent/unquote(u.path)).resolve() if u.path else page.resolve()
   assert target.is_relative_to(dest.resolve()) and target.exists(),(page,node)
   if u.fragment and target.suffix=='.html':assert BeautifulSoup(target.read_text(),'html.parser').find(id=unquote(u.fragment))
zip_path=root/'releases/ropureoem-v6-preview.zip'
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted(dest.rglob('*')):
  if p.is_file():
   # Media are already compressed; avoid redundant deflation.
   method=zipfile.ZIP_STORED if p.suffix.lower() in {'.jpg','.jpeg','.png','.webp','.mp4'} else zipfile.ZIP_DEFLATED
   z.write(p,p.relative_to(dest),compress_type=method)
with zipfile.ZipFile(zip_path) as z:
 assert z.testzip() is None
 assert len([p for p in z.namelist() if p.endswith('.html')])==150
 assert len([p for p in z.namelist() if p.startswith('zh/') and p.endswith('.html')])==75
 urls=[n.text for n in ET.fromstring(z.read('sitemap.xml')).findall('{*}url/{*}loc')]
 assert len(urls)==len(set(urls))==75 and not any('/zh/' in url for url in urls)
 for name in z.namelist():
  if not name.endswith('.html'):continue
  robots=BeautifulSoup(z.read(name),'html.parser').select('head meta[name=robots]')
  if name.startswith('zh/'):
   assert len(robots)==1 and robots[0]['content']=='noindex, nofollow',name
  else:assert not robots,name
 assert len([p for p in z.namelist() if p.startswith('products/RP-') and p.endswith('.html')])==62
 for p in dest.rglob('*'):
  if p.is_file():assert z.read(str(p.relative_to(dest)))==p.read_bytes()
print('PASS: portable preview and ZIP integrity; 150 pages (75 EN + 75 ZH), 62 models per language, English-only sitemap (75 URLs), ZH noindex, all files match.')
