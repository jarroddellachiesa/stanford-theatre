import json,urllib.request,os,io,time,re
from PIL import Image
UA={'User-Agent':'StanfordTheatreFanSite/1.0 (jarroddellachiesa@users.noreply.github.com)'}
M=json.load(open('data/cover_meta.json')); os.makedirs('posters/c',exist_ok=True); ok=0;bad=[]
for k,v in M.items():
    if not v.get('img') or v.get('poster_note'): continue
    fn='posters/c/'+re.sub(r'[^a-z0-9]+','-',k.replace('#','-')).strip('-')+'.jpg'; v['poster']=fn
    if os.path.exists(fn): ok+=1; continue
    for i in range(3):
        try:
            u=v['img']; m=re.match(r'(https://upload.wikimedia.org/wikipedia/\w+/)(\w/\w\w/)([^/]+)$',u)
            if False: u=m.group(1)+'thumb/'+m.group(2)+m.group(3)+'/500px-'+m.group(3)
            b=urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=40).read()
            im=Image.open(io.BytesIO(b)).convert('RGB'); im.thumbnail((400,600)); im.save(fn,quality=82); ok+=1; break
        except Exception as ex: time.sleep(3+5*i)
    else: bad.append(k); v.pop('poster')
    time.sleep(0.4)
json.dump(M,open('data/cover_meta.json','w'),indent=0); print('posters',ok,'failed',bad)
