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
    s=s.replace('–','-').replace('—','-').strip()
    s=re.sub(r'^uly\b','July',s)
    s=re.sub(r'^(?:(?:Mon|Tue|Tues|Wed|Wednes|Thu|Thur|Thurs|Fri|Sat|Satur|Sun)(?:day)?s?\b\.?\s*(?:[-,/&]|and)?\s*)+','',s)
    s=re.sub(r'^([A-Z][a-z]+)\.?(\d)',r'\1 \2',s)
    ym=re.search(r',\s*((?:19|20)\d\d)\b',s)
    if ym: y=int(ym.group(1)); s=re.sub(r',\s*(?:19|20)\d\d\b','',s)
    m=re.match(r'([A-Z][a-z]+)\.? (\d+)(?: ?[-,] ?(?:([A-Z][a-z]+)\.? )?(\d+))?',s)
    if not m or m.group(1) not in M or (m.group(3) and m.group(3) not in M): return None
    try:
        a=dt.date(y,M[m.group(1)],int(m.group(2))); mb=M[m.group(3)] if m.group(3) else a.month
        b=dt.date(y+(1 if mb<a.month else 0),mb,int(m.group(4))) if m.group(4) else a
        return a.isoformat(),b.isoformat()
    except Exception: return None
def fixt(t):
    m0=re.search(r'\s*\(((?:19|20)\d\d)\s*$',t)
    if m0: return t[:m0.start()].strip(),int(m0.group(1))
    t=re.sub(r'\s*\(\d{4}\)\s*$','',t); m=re.search(r'\s*\(\s*([^()]*?)\s*,?\s*((?:19|20)\d\d)\s*\)\s*$',t); ey=None
    if m:
        ey=int(m.group(2)); inner=m.group(1).strip(' ,')
        t=t[:m.start()].strip()+(' ('+inner+')' if inner else '')
    return t.strip(),ey
