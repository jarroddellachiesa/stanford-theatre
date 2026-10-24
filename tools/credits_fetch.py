import json,urllib.request,urllib.parse,time,os
UA={'User-Agent':'StanfordTheatreFanSite/1.0 (jarroddellachiesa@users.noreply.github.com)'}
C='tools/wd_credits_cache.json'; cache=json.load(open(C)) if os.path.exists(C) else {}
def get(u):
    if u in cache: return cache[u]
    for i in range(3):
        try: r=json.load(urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=60)); cache[u]=r; time.sleep(0.3); return r
        except Exception: time.sleep(3)
    return {}
CM=json.load(open('data/cover_meta.json'))
Q={k:v['qid'] for k,v in CM.items() if v.get('qid')}
for k,imdb in {'north by northwest':'tt0053125','on waterfront':'tt0047296','mary poppins':'tt0058331','wizard of oz':'tt0032138'}.items():
    r=get('https://www.wikidata.org/w/api.php?'+urllib.parse.urlencode(dict(action='query',list='search',srsearch=f'haswbstatement:P345={imdb}',format='json')))
    h=r.get('query',{}).get('search',[]); 
    if h: Q[k]=h[0]['title']
qs=sorted(set(Q.values())); CL={}
for i in range(0,len(qs),40):
    r=get('https://www.wikidata.org/w/api.php?'+urllib.parse.urlencode(dict(action='wbgetentities',format='json',ids='|'.join(qs[i:i+40]),props='claims')))
    for q,en in (r.get('entities') or {}).items(): CL[q]=en.get('claims',{})
def vals(c,P):
    out=[]
    for n,x in enumerate(c.get(P,[])):
        dv=x['mainsnak'].get('datavalue')
        if not dv or x.get('rank')=='deprecated': continue
        o=x.get('qualifiers',{}).get('P1545',[{}])[0].get('datavalue',{}).get('value')
        try: o=float(o)
        except Exception: o=None
        out.append((o if o is not None else 1e6+n,dv['value']['id']))
    return [q for _,q in sorted(out)]
need=set()
for c in CL.values():
    for P in ('P161','P57','P58','P162','P272'): need|=set(vals(c,P)[:6])
need=sorted(need); LB={}
for i in range(0,len(need),50):
    r=get('https://www.wikidata.org/w/api.php?'+urllib.parse.urlencode(dict(action='wbgetentities',format='json',ids='|'.join(need[i:i+50]),props='labels',languages='en')))
    for q,en in (r.get('entities') or {}).items():
        l=en.get('labels',{}).get('en',{}).get('value')
        if l: LB[q]=l
json.dump(cache,open(C,'w'))
OUT={}
for k,q in Q.items():
    c=CL.get(q,{}); L=lambda P,n:[LB[x] for x in vals(c,P) if x in LB][:n]
    cast=vals(c,'P161'); has_ord=any('P1545' in x.get('qualifiers',{}) for x in c.get('P161',[]))
    OUT[k]=dict(qid=q,star=L('P161',3),star_ordered=has_ord,director=L('P57',3),writer=L('P58',3),producer=L('P162',3),studio=L('P272',2))
json.dump(OUT,open('data/credits.json','w'),indent=0,ensure_ascii=False)
for f in ('star','director','writer','producer','studio'): print(f,sum(1 for v in OUT.values() if v[f]),'/',len(OUT))
print('cast with billing order',sum(1 for v in OUT.values() if v['star'] and v['star_ordered']))
print(OUT['mary poppins'])
