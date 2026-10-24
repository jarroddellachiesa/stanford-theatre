import json,urllib.request,urllib.parse,time,os
UA={'User-Agent':'StanfordTheatreFanSite/1.0 (jarroddellachiesa@users.noreply.github.com)'}
C='tools/wd_facts_cache.json'; cache=json.load(open(C)) if os.path.exists(C) else {}
def get(u):
    if u in cache: return cache[u]
    for i in range(3):
        try: r=json.load(urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=60)); cache[u]=r; time.sleep(0.3); return r
        except Exception: time.sleep(3)
    return {}
CM=json.load(open('data/cover_meta.json'))
q2k={v['qid']:k for k,v in CM.items() if v.get('qid')}; qs=list(q2k); CL={}
for i in range(0,len(qs),40):
    r=get('https://www.wikidata.org/w/api.php?'+urllib.parse.urlencode(dict(action='wbgetentities',format='json',ids='|'.join(qs[i:i+40]),props='claims')))
    for q,en in (r.get('entities') or {}).items(): CL[q]=en.get('claims',{})
json.dump(cache,open(C,'w'))
ids=lambda c,P:[x['mainsnak']['datavalue']['value']['id'] for x in c.get(P,[]) if x['mainsnak'].get('datavalue')]
need=set()
for c in CL.values():
    for P in ('P915','P166','P144','P1411','P840'): need|=set(ids(c,P))
need=sorted(need); LB={}
for i in range(0,len(need),50):
    r=get('https://www.wikidata.org/w/api.php?'+urllib.parse.urlencode(dict(action='wbgetentities',format='json',ids='|'.join(need[i:i+50]),props='labels|descriptions',languages='en')))
    for q,en in (r.get('entities') or {}).items(): LB[q]=(en.get('labels',{}).get('en',{}).get('value'),en.get('descriptions',{}).get('en',{}).get('value'))
json.dump(cache,open(C,'w'))
OUT={}
for q,c in CL.items():
    L=lambda P:[LB.get(x,(None,))[0] for x in ids(c,P) if LB.get(x,(None,))[0]]
    loc=list(dict.fromkeys(L('P915')))
    tr=[]
    aw=list(dict.fromkeys(L('P166'))); nm=L('P1411')
    for a in aw:
        if any(w in a for w in ('Registry','Top Ten','Top 10','list')): tr.append(f'Selected for the {a}.')
        else: tr.append(f'Won the {a}.' if not a.lower().startswith('the ') else f'Won {a}.')
    nm=[x for x in dict.fromkeys(nm) if x not in aw]
    if nm: tr.append(('Also nominated for: ' if aw else 'Nominated for: ')+'; '.join(nm[:4])+(f'; and {len(nm)-4} more' if len(nm)>4 else '')+'.')
    for x in ids(c,'P144'):
        lb=LB.get(x)
        if lb and lb[0]: tr.append(f'Based on {lb[0]}'+(f' ({lb[1]})' if lb[1] else '')+'.')
    OUT[q2k[q]]=dict(loc=loc[:12],trivia=tr[:10])
json.dump(OUT,open('data/cover_facts.json','w'),indent=0,ensure_ascii=False)
print('films',len(OUT),'loc',sum(1 for v in OUT.values() if v['loc']),'trivia',sum(1 for v in OUT.values() if v['trivia']))
