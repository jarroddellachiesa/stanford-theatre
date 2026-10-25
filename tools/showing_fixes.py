# Applies curated title/year answers (data/showing_fixes.json) to data/showings.json and data/festivals.json.
# Idempotent; run by tools/cover_pick.py and build.py so every rebuild keeps the answers.
import json,re,os,collections,datetime as _dt,unicodedata
def _apply():
    if not os.path.exists('data/showing_fixes.json'): return
    FX=json.load(open('data/showing_fixes.json')); SH=json.load(open('data/showings.json')); FJ=json.load(open('data/festivals.json'))
    TA=json.load(open('data/title_aliases.json'))
    if any(TA['aliases'].get(k)!=v for k,v in FX.get('aliases',{}).items()):
        TA['aliases'].update(FX['aliases']); TA['aliases']=dict(sorted(TA['aliases'].items()))
        json.dump(TA,open('data/title_aliases.json','w'),indent=1,ensure_ascii=False)
    before=json.dumps(SH,ensure_ascii=False); fbefore=json.dumps(FJ,ensure_ascii=False)
    SH=[o for o in SH if not o.get('fixcopy')]
    touched=set(); add=[]
    base=lambda o:o.get('run','').rsplit('|',1)[0]
    for o in SH:
        t=o.get('orig_title') or o['title']
        for r in FX.get('assign',[]):
            if not re.search(r['re'],t,re.I) or not (r['from']<=o['start']<=r['to']): continue
            touched.add(base(o)); touched.add(r['key'])
            if r.get('title') and o['title']!=r['title']: o.setdefault('orig_title',o['title']); o['title']=r['title']
            o['run']=r['key']+'|'+(o.get('run','|0').rsplit('|',1)[1]); o['fyear']=r['year']; o.pop('tyear',None); o['fixed']=1
            for c in r.get('copy',[]):
                n=dict(o,run=c['key']+'|0',fyear=c['year'],fixcopy=1); touched.add(c['key']); add.append(n)
    SH+=add
    OKD=lambda x:bool(re.fullmatch(r'\d{4}-\d\d-\d\d',x or '')) and x[5:7]!='00'
    G=collections.defaultdict(list)
    for o in SH:
        if base(o) in touched and o.get('run'): G[base(o)].append(o)
    for k,L in G.items():
        L.sort(key=lambda o:(o['start'],o.get('end') or o['start'])); n=0; ce=None
        for o in L:
            e_=o.get('end') if OKD(o.get('end')) else o['start']
            if ce is None or _dt.date.fromisoformat(o['start'])>_dt.date.fromisoformat(ce)+_dt.timedelta(days=1): n+=1; ce=e_
            elif e_>ce: ce=e_
            o['n']=n; o['run']=k+'|'+str(n)
    # festival-calendar year corrections
    for fe in FJ['festivals']:
        for b in fe['blocks']:
            for fm in b['films']:
                for r in FX.get('fest_year',[]):
                    if b.get('start')==r['start'] and re.search(r['re'],fm['title'],re.I):
                        fm['year']=r['year']
                        if r.get('title'): fm['title']=r['title']
    # one-year mismatches: use the year most festival listings give (tie -> Wikidata release year)
    if FX.get('majority_year'):
        def NK(t):
            t=unicodedata.normalize('NFKD',t).encode('ascii','ignore').decode().lower()
            t=re.sub(r"[^a-z0-9 ]","",t.replace('&','and')); t=re.sub(r'\b(the|a|an|and)\b',' ',t); t=re.sub(r'ing\b','in',t)
            return ' '.join(t.split())
        SPL={k.replace('-',''):v for k,v in FX.get('split',{}).items()}
        CM=json.load(open('data/cover_meta.json')) if os.path.exists('data/cover_meta.json') else {}
        Y=collections.defaultdict(collections.Counter)
        for fe in FJ['festivals']:
            for b in fe['blocks']:
                for fm in b['films']:
                    if fm.get('year'): Y[NK(fm['title'])][fm['year']]+=1
        FIXY={}
        for k,c in Y.items():
            ys=sorted(c)
            if len(ys)!=2 or ys[1]-ys[0]!=1 or k in SPL or k.replace(' ','') in SPL: continue
            (a,na),(b_,nb)=c.most_common(2)
            if na>nb: FIXY[k]=a
            else:
                pd=(CM.get(k) or {}).get('pd')
                if pd and int(pd) in ys: FIXY[k]=int(pd)
        for fe in FJ['festivals']:
            for b in fe['blocks']:
                for fm in b['films']:
                    y=FIXY.get(NK(fm['title']))
                    if y and fm.get('year') and fm['year']!=y: fm['year']=y
        for o in SH:
            y=FIXY.get(NK(o['title']))
            if y and o.get('fyear') and o['fyear']!=y and o['source']=='Stanford Theatre calendars': o['fyear']=y
        json.dump(sorted(FIXY.items()),open('data/majority_years.json','w'),indent=0)
    SH.sort(key=lambda o:(o['start'],o['source']!='Tile'))
    if json.dumps(SH,ensure_ascii=False)!=before: json.dump(SH,open('data/showings.json','w'),ensure_ascii=False)
    if json.dumps(FJ,ensure_ascii=False)!=fbefore: json.dump(FJ,open('data/festivals.json','w'),ensure_ascii=False,indent=1 if open('data/festivals.json').read(3).startswith('{\n') else None)
_apply()
