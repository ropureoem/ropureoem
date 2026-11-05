"""Create portable static preview without including historical archives recursively."""
from pathlib import Path
import shutil,zipfile
from bs4 import BeautifulSoup
from urllib.parse import urlsplit,unquote
root=Path('.');dest=root/'preview/v6';dest.mkdir(parents=True,exist_ok=True)
files=[*root.glob('*.html'),*root.glob('*.txt'),*root.glob('*.css'),*root.glob('*.js'),root/'CNAME',root/'sitemap.xml',root/'README.md',root/'STATUS.md']
for p in files:shutil.copy2(p,dest/p.name)
for name in ['assets','public','styles','products','docs']:
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
  if p.is_file():z.write(p,p.relative_to(dest))
with zipfile.ZipFile(zip_path) as z:
 assert z.testzip() is None
 assert len([p for p in z.namelist() if p.endswith('.html')])==75
 assert len([p for p in z.namelist() if p.startswith('products/WT-') and p.endswith('.html')])==62
 for p in dest.rglob('*'):
  if p.is_file():assert z.read(str(p.relative_to(dest)))==p.read_bytes()
print('PASS: portable preview and ZIP integrity; 75 pages, 62 models, all files match.')
