# For covered films whose Wikipedia page image wasn't returned (non-free posters are often hidden from pageimages),
# read the infobox "image =" field from the article wikitext and record that file (poster) in cover_meta.
import json,re,time,urllib.request,urllib.parse
UA={'User-Agent':'StanfordTheatreFanSite/1.0 (jarroddellachiesa@users.noreply.github.com)'}
W='https://en.wikipedia.org/w/api.php?'
def get(p):
    for i in range(3):
        try: return json.load(urllib.request.urlopen(urllib.request.Request(W+urllib.parse.urlencode(p),headers=UA),timeout=30))
        except Exception: time.sleep(2+3*i)
    return {}
M=json.load(open('data/cover_meta.json')); C={o['key'] for o in json.load(open('data/cover.json'))}; n=0
for k,v in M.items():
    if k not in C or not v.get('wt') or v.get('poster_note') or v.get('img') not in (None,'None',''): continue
    r=get(dict(action='query',format='json',titles=v['wt'],prop='revisions',rvprop='content',rvslots='main',rvsection=0,redirects=1))
    pg=list((r.get('query') or {}).get('pages',{}).values())
    wt=pg[0]['revisions'][0]['slots']['main']['*'] if pg and pg[0].get('revisions') else ''
    m=re.search(r'\|\s*image\s*=\s*(?:\[\[)?(?:File:|Image:)?([^\|\n\]]+\.(?:jpe?g|png|gif|tiff?))',wt,re.I)
    if not m: continue
    f='File:'+m.group(1).strip()
    ii=get(dict(action='query',format='json',titles=f,prop='imageinfo',iiprop='url'))
    p=list((ii.get('query') or {}).get('pages',{}).values())
    if p and p[0].get('imageinfo'):
        v['img']=p[0]['imageinfo'][0]['url']; v['poster_src']='https://en.wikipedia.org/wiki/'+urllib.parse.quote(f.replace(' ','_')); n+=1
    time.sleep(0.2)
json.dump(M,open('data/cover_meta.json','w'),indent=0); print('infobox images found',n)
