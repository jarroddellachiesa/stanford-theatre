import json,re,time,urllib.request,urllib.parse,os
UA={'User-Agent':'StanfordTheatreFanSite/1.0 (jarroddellachiesa@users.noreply.github.com)'}
C='tools/wiki_cache.json'; cache=json.load(open(C)) if os.path.exists(C) else {}
def get(u):
    if u in cache: return cache[u]
    for i in range(4):
        try:
            r=json.load(urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=30)); cache[u]=r; time.sleep(0.3); return r
        except Exception as ex: time.sleep(2+3*i)
    return {}
def norm(s): return re.sub(r'[^a-z0-9]','',re.sub(r'\(.*?\)','',s.lower()).replace('&','and'))
W='https://en.wikipedia.org/w/api.php?'
L=json.load(open('data/cover.json')); res={}
for o in L:
    t=re.sub(r'\s*\(.*?\)\s*$','',o['title']).strip()
    q=f"{t} {o['year']} film" if o['year'] else f"{t} film"
    r=get(W+urllib.parse.urlencode(dict(action='query',format='json',generator='search',gsrsearch=q,gsrlimit=8,prop='description|pageimages|extracts|pageprops',exintro=1,explaintext=1,exlimit=8,piprop='original',ppprop='wikibase_item',redirects=1)))
    pages=sorted((r.get('query',{}).get('pages') or {}).values(),key=lambda p:p.get('index',99))
    fy=int(o['first'][:4]); best=None;bs=-9
    for p in pages:
        de=p.get('description','')+' '+p.get('extract','')[:300]; m=re.search(r'\b(1[89]\d\d|20[0-2]\d)\b.{0,40}?\bfilm',de)
        if 'film' not in de.lower(): continue
        s=0
        if norm(p['title'])==norm(t) or norm(p['title']).startswith(norm(t)) and len(norm(p['title']))-len(norm(t))<6: s+=3
        elif norm(t) in norm(p['title']): s+=1
        else: continue
        py=int(m.group(1)) if m else None
        if o['year'] and py==o['year']: s+=3
        elif o['year'] and py and abs(py-o['year'])<=1: s+=1
        elif o['year'] and py: s-=3
        if not o['year'] and py: s+= 2 if fy-2<=py<=fy else (-3 if py>fy else 0)
        if s>bs: bs,best=s,(p,py)
    if best and bs>=3:
        p,py=best; res[o['key']]=dict(wt=p['title'],qid=p.get('pageprops',{}).get('wikibase_item'),img=(p.get('original') or {}).get('source'),desc=p.get('description'),ext=p.get('extract',''),wy=py,score=bs)
json.dump(cache,open(C,'w'))
qs=[v['qid'] for v in res.values() if v['qid']]
WD={}
for i in range(0,len(qs),50):
    r=get('https://www.wikidata.org/w/api.php?'+urllib.parse.urlencode(dict(action='wbgetentities',format='json',ids='|'.join(qs[i:i+50]),props='claims')))
    for q,en in (r.get('entities') or {}).items():
        c=en.get('claims',{}); g=lambda P:[x['mainsnak'].get('datavalue',{}).get('value') for x in c.get(P,[])]
        rt=[float(v['amount']) for v in g('P2047') if v]; im=[v for v in g('P345') if v]; pd=[v['time'][1:5] for v in g('P577') if v]
        P31=[v['id'] for v in g('P31') if v]
        WD[q]=dict(rt=round(min(rt)) if rt else None,imdb=im[0] if im else None,pd=min(pd) if pd else None,film=any(x in P31 for x in ['Q11424','Q24862','Q506240','Q202866','Q24869','Q229390','Q20650540']))
json.dump(cache,open(C,'w'))
for k,v in res.items(): v.update(WD.get(v['qid'],{}))
json.dump(res,open('data/cover_meta.json','w'),indent=0)
print(len(L),len(res),sum(1 for v in res.values() if v.get('img')),sum(1 for v in res.values() if v.get('rt')))
print('miss',[o['title'] for o in L if o['key'] not in res])
