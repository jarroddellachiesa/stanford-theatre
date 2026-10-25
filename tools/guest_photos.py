# Real photos for special-appearance guests: Wikidata P18 -> Wikimedia Commons (records source+license in data/guests.json)
import json,urllib.request,urllib.parse,re,os,sys
os.chdir(os.path.dirname(os.path.abspath(__file__))+'/..')
UA={'User-Agent':'StanfordTheatreFanSite/1.0 (jarrod@dellachiesa.us)'}
def J(u): return json.load(urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=30))
G=json.load(open('data/guests.json')) if os.path.exists('data/guests.json') else {}
names=sorted({b['guest'] for f in json.load(open('data/festivals.json'))['festivals'] for b in f['blocks'] if b.get('guest')})
for n in names:
    if n in G and G[n].get('img'): continue
    r=J('https://www.wikidata.org/w/api.php?action=wbsearchentities&format=json&language=en&limit=3&search='+urllib.parse.quote(n))['search']
    r=[x for x in r if re.search(r'actor|actress|director|singer|performer|composer|writer',x.get('description',''),re.I)]
    if not r: G[n]={'img':None,'note':'no Wikidata match'}; continue
    q=r[0]['id']; c=J(f'https://www.wikidata.org/wiki/Special:EntityData/{q}.json')['entities'][q]['claims']
    if 'P18' not in c: G[n]={'img':None,'wikidata':q,'note':'no P18 image'}; continue
    fn=c['P18'][0]['mainsnak']['datavalue']['value']
    ii=J('https://commons.wikimedia.org/w/api.php?action=query&format=json&prop=imageinfo&iiprop=url|extmetadata&iiurlwidth=400&titles='+urllib.parse.quote('File:'+fn))
    p=list(ii['query']['pages'].values())[0]['imageinfo'][0]; md=p['extmetadata']
    lic=md.get('LicenseShortName',{}).get('value',''); art=re.sub('<[^>]+>','',md.get('Artist',{}).get('value','')).strip()
    sl=re.sub(r'[^a-z0-9]+','-',n.lower()).strip('-'); out=f'img/guests/{sl}.jpg'
    open(out,'wb').write(urllib.request.urlopen(urllib.request.Request(p['thumburl'],headers=UA),timeout=60).read())
    G[n]={'img':out,'kind':'portrait (not from the appearance)','source':p['descriptionurl'],'license':lic,'credit':art,'wikidata':q}
    print(n,lic,art)
json.dump(G,open('data/guests.json','w'),indent=2,ensure_ascii=False)
