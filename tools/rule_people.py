# Fetch Wikidata films directed by Alfred Hitchcock (P57=Q7374) or with John Wayne in the cast (P161=Q40531).
# Output data/rule_people.json, used by tools/cover_pick.py to widen the film-page rule.
import json,urllib.request,urllib.parse
UA={'User-Agent':'StanfordTheatreFanSite/1.0 (jarroddellachiesa@users.noreply.github.com)'}
q='''SELECT ?f ?fl ?y ?who WHERE { VALUES (?p ?who ?v) {(wdt:P57 "Alfred Hitchcock (director)" wd:Q7374) (wdt:P161 "John Wayne (cast)" wd:Q40531)}
 ?f ?p ?v; wdt:P31/wdt:P279* wd:Q11424. ?f rdfs:label ?fl FILTER(lang(?fl)="en") OPTIONAL{?f wdt:P577 ?d} BIND(YEAR(?d) AS ?y)}'''
r=json.load(urllib.request.urlopen(urllib.request.Request('https://query.wikidata.org/sparql?format=json&query='+urllib.parse.quote(q),headers=UA),timeout=120))
L={}
for b in r['results']['bindings']:
    k=b['f']['value'].rsplit('/',1)[1]; o=L.setdefault(k,dict(qid=k,title=b['fl']['value'],why=b['who']['value'],years=[]))
    if 'y' in b and int(b['y']['value']) not in o['years']: o['years'].append(int(b['y']['value']))
for o in L.values(): o['years'].sort()
json.dump(sorted(L.values(),key=lambda o:(o['why'],o['title'])),open('data/rule_people.json','w'),indent=0,ensure_ascii=False)
print(len(L),'films')
