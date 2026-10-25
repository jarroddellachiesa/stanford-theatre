# Add cover_meta (+poster, credits) for specific keys with curated Wikipedia titles, without refetching everything.
# usage: python3 tools/cover_add.py  (reads data/cover_add.json {key: wikipedia title})
import json,re,time,urllib.request,urllib.parse,os,io
from PIL import Image
UA={'User-Agent':'StanfordTheatreFanSite/1.0 (jarroddellachiesa@users.noreply.github.com)'}
def get(u):
    for i in range(4):
        try: return json.load(urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=30))
        except Exception: time.sleep(2+3*i)
    return {}
W='https://en.wikipedia.org/w/api.php?'; WD='https://www.wikidata.org/w/api.php?'
ADD=json.load(open('data/cover_add.json')); M=json.load(open('data/cover_meta.json')); CR=json.load(open('data/credits.json'))
OV=json.load(open('data/cover_wt_overrides.json')); OV.update(ADD); json.dump(OV,open('data/cover_wt_overrides.json','w'),indent=1,ensure_ascii=False)
def lab(qs):
    if not qs: return {}
    r=get(WD+urllib.parse.urlencode(dict(action='wbgetentities',format='json',ids='|'.join(qs),props='labels',languages='en')))
    return {q:e_.get('labels',{}).get('en',{}).get('value') for q,e_ in (r.get('entities') or {}).items()}
for k,wt in ADD.items():
    if k in M and M[k].get('poster'): continue
    r=get(W+urllib.parse.urlencode(dict(action='query',format='json',titles=wt,prop='description|pageimages|extracts|pageprops',exintro=1,explaintext=1,piprop='original',ppprop='wikibase_item',redirects=1)))
    p=list((r.get('query',{}).get('pages') or {}).values())[0]
    assert 'missing' not in p, wt
    m=re.search(r'\b(1[89]\d\d|20[0-2]\d)\b',p.get('description','')+' '+p.get('extract','')[:300])
    v=dict(wt=p['title'],qid=p.get('pageprops',{}).get('wikibase_item'),img=(p.get('original') or {}).get('source'),desc=p.get('description'),ext=p.get('extract',''),wy=int(m.group(1)) if m else None,score=9)
    c=(get(WD+urllib.parse.urlencode(dict(action='wbgetentities',format='json',ids=v['qid'],props='claims'))).get('entities') or {}).get(v['qid'],{}).get('claims',{})
    g=lambda P:[x['mainsnak'].get('datavalue',{}).get('value') for x in c.get(P,[]) if x.get('rank')!='deprecated']
    rt=[float(x['amount']) for x in g('P2047') if x]; im=[x for x in g('P345') if x]; pd=[x['time'][1:5] for x in g('P577') if x]
    v.update(rt=round(min(rt)) if rt else None,imdb=im[0] if im else None,pd=min(pd) if pd else None,film=True)
    if v['img'] and not re.search(r'\.(jpe?g|png|gif|tiff?)(\?|$)',v['img'],re.I): v['img']=None  # e.g. a .webm clip, not a poster
    if not v['img']:  # infobox poster file
        r=get(W+urllib.parse.urlencode(dict(action='query',format='json',titles=v['wt'],prop='revisions',rvprop='content',rvslots='main',rvsection=0,redirects=1)))
        pg=list((r.get('query') or {}).get('pages',{}).values()); tx=pg[0]['revisions'][0]['slots']['main']['*'] if pg and pg[0].get('revisions') else ''
        mm=re.search(r'\|\s*image\s*=\s*(?:\[\[)?(?:File:|Image:)?([^\|\n\]]+\.(?:jpe?g|png|gif|tiff?))',tx,re.I)
        if mm:
            f='File:'+mm.group(1).strip(); ii=get(W+urllib.parse.urlencode(dict(action='query',format='json',titles=f,prop='imageinfo',iiprop='url')))
            pp=list((ii.get('query') or {}).get('pages',{}).values())
            if pp and pp[0].get('imageinfo'): v['img']=pp[0]['imageinfo'][0]['url']; v['poster_src']='https://en.wikipedia.org/wiki/'+urllib.parse.quote(f.replace(' ','_'))
    if v['img']:
        fn='posters/c/'+re.sub(r'[^a-z0-9]+','-',k.replace('#','-')).strip('-')+'.jpg'
        b=urllib.request.urlopen(urllib.request.Request(v['img'],headers=UA),timeout=40).read()
        imx=Image.open(io.BytesIO(b)).convert('RGB'); imx.thumbnail((400,600)); imx.save(fn,quality=82); v['poster']=fn
    M[k]=v
    def ids(P):
        out=[]
        for n,x in enumerate(c.get(P,[])):
            dv=x['mainsnak'].get('datavalue')
            if not dv or x.get('rank')=='deprecated': continue
            o=x.get('qualifiers',{}).get('P1545',[{}])[0].get('datavalue',{}).get('value')
            try: o=float(o)
            except Exception: o=None
            out.append((o if o is not None else 1e6+n,dv['value']['id']))
        return [q for _,q in sorted(out)][:6]
    need=sorted({q for P in ('P161','P57','P58','P162','P272') for q in ids(P)}); LB=lab(need)
    L=lambda P,n:[LB[x] for x in ids(P) if LB.get(x)][:n]
    CR[k]=dict(qid=v['qid'],star=L('P161',3),star_ordered=any('P1545' in x.get('qualifiers',{}) for x in c.get('P161',[])),director=L('P57',3),writer=L('P58',3),producer=L('P162',3),studio=L('P272',2))
    print(k,'|',v['wt'],v['pd'],v['rt'],v.get('poster'),CR[k]['studio'],CR[k]['star'])
json.dump(M,open('data/cover_meta.json','w'),indent=0); json.dump(CR,open('data/credits.json','w'),indent=0,ensure_ascii=False)
