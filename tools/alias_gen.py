import json,re,collections,unicodedata,difflib
d=json.load(open('data/showings.json'))
def NK(t):
    t=unicodedata.normalize('NFD',t); t=''.join(c for c in t if not unicodedata.combining(c)).lower()
    t=re.sub(r'\s*\((?:19|20)\d\d\)\s*$','',t).replace('&',' and ')
    t=re.sub(r"['’`]",'',t); w=[x for x in re.sub(r'[^a-z0-9]+',' ',t).split() if x not in('the','a','an')]
    return ' '.join(w)
NUM={'1':'one','2':'two','3':'three','4':'four','5':'five','6':'six','7':'seven','8':'eight','9':'nine','10':'ten','12':'twelve','39':'thirty nine','100':'one hundred'}
AB={'mr':'mister','mrs':'missus','dr':'doctor','st':'saint','vs':'versus','pt':'part','ii':'2','iii':'3'}
def SK(t):
    t=re.sub(r'\([^)]*\)',' ',t); t=re.sub(r',\s*(the|a|an)\s*$','',t,flags=re.I)
    w=[AB.get(x,x) for x in NK(t).split() if x!='and']
    w=[NUM.get(x,x) for x in w]; s=' '.join(w)
    s=re.sub(r'in\b','ing',s)
    return s.replace(' ','')
src=collections.defaultdict(collections.Counter); dates=collections.defaultdict(list)
for o in d:
    src[o['title']][o['source']]+=1; dates[o['title']].append(o['start'])
byNK=collections.defaultdict(set)
for t in src: byNK[NK(t)].add(t)
byS=collections.defaultdict(set)
for k in byNK: byS[SK(next(iter(byNK[k])))].add(k)
def score(t):
    c=src[t]; return (c['Stanford Theatre calendars']*3+c['Tile']*2+c['Stanford Theatre history page'], not t.isupper(), '(' not in t)
AL={};groups=[]
for s,ks in byS.items():
    titles={t for k in ks for t in byNK[k]}
    if len(titles)<2: continue
    canon=max(titles,key=score)
    for t in titles:
        if t!=canon: AL[t]=canon
    if len(ks)>1: groups.append(sorted(titles))
# fuzzy candidates (questions, not merged)
keys=sorted(byS); Q=[]
import itertools
bylen=collections.defaultdict(list)
for k in keys: bylen[len(k)].append(k)
for k in keys:
    if len(k)<9: continue
    for L in (len(k),len(k)+1):
        for k2 in bylen[L]:
            if k2<=k and L==len(k): continue
            r=difflib.SequenceMatcher(None,k,k2).ratio()
            if r>=0.93: Q.append((k,k2))
print('raw titles',len(src),'NK keys',len(byNK),'after SK',len(byS),'aliases',len(AL),'new merges',len(groups),'fuzzy Q',len(Q))
for g in groups[:40]: print(' MERGE',g)
json.dump(dict(groups=groups,Q=Q),open('/workspace/alias_work.json','w'))
