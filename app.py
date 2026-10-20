"""Run locally: python app.py --port 8000. No external dependencies."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse,parse_qs
import argparse,json
from matching import recommend
ROOT=Path(__file__).resolve().parent
class Handler(BaseHTTPRequestHandler):
 def do_GET(self):
  parsed=urlparse(self.path)
  if parsed.path=='/':
   body=(ROOT/'index.html').read_bytes();kind='text/html; charset=utf-8'
  elif parsed.path=='/api/profiles':
   body=(ROOT/'data/profiles.json').read_bytes();kind='application/json'
  elif parsed.path=='/api/metrics':
   body=(ROOT/'outputs/metrics.json').read_bytes();kind='application/json'
  elif parsed.path=='/api/matches':
   try:
    uid=int(parse_qs(parsed.query).get('user',['1'])[0])
    profiles=json.loads((ROOT/'data/profiles.json').read_text())
    user=next(p for p in profiles if p['id']==uid)
   except (ValueError,StopIteration):
    self.send_error(400,'Unknown profile');return
   body=json.dumps(recommend(user,profiles)).encode();kind='application/json'
  else:
   self.send_error(404);return
  self.send_response(200);self.send_header('Content-Type',kind)
  self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body)
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--port',type=int,default=8000)
 args=parser.parse_args()
 ThreadingHTTPServer(('127.0.0.1',args.port),Handler).serve_forever()
