import json,urllib.request,urllib.parse,time,os,re
UA={'User-Agent':'StanfordTheatreFanSite/1.0 (jarroddellachiesa@users.noreply.github.com)'}
C='tools/wp_full_cache.json'; cache=json.load(open(C)) if os.path.exists(C) else {}
CM=json.load(open('data/cover_meta.json'))
n=0
for k,v in CM.items():
    wt=v['wt']
    if wt in cache: continue
    u='https://en.wikipedia.org/w/api.php?'+urllib.parse.urlencode(dict(action='query',format='json',titles=wt,prop='extracts',explaintext=1,exsectionformat='wiki',redirects=1))
    for i in range(3):
        try:
            r=json.load(urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=40)); cache[wt]=list(r['query']['pages'].values())[0].get('extract',''); break
        except Exception: time.sleep(3)
    n+=1; time.sleep(0.25)
    if n%50==0: json.dump(cache,open(C,'w'))
json.dump(cache,open(C,'w'))
def sections(t):
    out={}; cur='_'; buf=[]
    for line in t.split('\n'):
        m=re.match(r'^(=+)\s*(.*?)\s*\1$',line)
        if m: out.setdefault(cur,[]).append('\n'.join(buf)); cur=m.group(2).lower(); buf=[]
        else: buf.append(line)
    out.setdefault(cur,[]).append('\n'.join(buf)); return {k:'\n'.join(v).strip() for k,v in out.items()}
SENT=lambda x:[s.strip() for s in re.split(r'(?<=[a-z0-9)]{2}[.!?])\s+(?=[A-Z"])',re.sub(r'\s+',' ',x)) if 40<=len(s.strip())<=320]
LOCRE=re.compile(r'\b(filmed|shot|filming took place|principal photography|on location|location shooting|sound ?stages?|backlot)\b',re.I)
BADS=re.compile(r'^(This|These|That|Those|It|Its|He|She|They|His|Her|Their|However|But|Also|Although|In addition|Meanwhile|Instead|Later|Then|There|Such|Both|Here|As a result|Nevertheless|Despite this|The latter|The former|When|While|After this|Afterwards)\b')
W={}
for k,v in CM.items():
    S=sections(cache.get(v['wt'],''))
    prod=' '.join(S[s] for s in S if re.search(r'production|development|filming|casting|background|writing',s))
    loc=[s for s in SENT(' '.join(S[s] for s in S if re.search(r'production|filming|location',s))) if LOCRE.search(s) and re.search(r'\b(in|at|on)\s+(the\s+)?[A-Z]',s) and not BADS.match(s)][:3]
    triv=[s for s in SENT(prod) if not LOCRE.search(s) and not BADS.match(s) and s[0].isalnum() and '[' not in s][:3]
    W[k]=dict(loc=loc,trivia=triv)
json.dump(W,open('data/cover_wpfacts.json','w'),indent=0,ensure_ascii=False)
print('fetched',n,'loc',sum(1 for v in W.values() if v['loc']),'trivia',sum(1 for v in W.values() if v['trivia']))
