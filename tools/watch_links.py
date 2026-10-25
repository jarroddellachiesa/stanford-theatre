# Find legitimate full-length online copies for covered films.
# Order: Wikidata P724 (Internet Archive ID) and P1651 (YouTube video ID), then archive.org advanced search
# restricted to collections feature_films / moviesandfilms, matched on title + year (+ runtime when known).
# Every link is verified (archive.org metadata has a video file; YouTube oEmbed resolves) before it is kept.
# Output: data/watch_links.json  {key: [{source,url,id,evidence}]}.  Cache: tools/watch_cache.json (gitignored).
import json,os,re,time,urllib.request,urllib.parse,unicodedata,sys
UA={'User-Agent':'StanfordTheatreFanSite/1.0 (jarroddellachiesa@users.noreply.github.com)'}
C='tools/watch_cache.json'; cache=json.load(open(C)) if os.path.exists(C) else {}
def get(u,js=True):
    if u in cache: return cache[u]
    for i in range(3):
        try:
            b=urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=40).read().decode('utf-8','replace')
            r=json.loads(b) if js else b; cache[u]=r; time.sleep(0.25); return r
        except urllib.error.HTTPError as ex:
            if ex.code in (400,401,403,404): cache[u]=None; return None
            time.sleep(2+3*i)
        except Exception: time.sleep(2+3*i)
    return None
def NK(t):
    t=unicodedata.normalize('NFKD',t).encode('ascii','ignore').decode().lower()
    t=re.sub(r'\(.*?\)','',t).replace('&',' and '); t=re.sub(r"['’`]",'',t)
    return ' '.join(w for w in re.sub(r'[^a-z0-9]+',' ',t).split() if w not in('the','a','an','and'))
def mins(s):
    s=str(s or '')
    m=re.match(r'^\s*(?:(\d+):)?(\d+):(\d\d)\s*$',s)
    if m: return (int(m.group(1) or 0)*60+int(m.group(2))+int(m.group(3))/60)
    m=re.search(r'(\d+)\s*(?:min|m\b)',s); return int(m.group(1)) if m else None
def ia_ok(ident,rt):
    md=get('https://archive.org/metadata/'+urllib.parse.quote(ident))
    if not md or not md.get('metadata'): return None
    m=md['metadata']; col=m.get('collection'); col=[col] if isinstance(col,str) else (col or [])
    vids=[f for f in md.get('files',[]) if re.search(r'\.(mp4|ogv|mpeg|mpg|avi|mkv|webm)$',f.get('name',''),re.I)]
    if not vids: return None
    L=max((float(f.get('length') or 0) for f in vids),default=0)/60 or mins(m.get('runtime'))
    if L and L<40: return None                      # shorts / clips / trailers
    if rt and L and abs(L-rt)>max(15,0.2*rt): return None
    if re.search(r'trailer|clip|excerpt|preview|scene',(m.get('title') or '')+' '+ident,re.I): return None
    return dict(collections=col,minutes=round(L) if L else None,license=m.get('licenseurl') or '',title=m.get('title'),year=m.get('year') or m.get('date'))
def yt_ok(vid):
    r=get('https://www.youtube.com/oembed?format=json&url='+urllib.parse.quote('https://www.youtube.com/watch?v='+vid))
    return r and dict(title=r.get('title'),channel=r.get('author_name'))
