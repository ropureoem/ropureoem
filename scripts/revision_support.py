"""Compare immutable Git evidence in the current public model namespace.

Correspondence is reconstructed in memory from historical model ordering for
regression tests only; no correspondence file is written or published.
Measurements, SEO keywords and image bytes are never transformed.
"""
import re,subprocess
from functools import lru_cache
from pathlib import Path

_REFERENCE='7faf36a35fc7b564f6e8c5d63ec2f0463198aee2'
_TEXT={'.html','.md','.json','.js','.tsv','.css','.py','.txt','.xml','.yml','.yaml','.svg','.csv'}
@lru_cache(maxsize=1)
def _identifiers():
 paths=subprocess.check_output(['git','ls-tree','-r','--name-only',_REFERENCE,'products']).decode().splitlines()
 result={}
 for category,letter in [('CT','C'),('UR','U'),('T','F'),('SH','S'),('WS','W')]:
  names=sorted(Path(p).stem for p in paths if re.fullmatch(r'[A-Z]{2}-'+category+r'\d{2}',Path(p).stem))
  for index,name in enumerate(names,1):
   result[name]=f'RP-{letter}{index:02d}'
   result[name.split('-',1)[1]]=result[name]
 return result
@lru_cache(maxsize=1)
def _pattern():
 return re.compile(r'(?<![A-Za-z0-9-])(?:'+'|'.join(sorted(map(re.escape,_identifiers()),key=len,reverse=True))+r')(?!\d)')
def clean_obsolete_references(value):
 # Unlisted legacy housing variants have no product in the 62-model inventory.
 # Preserve configuration caveats without inventing new product identifiers.
 value=re.sub(r'Represents the [A-Z]{2}-T\d{2} variant; ([a-z])',lambda m:m[1].upper(),value)
 value=re.sub(r'代表 [A-Z]{2}-T\d{2} 变体；','',value)
 value=re.sub(r'Represents the T\d{2}[–-]T\d{2} and T\d{2} housing variants; ([a-z])',lambda m:m[1].upper(),value)
 value=re.sub(r'代表 T\d{2}[–-]T\d{2} 和 T\d{2} 外壳变体；','',value)
 return re.sub(r'gold/blue-light [A-Z]{2}-T\d{2} photo','gold/blue-light photo',value)
def current_name(value):return clean_obsolete_references(_pattern().sub(lambda m:_identifiers()[m[0]],value))
def current_bytes(data,path):
 return current_name(data.decode()).encode() if Path(path).suffix in _TEXT else data
@lru_cache(maxsize=None)
def revision_paths(revision):
 paths=subprocess.check_output(['git','ls-tree','-r','--name-only',revision]).decode().splitlines()
 return {current_name(path):path for path in paths}
def historical_bytes(revision,path,raw=False):
 name=revision_paths(revision)[str(path)]
 data=subprocess.check_output(['git','show',revision+':'+name])
 return data if raw else current_bytes(data,path)
