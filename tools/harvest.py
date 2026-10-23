import re,html,json,glob,datetime as dt
M={m:i for i,m in enumerate("January February March April May June July August September October November December".split(),1)}
def D(y,m,d):
    try: return dt.date(y,m,d)
    except: return None
def pdate(s,yr):
    s=s.replace('–','-').replace('—','-'); s=re.sub(r'\s+',' ',s).strip()
    rx=r'([A-Z][a-z]+)\.? (\d+)(?:, (\d{4}))?(?: ?- ?(?:([A-Z][a-z]+)\.? )?(\d+))?(?:, (\d{4}))?'
    m=re.match(rx,s)
    if not m or m.group(1) not in M: return None
    m1,d1,y1,m2,d2,y2=m.groups(); y1=int(y1 or y2 or yr); y2=int(y2 or y1)
    a=D(y1,M[m1],int(d1))
    if m2 and m2 not in M: return None
    b=D(y2 if y2!=y1 or not m2 or M.get(m2,0)>=M[m1] else y1+1, M[m2] if m2 else M[m1], int(d2)) if d2 else a
    if a and b and b<a and not m2: b=D(a.year+1 if a.month==12 else a.year,(a.month%12)+1,int(d2))
    return (a,b) if a and b else None
out=[];skipped=[]
for f in sorted(glob.glob('cache/years/*.htm')):
    yr=int(f[-8:-4]); t=open(f,encoding='utf-8',errors='replace').read()
    cur=None
    for cls,txt in re.findall(r'<div class="(date|film|notes)">(.*?)</div>',t,re.S):
        txt=html.unescape(re.sub(r'<[^>]+>','',txt)).replace('\u2003',' ')
        txt=re.sub(r'\s+',' ',txt).strip()
        if cls=='date':
            raw=re.sub(r'\s*\(.*$','',txt); cur=pdate(raw,yr); curraw=txt
            if not cur: skipped.append(('date',yr,txt))
        elif cls=='film' and txt:
            if not cur: skipped.append(('film-no-date',yr,txt)); continue
            m=re.match(r'^(.*?)\s*\(([^()]*)\)\s*$',txt)
            title,extra=(m.group(1),m.group(2)) if m else (txt,'')
            out.append(dict(title=title,note=extra,start=cur[0].isoformat(),end=cur[1].isoformat(),date_text=curraw,source='Stanford Theatre history page',url=f'history/years/{yr}.htm'))
# Tile: full history for current films
for f in sorted(glob.glob('tile/*.html')):
    t=html.unescape(re.sub(r'<[^>]+>','\n',open(f).read())); L=[x.strip() for x in t.split('\n') if x.strip()]
    title=L[L.index('Tile Program')+1]; pair=None; runs={}
    i=0
    while i<len(L):
        if L[i]=='Plays alone': pair=[]
        elif L[i]=='Plays with':
            pair=[];j=i+1
            while not re.fullmatch(r'\d+',L[j]): pair.append(L[j]); j+=1
            i=j; continue
        if i+4<len(L) and re.fullmatch(r'\d+',L[i]) and re.fullmatch(r"[A-Z][a-z]{2} \d+ '\d\d",L[i+1]):
            mo,dd,yy=re.match(r"(\w+) (\d+) '(\d\d)",L[i+1]).groups(); y=int(yy); y+=1900 if y>=80 else 2000
            d=dt.datetime.strptime(f"{mo} {dd} {y}","%b %d %Y").date()
            r=runs.setdefault(L[i],dict(title=title,pair=pair,dates=[],tickets=0))
            r['dates'].append(d); r['tickets']+=int(L[i+3].replace(',',''))
            i+=5; continue
        i+=1
    q=title.replace(' ','+')
    for pid,r in runs.items():
        out.append(dict(title=title,note=('w/ '+', '.join(r['pair'])) if r['pair'] else '',start=min(r['dates']).isoformat(),end=max(r['dates']).isoformat(),days=len(r['dates']),tickets=r['tickets'],source='Tile',url=f'https://tile.stanfordtheatre.org/tile?q={q}'))
# dedupe title+start
seen=set();ded=[]
for o in sorted(out,key=lambda o:(o['source']!='Tile',o['start'])):
    k=(o['title'].lower(),o['start'])
    if k in seen: continue
    seen.add(k);ded.append(o)
ded.sort(key=lambda o:o['start'])
json.dump(ded,open('stanford-site/data/showings.json','w'),ensure_ascii=False)
from collections import Counter
print(Counter(o['source'] for o in ded)); 
for s in ['Tile','Stanford Theatre history page']:
    x=[o for o in ded if o['source']==s]; print(s,x[0]['start'],x[-1]['start'])
print('skipped',len(skipped),skipped[:15])