# official studio / distributor / rights-holder channels only
OFFICIAL={'YouTube Movies','Warner Bros. Classics','Harold Lloyd','Paramount Vault','Sony Pictures Entertainment','MGM','Universal Pictures','20th Century Studios','Criterion Collection','British Pathé','BFI','Janus Films','Kino Lorber','Flicker Alley'}
M=json.load(open('data/cover_meta.json')); COV={o['key']:o for o in json.load(open('data/cover.json'))}
OUT={}
qids=[v['qid'] for k,v in M.items() if k in COV and v.get('qid')]
WD={}
for i in range(0,len(qids),50):
    r=get('https://www.wikidata.org/w/api.php?action=wbgetentities&format=json&props=claims&ids='+'|'.join(qids[i:i+50])) or {}
    for q,e in (r.get('entities') or {}).items():
        cl=e.get('claims',{}); WD[q]={'P724':[c['mainsnak']['datavalue']['value'] for c in cl.get('P724',[]) if c['mainsnak'].get('datavalue')]}
        yt=[]
        for c in cl.get('P1651',[]):
            if not c['mainsnak'].get('datavalue'): continue
            ql=c.get('qualifiers',{}); role=[x.get('datavalue',{}).get('value',{}).get('id') for x in ql.get('P3831',[])]
            dur=[float(x['datavalue']['value']['amount']) for x in ql.get('P2047',[]) if x.get('datavalue')]
            unit=[x['datavalue']['value'].get('unit','') for x in ql.get('P2047',[]) if x.get('datavalue')]
            mins_=[d/60 if u.endswith('Q11574') else d for d,u in zip(dur,unit)]  # Q11574 = second
            if 'Q622550' in role or any(r in role for r in ('Q1365560','Q2297927')): continue   # trailer / clip / teaser
            if mins_ and max(mins_)<40: continue
            yt.append(dict(id=c['mainsnak']['datavalue']['value'],role=role,minutes=round(max(mins_)) if mins_ else None))
        WD[q]['P1651']=yt
        WD[q]['pd']=any(c['mainsnak'].get('datavalue',{}).get('value',{}).get('id')=='Q19652' for c in cl.get('P6216',[]))
n=0
for k,o in COV.items():
    v=M.get(k) or {}; q=v.get('qid'); rt=int(v['rt']) if str(v.get('rt') or '').isdigit() else None
    y=o.get('year') or (int(v['wy']) if str(v.get('wy') or '').isdigit() else None)
    L=[]
    # Internet Archive only when the film itself is public domain: Wikidata P6216 = public domain, or US release <= 1930
    PD=WD.get(q,{}).get('pd') or (y and y<=1930)
    for ident in (WD.get(q,{}).get('P724') or []):
        ok=PD and ia_ok(ident,rt)
        if ok: L.append(dict(source='Internet Archive',url='https://archive.org/details/'+ident,id=ident,evidence=dict(public_domain='Wikidata P6216' if WD.get(q,{}).get('pd') else 'US release <= 1930',via=f'Wikidata {q} P724',**ok)))
    for yv in (WD.get(q,{}).get('P1651') or []):
        vid=yv['id']; ok=yt_ok(vid)
        if ok and ok.get('channel') not in OFFICIAL: continue
        if not ok or re.search(r'trailer|teaser|clip|scene|excerpt|preview|featurette|review',ok.get('title') or '',re.I): continue
        if not yv['minutes'] and not re.search(r'full (movie|film)|complete film|full length',ok.get('title') or '',re.I): continue  # need duration or explicit full-film title
        L.append(dict(source='YouTube',url='https://www.youtube.com/watch?v='+vid,id=vid,evidence=dict(via=f'Wikidata {q} P1651',minutes=yv['minutes'],**ok)))
    if PD and not any(x['source']=='Internet Archive' for x in L) and y:
        t=re.sub(r'\s*\(.*?\)\s*$','',o['title']).replace('"','')
        qq=f'title:("{t}") AND mediatype:movies AND collection:(feature_films OR moviesandfilms) AND year:[{y-1} TO {y+1}]'
        r=get('https://archive.org/advancedsearch.php?'+urllib.parse.urlencode([('q',qq),('fl[]','identifier'),('fl[]','title'),('fl[]','year'),('rows','10'),('output','json')]))
        for d in ((r or {}).get('response') or {}).get('docs',[]):
            if NK(d.get('title','')) != NK(t): continue
            ok=ia_ok(d['identifier'],rt)
            if ok and (rt or ok['minutes']):
                L.append(dict(source='Internet Archive',url='https://archive.org/details/'+d['identifier'],id=d['identifier'],evidence=dict(public_domain='Wikidata P6216' if WD.get(q,{}).get('pd') else 'US release <= 1930',via='archive.org search: title + year'+(' + runtime' if rt and ok['minutes'] else ''),**ok))); break
    if L: OUT[k]=L
    else: OUT.pop(k,None)
    n+=1
    if n%50==0: json.dump(cache,open(C,'w')); print(n,len(OUT),flush=True)
json.dump(cache,open(C,'w'))
json.dump(dict(sorted(OUT.items())),open('data/watch_links.json','w'),indent=1,ensure_ascii=False)
from collections import Counter
print('films with links',len(OUT),Counter(x['source'] for L in OUT.values() for x in L))
