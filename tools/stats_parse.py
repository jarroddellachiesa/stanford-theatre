# Parse cached Tile per-film stats pages (cache/tileq, tile/) -> PRIVATE /workspace/private/stanford_stats.json (never commit)
import re,html,json,glob,datetime as dt,os
OUT=os.environ.get('STATS_PRIVATE','/workspace/private/stanford_stats.json')
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
            d=dt.datetime.strptime(f"{mo} {dd} {y}","%b %d %Y").date().isoformat()
            num=lambda s:int(re.sub(r'[^\d]','',s) or 0)
            r=runs.setdefault(L[i],dict(prog=L[i],pair=list(pair),days=[]))
            r['days'].append([d,L[i+2],num(L[i+3]),num(L[i+4])]); i+=5; continue
        i+=1
    return title,list(runs.values())
S={}
for f in glob.glob('/workspace/cache/tileq/*.html')+glob.glob('/workspace/tile/*.html'):
    t,r=parse(open(f,errors='replace').read())
    if t and r: S[t]=sorted(r,key=lambda x:x['days'][0][0])
os.makedirs(os.path.dirname(OUT),exist_ok=True); json.dump(S,open(OUT,'w')); os.chmod(OUT,0o600)
print('films',len(S),'runs',sum(len(v) for v in S.values()),'days',sum(len(r['days']) for v in S.values() for r in v))
