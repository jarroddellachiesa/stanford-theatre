import json,collections,re,sys
sys.path.insert(0,'tools')
d=json.load(open('data/showings.json'))
G=collections.defaultdict(list)
for x in d: G[x['run'].rsplit('|',1)[0]].append(x)
BAD=re.compile(r'\b(news|cartoons?|matinee|vitaphone|march of time|vaudeville|sportlight|aesop|midnight show|serial|newsreel|acts?|organ|short subjects?|shorts|intermission|preview|program|benefit|closed|travelogue|comedy reel|chapter|kinograms|amateur night)\b',re.I)
def NK(t):
    import unicodedata
    t=unicodedata.normalize('NFKD',t).encode('ascii','ignore').decode().lower()
    t=re.sub(r"[^a-z0-9 ]","",t.replace('&','and')); t=re.sub(r'\b(the|a|an|and)\b',' ',t); t=re.sub(r'ing\b','in',t)
    return ' '.join(t.split())
FJ=json.load(open('data/festivals.json'))['festivals']
Y=collections.defaultdict(collections.Counter); TT={}
for fe in FJ:
  for b in fe['blocks']:
    for fm in b['films']:
      if fm.get('year'): Y[NK(fm['title'])][fm['year']]+=1; TT.setdefault(NK(fm['title']),fm['title'])
keys=[k for k in G if not BAD.search(k) and not BAD.search(G[k][0]['title']) and any(x['source']!='Stanford Theatre history page' for x in G[k])]
nr=lambda k:len({x['run'] for x in G[k] if x['source']!='Stanford Theatre history page'}); tk=lambda k:sum(x.get('tickets') or 0 for x in G[k])
rank=sorted(keys,key=lambda k:(-nr(k),-tk(k)))
TOPN=500
top=rank[:TOPN]; recent=[k for k in keys if any(x['start']>='2021-10-01' for x in G[k])]
import os
PREV=[o['key'] for o in json.load(open('data/cover.json'))] if os.path.exists('data/cover.json') else []
_CM=json.load(open('data/cover_meta.json')) if os.path.exists('data/cover_meta.json') else {}
keep=[k for k in dict.fromkeys(PREV+list(_CM)) if k in G]  # never drop an existing page: anything once covered (has metadata) stays
# every Hitchcock-directed / John Wayne film that played a festival (data/rule_people.json, from tools/rule_people.py)
PEOPLE=json.load(open('data/rule_people.json')) if os.path.exists('data/rule_people.json') else []
def _fy(k):
    if '#' in k: return [int(k.split('#')[1])]
    return [y for y,_ in Y[k.split('#')[0]].most_common()] if Y[k.split('#')[0]] else []
people=[]; PWHY={}
for k in keys:
    b=k.split('#')[0]
    for p in PEOPLE:
        if NK(p['title'])==b and (any(abs(a-c)<=1 for a in _fy(k) for c in p['years']) or not _fy(k)):  # no festival year: title match only
            people.append(k); PWHY[k]=p['why']+' '+p['qid']; break
out=[]
MINRUNS=3  # also every festival film with at least this many runs
many=[k for k in keys if nr(k)>=MINRUNS]
for k in dict.fromkeys(top+recent+keep+people+many):
    yr=int(k.split('#')[1]) if '#' in k else (Y[k].most_common(1)[0][0] if Y[k] else None)
    if yr is None:  # history: first showing year as upper bound
        pass
    t=TT.get(k) or collections.Counter(x['title'] for x in G[k]).most_common(1)[0][0]
    out.append(dict(key=k,title=t,year=yr,first=min(x['start'] for x in G[k]),runs=nr(k),top=k in top,recent=k in recent,people=PWHY.get(k),yrs=dict(Y[k])))
json.dump(out,open('data/cover.json','w'),indent=0)
print(len(top),len(recent),len(out),sum(1 for o in out if not o['year']))
print([o['title'] for o in out if not o['year']][:40])
print(top[-1],nr(top[-1]))
