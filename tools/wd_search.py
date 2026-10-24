# wbsearchentities lookup for titles still 'unknown'; cache tools/wd_search.json  {query: [[desc,label],...]}
import json,urllib.request,urllib.parse,time,os,sys
sys.path.insert(0,os.path.dirname(__file__)); os.chdir(os.path.dirname(os.path.abspath(__file__)))
C=json.load(open('wd_search.json')) if os.path.exists('wd_search.json') else {}
ET=json.load(open('../data/entry_types.json')); import re
from entry_types_clean import clean
qs=sorted({clean(k.split('|')[0]) for k,v in ET.items() if v=='unknown'}-set(C))
for i,q in enumerate(qs):
    if len(q)<2: C[q]=[]; continue
    try:
        u='https://www.wikidata.org/w/api.php?action=wbsearchentities&format=json&language=en&type=item&limit=10&search='+urllib.parse.quote(q)
        r=json.load(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'StanfordTheatreFanSite/1.0 (jarrod@dellachiesa.us)'}),timeout=30))
        C[q]=[[x.get('description',''),x.get('label',''),x['id']] for x in r.get('search',[])]
    except Exception as ex: print(q,ex); time.sleep(5)
    if i%50==0: json.dump(C,open('wd_search.json','w')); print(i,len(qs),flush=True)
    time.sleep(0.3)
json.dump(C,open('wd_search.json','w'))
