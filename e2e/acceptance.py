"""Verify deployed static status assets and client routing without a browser."""
import argparse,hashlib,json,urllib.request,urllib.error
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('origin');p.add_argument('assets');p.add_argument('receipt');a=p.parse_args()
root=Path(a.assets);results=[]
def get(path):
 return urllib.request.urlopen(urllib.request.Request(a.origin.rstrip('/')+path,headers={'User-Agent':'UniClipboard-Status-Acceptance/1.0'}),timeout=40)
for path in ['/','/history/website','/incident/1','/rate-limit-exceeded']:
 with get(path) as r:
  assert r.status==200,(path,r.status)
  assert b'UniClipboard' in r.read(),path
  assert 'no-cache' in r.headers.get('Cache-Control',''),path
 results.append({'path':path,'result':'PASS'})
count=0
for file in sorted(root.rglob('*')):
 if file.is_file() and file.name not in ['_headers','_redirects','404.html','index.html','service-worker-index.html']:
  path='/'+str(file.relative_to(root))
  with get(path) as r: assert hashlib.sha256(r.read()).digest()==hashlib.sha256(file.read_bytes()).digest(),path
  count+=1
for path in ['/client/migration-missing.js','/migration-missing','/.git/config','/.env']:
 try:
  get(path);raise AssertionError('Missing asset returned success: '+path)
 except urllib.error.HTTPError as e: assert e.code==404,(path,e.code)
results.append({'name':'all static asset hashes','files':count,'result':'PASS'})
for path in ['/service-worker.js','/manifest.json']:
 with get(path) as r: assert 'no-cache' in r.headers.get('Cache-Control',''),path
out={'origin':a.origin,'results':results,'browser':'NOT_RUN_USER_OWNED'}
Path(a.receipt).parent.mkdir(parents=True,exist_ok=True);Path(a.receipt).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
