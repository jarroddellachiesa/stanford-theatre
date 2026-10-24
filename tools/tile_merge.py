import re,html,json,glob,datetime as dt,urllib.parse
p=P0='stanford-site/data/showings.json'
d=[o for o in json.load(open(p)) if o['source'] not in ('Tile','Stanford Theatre calendars')]
FJ=json.load(open('stanford-site/data/festivals.json'))
for fe in FJ['festivals']:
    for b in fe['blocks']:
        for fm in b['films']:
            d.append(dict(title=fm['title'],note=(fe['name'][:80]+' · '+fm['times']).strip(' ·'),start=b['start'] or (str(fe['year'])+'-00-00' if fe['year'] else '0000-00-00'),end=b['end'] or '',date_text=b['dates']+(', '+str(fe['year']) if fe['year'] else ' (year not given)'),fyear=fm['year'],source='Stanford Theatre calendars',url='festivals/archive/cal/'+fe['file']))
YR={}
for f in glob.glob('cache/cal/*'):
    for a in re.findall(r'<a [^>]*imdb[^>]*>([^<]{2,100})</a>',open(f,errors='replace').read()):
        m=re.match(r'(.*?)\s*\(((?:19|20)\d\d)\)\s*$',html.unescape(a).strip())
        if m: YR.setdefault(m.group(1).strip().lower(),int(m.group(2)))
YR.update({'north by northwest':1959,'on the waterfront':1954,'mary poppins':1964,'the wizard of oz':1939})
def parse(t):
    L=[x.strip() for x in html.unescape(re.sub(r'<[^>]+>','\n',t)).split('\n') if x.strip()]
    if 'has played' not in L: return None,[]
    title=L[L.index('has played')-1]; pair=[]; runs={}; i=0
    while i<len(L):
        if L[i]=='Plays alone': pair=[]
        elif L[i]=='Plays with':
            pair=[];j=i+1
            while j<len(L) and not re.fullmatch(r'\d+',L[j]): pair.append(L[j]); j+=1
            i=j; continue
        if i+4<len(L) and re.fullmatch(r'\d+',L[i]) and re.fullmatch(r"[A-Z][a-z]{2} \d+ '\d\d",L[i+1]):
            mo,dd,yy=re.match(r"(\w+) (\d+) '(\d\d)",L[i+1]).groups(); y=int(yy); y+=1900 if y>=80 else 2000
            dd_=dt.datetime.strptime(f"{mo} {dd} {y}","%b %d %Y").date()
            r=runs.setdefault(L[i],dict(pair=list(pair),dates=[],tickets=0)); r['dates'].append(dd_)
            try: r['tickets']+=int(L[i+3].replace(',',''))
            except: pass
            i+=5; continue
        i+=1
    return title,list(runs.values())
T={}
for f in glob.glob('cache/tileq/*.html')+glob.glob('tile/*.html'):
    title,runs=parse(open(f,errors='replace').read())
    if title and runs: T[title]=runs
tile=[]
for title,runs in T.items():
    q=urllib.parse.quote_plus(title)
    for r in sorted(runs,key=lambda r:min(r['dates'])):
        tile.append(dict(title=title,note=('w/ '+', '.join(r['pair'])) if r['pair'] else '',start=min(r['dates']).isoformat(),end=max(r['dates']).isoformat(),days=len(r['dates']),tickets=r['tickets'],source='Tile',url=f'https://tile.stanfordtheatre.org/tile?q={q}'))
seen=set();out=[]
for o in sorted(d+tile,key=lambda o:(o['start'],o['source']!='Tile')):
    k=(o['title'].lower(),o['start'],o['source'])
    if k in seen: continue
    seen.add(k); out.append(o)
import unicodedata
def NK(t):
    t=unicodedata.normalize('NFD',t); t=''.join(c for c in t if not unicodedata.combining(c)).lower()
    t=re.sub(r'\s*\((?:19|20)\d\d\)\s*$','',t).replace('&',' and ')
    t=re.sub(r"['’`]",'',t); w=[x for x in re.sub(r'[^a-z0-9]+',' ',t).split() if x not in('the','a','an')]
    return ' '.join(w)
def OKD(x): return bool(re.fullmatch(r'\d{4}-\d\d-\d\d',x or '')) and x[5:7]!='00' and x[:4]!='0000'
first=set()
for o in out:
    k=o['title'].strip().lower(); o['badge']=''; o.pop('label',None); o.pop('n',None); o.pop('run',None)
    if o['source']=='Stanford Theatre calendars':
        y=o.get('fyear') or YR.get(k)
        if y and o['start'][:4].isdigit() and int(o['start'][:4])>1000 and 0<=int(o['start'][:4])-y<=2: o['badge']='Original Run'
    elif o['source']!='Tile':
        if k not in first:
            first.add(k); y=YR.get(k)
            if y is None or int(o['start'][:4])-y<=2: o['badge']='Original Run'
# partner appearances -> runs for the partner film
tl={}
for o in out:
    if o['source']=='Tile': tl.setdefault(NK(o['title']),[]).append(o)
syn=[]
for o in [x for x in out if x['source']=='Tile' and x['note'].startswith('w/ ')]:
    for pn in o['note'][3:].split(', '):
        kp=NK(pn)
        if not kp or any(x['start']<=o['end'] and o['start']<=x['end'] for x in tl.get(kp,[])): continue
        n=dict(title=pn,note='w/ '+o['title'],start=o['start'],end=o['end'],days=o.get('days'),tickets=None,source='Tile',url=o['url'],via=1,badge='')
        tl.setdefault(kp,[]).append(n); syn.append(n)
out+=syn
# one chronological sequence per film; overlapping/adjacent dated entries = one run
G={}
for o in out:
    if OKD(o['start']): G.setdefault(NK(o['title']),[]).append(o)
for k,L in G.items():
    L.sort(key=lambda o:(o['start'],o.get('end') or o['start']))
    n=0;ce=None
    for o in L:
        e_=o.get('end') if OKD(o.get('end')) else o['start']
        if ce is None or dt.date.fromisoformat(o['start'])>dt.date.fromisoformat(ce)+dt.timedelta(days=1):
            n+=1; ce=e_
        elif e_>ce: ce=e_
        o['n']=n; o['run']=k+'|'+str(n)
out.sort(key=lambda o:(o['start'],o['source']!='Tile'))
with open(P0,'w') as fh: json.dump(out,fh,ensure_ascii=False)
open('stanford-site/data/showings.js','w').write('window.SHOWINGS='+json.dumps(out,ensure_ascii=False)+';')
for s in ['Tile','Stanford Theatre history page','Stanford Theatre calendars']:
    x=[o for o in out if o['source']==s]; print(s,'runs',len(x),'films',len(set(o['title'].lower() for o in x)),x[0]['start'],x[-1]['start'])
print('OR',sum(1 for o in out if o['badge']))