F=[];gaps=[]
OV=json.load(open('stanford-site/data/festival_overrides.json')) if os.path.exists('stanford-site/data/festival_overrides.json') else {}
for f in sorted(glob.glob('cache/cal/*')):
    fn=os.path.basename(f); t=open(f,errors='replace').read()
    ban=re.search(r'(?s)<div class="banner">(.*?)</div>',t)
    name=txt(re.sub(r'(?s)<a .*?</a>','',ban.group(1))) if ban else ''
    slug=re.sub(r'%20',' ',fn.rsplit('.',1)[0]); ov=OV.get(slug,{})
    y=ov.get('year') or yearof(fn,t); blocks=[]
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
                tt,ey=fixt(txt(a.group(1))); films.append(dict(title=tt,year=(int(yr.group(1)) if yr else ey),times=times)); i+=2 if times else 1; continue
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
                    tt,ey=fixt(txt(a)); ry=re.match(r'\s*\(((?:19|20)\d\d)\)',rest)
                    films.append(dict(title=tt,year=int(yy.group(1) or yy.group(2)) if yy else (ey or (int(ry.group(1)) if ry else None)),times=txt(re.sub(r'^\s*\((?:19|20)\d\d\)','',rest))))
            if not films: continue
            rng=pd(dtxt,y) if y else None
            blocks.append(dict(dates=dtxt,start=rng[0] if rng else None,end=rng[1] if rng else None,films=films))
            if not rng: gaps.append((fn,dtxt))
    if not blocks:
        T=txt(t); dm=re.search(r'([A-Z][a-z]+ \d+(?:\s*-\s*\d+)?,\s*(?:19|20)\d\d)',T)
        fl=re.findall(r'(\d{1,2}:\d\d)\s+([^()]+?)\s+\(((?:19|20)\d\d)\)',T)
        if dm and fl:
            r=pd(dm.group(1),y or 2000)
            blocks.append(dict(dates=dm.group(1),start=r[0] if r else None,end=r[1] if r else None,films=[dict(title=a.strip(),year=int(c),times=tm) for tm,a,c in fl]))
            gaps[:]=[g for g in gaps if g[0]!=fn]
    if not name or 'University Ave' in name or len(name)>100:
        name=re.sub(r'%20',' ',fn.rsplit('.',1)[0])
    for b in blocks:  # "... Special Appearance by" + person parsed as first film -> fold into header
        if b['films'] and re.search(r'\b(appearance|guest|in person|introduced|hosted|presented|conversation with)\b[^~]*\bby\s*$|\bwith\s*$',b['dates'],re.I) and not b['films'][0].get('year') and not b['films'][0].get('times'):
            who=b['films'].pop(0)['title']; d0=b['dates']; sc=re.search(r'schedule change',d0,re.I)
            d0=re.sub(r'\s*~\s*schedule change\s*~\s*',' ~ ',d0,flags=re.I); parts=[p.strip() for p in d0.split('~') if p.strip()]
            b['dates']=parts[0]+' – '+' '.join(parts[1:])+' '+who+(' (schedule change)' if sc else ''); b['guest']=who; b['guest_label']=re.sub(r'\s*by\s*$','',' '.join(parts[1:])).strip().title() or 'Special Appearance'
    for b in blocks:
        for fm in b['films']: fm['times']=re.sub(r'^\s*\((?:19|20)\d\d\)\s*','',fm['times']).strip()
    for b in [b for b in blocks if not b['start']]:
        m=re.search(r'(?:Starting|Beginning)\s+(?:\w+day\s+)?([A-Z][a-z]+ \d+)',b['dates'])
        if not m:
            m=re.search(r'(?:Starting|Beginning)\s+(?:\w+day\s+)?([A-Z][a-z]+ \d+)\s*:?\s*(?:<[^>]*>\s*)*'+re.escape(b['dates'][:20]),txt(t)) if b['dates'] else None
        r=pd(m.group(1),y) if m and y else None
        if r: b['start'],b['end']=r; b['dates']=m.group(1); b['films']=[f for f in b['films']]; gaps[:]=[g for g in gaps if g!=(fn,b['dates'])]
    note=[b for b in blocks if not b['start'] and all(f['title'].lower().startswith('superman') for f in b['films'])]
    for b in note:
        blocks.remove(b)
        star=any('*' in f['times'] for o in blocks for f in o['films'])
        for o in blocks:
            if not star and o['start']:
                a=dt.date.fromisoformat(o['start']); e=dt.date.fromisoformat(o['end'])
                if any((a+dt.timedelta(k)).weekday() in (3,4) for k in range((e-a).days+1)): o['short']='Thursday & Friday 7:30 show starts with an episode of the 1948 serial Superman'
            elif any(f['title'].startswith('*') or f['title'].endswith('*') or '*' in f['times'] for f in o['films']): o['short']='Preceded by the 1948 serial Superman'
    gaps[:]=[g for g in gaps if g[0]!=fn or any(b['dates']==g[1] and not b['start'] for b in blocks) or g[1]=='no bills parsed']
    MO=r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\.?'
    D=MO+r'\s*\d{1,2}(?!\d)(?:\s*(?:[-–—]|through|to)\s*(?:'+MO+r'\s*)?\d{1,2}(?!\d))?(?:,?\s*(?:19|20)\d\d)?'
    name=re.sub(r'(?:(?:Starting|Beginning)\s+(?:\w+day\s+)?)?\b'+D+r'(?:\s+through\b)?',' ',name)
    for _ in range(2): name=re.sub(r'\s+(?:through|Starting(?:\s+\w+day)?|Beginning|Every \w+day(?: through \w+day)?(?: in)?|,)\s*$','',name)
    name=re.sub(r'\s+,',',',re.sub(r'\s+',' ',name)).strip(' ,:;-–—~')
    if ov.get('name'): name=ov['name']
    if blocks: F.append(dict(name=name or fn.rsplit('.',1)[0],file=fn,year=y,blocks=blocks,start=min((b['start'] for b in blocks if b['start']),default=None),end=max((b['end'] for b in blocks if b['end']),default=None)))
    else: gaps.append((fn,'no bills parsed'))
for _src in [x for x in F if OV.get(x['file'].rsplit('.',1)[0].replace('%20',' '),{}).get('merge_into')]:
    _t=[x for x in F if x['file']==OV[_src['file'].rsplit('.',1)[0].replace('%20',' ')]['merge_into']]
    if not _t: continue
    _t=_t[0]; F.remove(_src); _t.setdefault('extra_files',[]).append(_src['file'])
    for _b in _src['blocks']:
        if not any(_b['start']==o['start'] for o in _t['blocks']): _t['blocks'].append(_b)
    _t['end']=max([o['end'] for o in _t['blocks'] if o['end']],default=_t['end'])
os.makedirs('stanford-site/data',exist_ok=True)
json.dump(dict(festivals=F,gaps=gaps),open('stanford-site/data/festivals.json','w'),ensure_ascii=False)
print(len(F),'festivals',sum(len(x['blocks']) for x in F),'bills')
print('range',min(x['start'] for x in F if x['start']),max(x['end'] for x in F if x['end']))
print('gaps',len(gaps),gaps[:25])
for x in sorted(F,key=lambda x:x['start'] or '')[:4]+sorted(F,key=lambda x:x['start'] or '')[-3:]: print(repr(x['name'][:70]),x['file'],x['start'],x['end'],len(x['blocks']))
