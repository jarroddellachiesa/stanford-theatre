# Tag each Original Run showing: feature / short / newsreel / vaudeville/stage act / special event / unknown
# Wikidata cache: tools/wd_films (wd_fetch.py). Output: data/entry_types.json  {"title|start": type}
import json,re,glob,unicodedata as ud,os,collections
os.chdir(os.path.dirname(os.path.abspath(__file__))+'/..')
def N(t):
    t=ud.normalize('NFD',str(t)); t=''.join(c for c in t if not ud.combining(c)).lower().replace('&',' and ')
    t=re.sub(r"['’`]",'',t); return ' '.join(x for x in re.sub(r'[^a-z0-9]+',' ',t).split() if x not in('the','a','an'))
def clean(t):
    t=re.sub(r'^(week \d+( & \d+)?|plus|also|extra!?|new|latest)\s*[-:]?\s*','',t,flags=re.I)
    t=re.sub(r'\s*\((?:19|20)\d\d\)\s*$','',t); t=re.sub(r'\s*[\(—–;].*$','',t) if not re.match(r'^[^(]*\)$',t) else t
    return t.strip(' "-:')
W=collections.defaultdict(list)
for f in glob.glob('tools/wd_films/*.json'):
    typ='short' if 'Q24862' in f else 'feature'
    for q,l,d in json.load(open(f)): W[N(l)].append((int(d[:4]),typ,q))
RS=[('special event',r'pictures? of|game pictures|football|fight pictures|fight highlights|\bfight\b(?! for)|highlights|rose bowl|track meet|homecoming|lindbergh|election|amateur ni|contest|benefit|kiddie|costume party|eve party|spook pa|midnite show|race night|rodeo|broadcast|twist|yo yo|clown suit|frosh|first pictures|royal wedding|olympic records|frankenstein.*in person|in person.*monster|monster in person|stanford.*(game|cal)\b'),
    ('newsreel',r'\bnews\b|newsreel|kinogram|path[eé]|metrotone|movietone|march of time|scoop|first scenes|news events'),
    ('vaudeville/stage act',r'vaudeville|on stage|on the stage|stage!|in person|live (on stage|play)|stage show|revue|varieties|orchestra|\bband\b|organist|\bacts?\b|follies|marionette|s[eé]ance|songsters|comedy (skit|sketch)|talking act|gang\b.*clown'),
    ('short',r'cartoons?\b|\bshorts?\b|serial|travelogue|vitaphone|sportlight|featurette|our gang|stooges|little rascals|silly symphony|novelty|comedies')]
# manual review overrides (title -> type)
OVR={**{t:'short' for t in ["First to Fight","Football for the Fan","Developing a Football Team","How to Play Football","How to See a Football Game","Rockne's Football","Football 40 Years Ago","Buffalo Bill's Fight","Norman Sper's \"Football This Week\"","Cockeyed News","Live News","The News Hound","Mickey's Band Concert","Mickey's Revue","Marionettes—A Sound Cartoon","6 band shorts","Alum & Eve","The Baby Follies","Selection of short subjects (Educational studios);","Svensen's Wild Party","Whoopee Party","Necking Party","The Pajama Party","Strife of the Party","His Birthday Party","Betty Boop's May Party","The Kiddies' Revue","Vitaphone short: Artie Shaw and his Orchestra"]},
     **{t:'feature' for t in ["Ziegfeld Follies of 1945","Fox Follies of 1929","Follies Bergere"]},
     'Walt Disney\'s Academy Award Revue (Academy Award winning':'short',
     'Century Fox Studio (not a newsreel)."':'special event'}
WS=json.load(open('tools/wd_search.json')) if os.path.exists('tools/wd_search.json') else {}
SH=json.load(open('data/showings.json')); OUT={}; how=collections.Counter()
for o in SH:
    if o.get('badge')!='Original Run': continue
    t=o['title']; y=int(o['start'][:4]); note=(o.get('note') or '')
    k=N(clean(t)); hits=[h for h in W.get(k,[]) if y-3<=h[0]<=y+1] if k else []
    typ=None
    if hits:
        h=min(hits,key=lambda h:(h[1]!='feature',abs(y-h[0]))); typ=h[1]; how['wikidata']+=1
        if re.search(r'\bshort\b|cartoon|mickey mouse|silly symphony|specialty',note,re.I) and typ=='feature': typ='short'
    if not typ:
        for d_,l_,q_ in WS.get(clean(t),[]):
            m_=re.search(r'\b(19[1-6]\d)\b.*\b(film|cartoon|short)',d_,re.I)
            if m_ and N(l_)==k and y-3<=int(m_.group(1))<=y+1:
                typ='short' if re.search(r'short|cartoon',d_,re.I) else 'feature'; how['wbsearch']+=1; break
        if typ and typ=='feature' and re.search(r'\bshort\b|cartoon|mickey mouse|silly symphony|specialty',note,re.I): typ='short'
    if not typ:
        for tp,rx in RS:
            if re.search(rx,t,re.I): typ=tp; break
        if not typ and re.match(r'^[A-Z][a-z]+ & [A-Z][a-z]+\b',t): typ='vaudeville/stage act'
        if typ: how['keyword']+=1
        elif re.fullmatch(r'\s*(newsreel|comedy short|short|.*comedy short|cartoon|mickey mouse.*|silly symphony)\s*',note,re.I): typ='newsreel' if 'news' in note.lower() else 'short'; how['note']+=1
        else: typ='unknown'
    if re.match(r'^chapter \d+',t,re.I) and typ=='unknown': typ='short'
    typ=OVR.get(t,typ)
    OUT[t+'|'+o['start']]=typ
json.dump(OUT,open('data/entry_types.json','w'),ensure_ascii=False,indent=0,sort_keys=True)
print(collections.Counter(OUT.values()),how)
