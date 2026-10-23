import re,html,glob,json,os,datetime as dt
M0={m:i for i,m in enumerate("January February March April May June July August September October November December".split(),1)}
class _M(dict):
    def __contains__(s,k): return k[:3].title() in s.k
    def __getitem__(s,k): return s.k[k[:3].title()]
M=_M(); M.k={m[:3]:i for m,i in M0.items()}
def txt(x): return re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',x))).strip()
def yearof(fn,body):
    m=re.search(r'((?:19[89]|20[0-2])\d)',fn) or re.search(r'(?<!\d)(\d\d)(?!\d)',fn)
    if m:
        y=int(m.group(1)); return y if y>1900 else (1900+y if y>=80 else 2000+y)
    b=re.sub(r'\((?:19|20)\d\d\)','',txt(body)); m=re.search(r'\b(198[7-9]|199\d|20[0-2]\d)\b',b); return int(m.group(1)) if m else None
def pd(s,y):
    s=s.replace('–','-').replace('—','-'); s=re.sub(r'^(?:(?:Mon|Tues|Wednes|Thurs|Fri|Satur|Sun)day[s]?[-, ]*(?:(?:Mon|Tues|Wednes|Thurs|Fri|Satur|Sun)day)?[, ]*)+','',s.strip())
    m=re.match(r'([A-Z][a-z]+)\.? (\d+)(?: ?- ?(?:([A-Z][a-z]+)\.? )?(\d+))?',s)
    if not m or m.group(1) not in M or (m.group(3) and m.group(3) not in M): return None
    try:
        a=dt.date(y,M[m.group(1)],int(m.group(2))); mb=M[m.group(3)] if m.group(3) else a.month
        b=dt.date(y+(1 if mb<a.month else 0),mb,int(m.group(4))) if m.group(4) else a
        return a.isoformat(),b.isoformat()
    except Exception: return None
F=[];gaps=[]
for f in sorted(glob.glob('cache/cal/*')):
    fn=os.path.basename(f); t=open(f,errors='replace').read()
    ban=re.search(r'(?s)<div class="banner">(.*?)</div>',t)
    name=txt(re.sub(r'(?s)<a .*?</a>','',ban.group(1))) if ban else ''
    y=yearof(fn,t); blocks=[]
    cells=re.split(r'<td class="playdate"',t)[1:]
    for cell in cells:
        cell=re.split(r'(?i)</table',cell)[0]
        dm=re.search(r'(?s)<p class="date">(.*?)</p>',cell)
        if not dm: continue
        dtxt=txt(dm.group(1)); films=[]
        ps=re.findall(r'(?s)<p[^>]*>(.*?)</p>',cell)[1:]
        i=0
        while i<len(ps):
            p=ps[i]; a=re.search(r'(?s)<a [^>]*imdb[^>]*>(.*?)</a>',p)
            if a:
                yr=re.search(r'\(((?:19|20)\d\d)\)',txt(p))
                nxt=ps[i+1] if i+1<len(ps) else ''
                times=txt(nxt) if nxt and 'imdb' not in nxt and re.search(r'\d:\d\d',nxt) else ''
                films.append(dict(title=re.sub(r'\s*\(\d{4}\)\s*$','',txt(a.group(1))),year=int(yr.group(1)) if yr else None,times=times)); i+=2 if times else 1; continue
            i+=1
        rng=pd(dtxt,y) if y else None
        if films:
            blocks.append(dict(dates=dtxt,start=rng[0] if rng else None,end=rng[1] if rng else None,films=films))
            if not rng: gaps.append((fn,dtxt))
    if not blocks:
        hd=re.search(r'(?s)stanford_theatre\.gif[^>]*>(.*?)</td>',t)
        if hd and not name: name=txt(hd.group(1))
        for cell in re.split(r'(?i)<td\b',t)[1:]:
            cell=re.split(r'(?i)</td>',cell)[0]
            dm=re.search(r'(?s)<b>(.*?)</b>',cell)
            if not dm: continue
            dtxt=txt(dm.group(1)); films=[]
            for p in re.findall(r'(?s)<p[^>]*>(.*?)</p>',cell):
                for a,rest in re.findall(r'(?s)<a [^>]*imdb[^>]*>(.*?)</a>([^<]*)',p):
                    yr=re.search(r'\((\d{4})\)',p); href=re.search(r'href="([^"]*imdb[^"]*)"',p)
                    yy=re.search(r'%28(\d{4})%29|\((\d{4})\)',href.group(1) if href else '')
                    films.append(dict(title=txt(a),year=int(yy.group(1) or yy.group(2)) if yy else None,times=txt(rest)))
            if not films: continue
            rng=pd(dtxt,y) if y else None
            blocks.append(dict(dates=dtxt,start=rng[0] if rng else None,end=rng[1] if rng else None,films=films))
            if not rng: gaps.append((fn,dtxt))
    if blocks: F.append(dict(name=name or fn.rsplit('.',1)[0],file=fn,year=y,blocks=blocks,start=min((b['start'] for b in blocks if b['start']),default=None),end=max((b['end'] for b in blocks if b['end']),default=None)))
    else: gaps.append((fn,'no bills parsed'))
os.makedirs('stanford-site/data',exist_ok=True)
json.dump(dict(festivals=F,gaps=gaps),open('stanford-site/data/festivals.json','w'),ensure_ascii=False)
print(len(F),'festivals',sum(len(x['blocks']) for x in F),'bills')
print('range',min(x['start'] for x in F if x['start']),max(x['end'] for x in F if x['end']))
print('gaps',len(gaps),gaps[:25])
for x in sorted(F,key=lambda x:x['start'] or '')[:4]+sorted(F,key=lambda x:x['start'] or '')[-3:]: print(repr(x['name'][:70]),x['file'],x['start'],x['end'],len(x['blocks']))
