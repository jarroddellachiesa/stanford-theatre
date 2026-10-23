import re,html,json,os,time,urllib.request,urllib.parse,glob
UA={'User-Agent':'StanfordSiteIndexer/1.0 (personal archive; polite)'}
def get(u): return urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=40).read().decode('utf-8','replace')
def fn(q): return 'cache/tileq/'+re.sub(r'[^A-Za-z0-9]+','_',q)[:120]+'.html'
cal=set()
for f in glob.glob('cache/cal/*'):
    for a in re.findall(r'<a [^>]*imdb[^>]*>([^<]{2,100})</a>',open(f,errors='replace').read()):
        t=re.sub(r'\s*\((?:19|20)\d\d\)\s*$','',html.unescape(a).strip()).strip()
        if t: cal.add(t)
hist=set(o['title'] for o in json.load(open('stanford-site/data/showings.json')) if o['source']!='Tile')
queue=sorted(cal)+sorted(hist-cal); done=set(); fails={}
json.dump({'cal':sorted(cal),'hist':sorted(hist)},open('cache/titlelist.json','w'))
print('cal',len(cal),'hist',len(hist),flush=True)
def partners(t):
    L=[x.strip() for x in html.unescape(re.sub(r'<[^>]+>','\n',t)).split('\n') if x.strip()];o=[]
    for i,x in enumerate(L):
        if x=='Plays with':
            j=i+1
            while j<len(L) and not re.fullmatch(r'\d+',L[j]): o.append(L[j]); j+=1
    return o
for rnd in range(4):
    i=0
    while i<len(queue):
        q=queue[i]; i+=1
        if q in done: continue
        f=fn(q)
        if not os.path.exists(f):
            try: open(f,'w').write(get('https://tile.stanfordtheatre.org/tile?q='+urllib.parse.quote_plus(q)))
            except Exception as e:
                fails[q]=str(e); time.sleep(2); continue
            time.sleep(1.5)
        done.add(q); fails.pop(q,None)
        for p in partners(open(f,errors='replace').read()):
            if p not in done and p not in queue: queue.append(p)
        if i%100==0: print(rnd,i,len(queue),len(fails),flush=True)
    json.dump(fails,open('cache/tile_fails.json','w'))
    print('round',rnd,'fails',len(fails),flush=True)
    if not fails: break
    time.sleep(60)
print('DONE',len(done),flush=True)
