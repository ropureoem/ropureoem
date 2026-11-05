"""Local static preview server on 127.0.0.1:8766 with byte-range support for video QA."""
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from pathlib import Path
import re
class Handler(SimpleHTTPRequestHandler):
 def send_head(self):
  self.byte_range=None
  p=Path(self.translate_path(self.path))
  header=self.headers.get('Range','')
  if p.is_file() and p.suffix=='.mp4' and header:
   match=re.fullmatch(r'bytes=(\d*)-(\d*)',header)
   if not match:return super().send_head()
   size=p.stat().st_size
   start=int(match[1]) if match[1] else max(0,size-int(match[2]))
   end=min(int(match[2]),size-1) if match[1] and match[2] else size-1
   if start>=size or start>end:
    self.send_response(416);self.send_header('Content-Range',f'bytes */{size}');self.send_header('Content-Length','0');self.end_headers();return None
   file=p.open('rb');file.seek(start);self.byte_range=(start,end)
   self.send_response(206);self.send_header('Content-Type','video/mp4');self.send_header('Accept-Ranges','bytes');self.send_header('Content-Range',f'bytes {start}-{end}/{size}');self.send_header('Content-Length',str(end-start+1));self.end_headers();return file
  return super().send_head()
 def copyfile(self,source,output):
  try:
   if self.byte_range is None:return super().copyfile(source,output)
   remaining=self.byte_range[1]-self.byte_range[0]+1
   while remaining:
    block=source.read(min(65536,remaining))
    if not block:break
    output.write(block);remaining-=len(block)
  except (BrokenPipeError,ConnectionResetError):pass
if __name__=='__main__':
 ThreadingHTTPServer(('127.0.0.1',8766),Handler).serve_forever()
