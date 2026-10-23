import json
p='stanford-site/data/showings.json'; d=json.load(open(p))
FY={'north by northwest':1959,'on the waterfront':1954,'mary poppins':1964,'the wizard of oz':1939}
seen=set()
for o in sorted(d,key=lambda o:o['start']):
    o['badge']=''
    if o['source']=='Tile': o['label']='Tile'; continue
    o['label']='Original billings'
    k=o['title'].strip().lower()
    if k in seen: continue
    seen.add(k); y=FY.get(k)
    if y is None or int(o['start'][:4])-y<=2: o['badge']='Original Run'
json.dump(d,open(p,'w'),ensure_ascii=False); open('stanford-site/data/showings.js','w').write('window.SHOWINGS='+json.dumps(d,ensure_ascii=False)+';')
print(sum(1 for o in d if o['badge']),len(d))
