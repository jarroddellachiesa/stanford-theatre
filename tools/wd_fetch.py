# Cache Wikidata films (feature Q11424 / short Q24862) by release year, en labels+aliases -> tools/wd_films/
import json,urllib.request,urllib.parse,time,os,sys
Q='''SELECT ?f ?l ?d WHERE {{ ?f wdt:P31 wd:{t}; wdt:P577 ?d. FILTER(?d >= "{y}-01-01"^^xsd:dateTime && ?d < "{y1}-01-01"^^xsd:dateTime) ?f {p} ?l. FILTER(LANG(?l)="en") }}'''
os.makedirs('wd_films',exist_ok=True)
for y in range(int(sys.argv[1]),int(sys.argv[2])):
  for t in ('Q11424','Q24862'):
   for p in ('rdfs:label','skos:altLabel'):
    fn=f'wd_films/{y}_{t}_{p[:4]}.json'
    if os.path.exists(fn): continue
    for a in range(4):
        try:
            u='https://query.wikidata.org/sparql?format=json&query='+urllib.parse.quote(Q.format(y=y,y1=y+1,t=t,p=p))
            b=json.load(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'StanfordTheatreFanSite/1.0 (jarrod@dellachiesa.us)'}),timeout=70))['results']['bindings']
            json.dump([[x['f']['value'].rsplit('/',1)[1],x['l']['value'],x['d']['value'][:10]] for x in b],open(fn,'w')); print(fn,len(b),flush=True); break
        except Exception as ex: print(fn,'err',ex,flush=True); time.sleep(15)
    time.sleep(1)
