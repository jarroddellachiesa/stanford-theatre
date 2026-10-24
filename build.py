import json,html,datetime,urllib.parse
src=open('/workspace/stanford-infographics/gen.py').read(); ns={}
exec(src[:src.index('CSS=')],ns); F={f['slug']:f for f in ns['F']}
T=json.load(open('/workspace/tile.json'))
K={'north-by-northwest':'N','on-the-waterfront':'W','mary-poppins':'P','the-wizard-of-oz':'O'}
IMDB={'N':'tt0053125','W':'tt0047296','P':'tt0058331','O':'tt0032138'}
TQ={'N':'North+by+Northwest','W':'On+the+Waterfront','P':'Mary+Poppins','O':'Wizard+of+Oz'}
EMS="https://www.stanfordtheatre.org/calendars/Eva%20Marie%20Saint.html"; PW="https://www.stanfordtheatre.org/calendars/Poppins%20Wizard%202026.html"
FEST=[("Remembering Eva Marie Saint","Oct 16–25, 2026",EMS,[("October 23–25",[("north-by-northwest","7:30 (plus 3:00 Sat/Sun)"),("on-the-waterfront","5:30, 10:00")])],["north-by-northwest","on-the-waterfront"]),
("Mary Poppins / The Wizard of Oz","Oct 29–Nov 8, 2026",PW,[("October 29–November 1",[("mary-poppins","7:30 (plus 3:05 Sat/Sun)"),("the-wizard-of-oz","5:35, 10:00")]),("November 5–8",[("mary-poppins","7:30 (plus 3:05 Sat/Sun)"),("the-wizard-of-oz","5:35, 10:00")])],["mary-poppins","the-wizard-of-oz"])]
MAP="https://www.google.com/maps/search/?api=1&query=Stanford+Theatre%2C+221+University+Ave%2C+Palo+Alto%2C+CA+94301"
e=html.escape
SLUG={EMS:'remembering-eva-marie-saint',PW:'mary-poppins-the-wizard-of-oz'}
def page(title,body,root="",act=""):
    A=lambda k:' class="on" aria-current="page"' if k==act else ""
    return f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(title)}</title><link rel="stylesheet" href="{root}style.css"><link rel="icon" href="{root}favicon.ico" sizes="any"><link rel="icon" type="image/png" sizes="32x32" href="{root}icons/favicon-32.png"><link rel="apple-touch-icon" href="{root}icons/apple-touch-icon.png?v=3"><link rel="manifest" href="{root}manifest.webmanifest"><meta name="theme-color" content="#5a0e18"><meta name="apple-mobile-web-app-capable" content="yes"><meta name="mobile-web-app-capable" content="yes"><meta name="apple-mobile-web-app-title" content="Stanford"><meta name="apple-mobile-web-app-status-bar-style" content="black-translucent"><script>if("serviceWorker" in navigator)addEventListener("load",function(){{navigator.serviceWorker.register("{root}sw.js")}})</script></head><body>
<header class="mq"><a href="{root}index.html"><div class="m1">THE STANFORD THEATRE</div></a><nav class="nav"><a href="{root}index.html"{A("now")}>Now Showing</a><a href="{root}upcoming.html"{A("up")}>Upcoming</a><a href="{root}past.html"{A("past")}>Past</a><a href="{root}search.html"{A("search")}>Search</a></nav></header><main>{body}</main>
<footer><address class="addr"><a href="{MAP}"><span class="an1">Stanford Theatre</span><br>221 University Avenue<br>Palo Alto, CA 94301</a></address></footer></body></html>'''
def ft(s): f=F[s]; return f"{e(f['t'])} ({f['y']})"

import datetime as _dt, zoneinfo as _zi
TODAY=_dt.datetime.now(_zi.ZoneInfo('America/Los_Angeles')).date().isoformat()
NB=[(EMS,"October 16–18","2026-10-16","2026-10-18",[("north-by-northwest","7:30 (plus 3:00 Sat/Sun)"),("on-the-waterfront","5:30, 10:00")]),
(EMS,"October 23–25","2026-10-23","2026-10-25",[("north-by-northwest","7:30 (plus 3:00 Sat/Sun)"),("on-the-waterfront","5:30, 10:00")]),
(EMS,"October 30-November 1","2026-10-30","2026-11-01",None),
(PW,"October 29–November 1","2026-10-29","2026-11-01",[("mary-poppins","7:30 (plus 3:05 Sat/Sun)"),("the-wizard-of-oz","5:35, 10:00")]),
(PW,"November 5–8","2026-11-05","2026-11-08",[("mary-poppins","7:30 (plus 3:05 Sat/Sun)"),("the-wizard-of-oz","5:35, 10:00")])]
import re as _re0
_MF0={k:v for v in "January February March April May June July August September October November December".split() for k in (v[:3],v[:4])}
def _sp(t):
    t=_re0.sub(r'\b(Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)\b\.?(?=\s*\d)',lambda m:_MF0.get(m.group(1),m.group(1)),t)
    return _re0.sub(r'\s*[-–—]\s*',' - ',t)
def _dr(t,a,b):
    f=_sp(t)
    if len(f)<=38: return f
    A=_dt.date.fromisoformat(a);B=_dt.date.fromisoformat(b);g=lambda d:f"{d.month}/{d.year%100:02d}"
    return g(A)+' - '+g(B)
_rng={u:(min(b[2] for b in NB if b[0]==u),max(b[3] for b in NB if b[0]==u)) for u in {b[0] for b in NB}}
FEST=[(n,_dr(d,*_rng[u]),u,[(_sp(g),it) for g,it in gs],fl) for n,d,u,gs,fl in FEST]
NB=[(u,_sp(l),a,b,it) for u,l,a,b,it in NB]
_MN='January|February|March|April|May|June|July|August|September|October|November|December'
def DT(t):
    t=_re0.sub(r'\b(Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)\b\.?(?=\s*\d)',lambda m:_MF0.get(m.group(1),m.group(1)),t)
    return _re0.sub(r'\b(('+_MN+r') \d{1,2})\s*[–—-]\s*(?=\d|(?:'+_MN+r') )',r'\1 - ',t)
FN={x[2]:(x[0],x[1]) for x in FEST}
NB=[b for b in NB if b[4] or not any(o[0]!=b[0] and o[4] and o[2]<=b[3] and b[2]<=o[3] for o in NB)]
def blk(b):
    url,lab,st,en,items=b; nm,dr=FN[url]; sl=SLUG[url]
    head=f'<div class="bf"><div class="dr dtop">{dr}</div><h2><a href="festivals/{sl}.html">{e(nm)}</a></h2></div>'
    if items:
        body='<div class="cols">'+"".join(f'<div class="col"><a class="card" href="films/{s}.html"><img src="posters/{s}.jpg" alt="{e(F[s]["t"])} poster"><span>{ft(s)}</span><small>{F[s]["rt"]} min</small></a><div class="tm">{t}</div></div>' for s,t in items)+'</div>'
    else: body='<p class="tba">To Be Announced</p>'
    return f'<section class="fest blk" data-start="{st}" data-end="{en}" data-fest="{sl}">{head}<h3 class="bl">{lab}</h3>{body}</section>'
live=sorted([b for b in NB if b[3]>=TODAY],key=lambda b:b[2])
JSF="""<script>(function(){var t=new Intl.DateTimeFormat('en-CA',{timeZone:'America/Los_Angeles'}).format(new Date());
var all=[].slice.call(document.querySelectorAll('.blk'));all.forEach(function(b){if(b.dataset.end<t)b.remove();});
var r=[].slice.call(document.querySelectorAll('.blk')).sort(function(a,b){return a.dataset.start<b.dataset.start?-1:1;});
var M=document.body.dataset.mode;
if(M==='now'){r.slice(1).forEach(function(b){b.remove();});}else if(r[0])r[0].remove();
document.querySelectorAll('.fgrp').forEach(function(g){if(!g.querySelector('.blk'))g.remove();});
var em=document.getElementById('empty');if(em&&!document.querySelector('.blk'))em.style.display='block';})();</script>"""
h=['<section id="now"><h1 class="mqh">Now Showing</h1>']+[blk(b) for b in live]+['<p id="empty" class="sm" style="display:none;text-align:center">Nothing scheduled right now — see <a href="past.html">Past</a>.</p></section>',JSF]
open('index.html','w').write(page("Stanford Theatre — Now Showing","".join(h),"","now").replace('<body>','<body data-mode="now">',1))
u=['<section id="upcoming"><h1 class="mqh">Upcoming</h1>']
for name,dr,url,groups,films in FEST:
    bs=[b for b in live if b[0]==url]
    if bs: u.append(f'<div class="fgrp" data-fest="{SLUG[url]}"><div class="dr dtop">{dr}</div><h2 class="gh"><a href="festivals/{SLUG[url]}.html">{e(name)}</a></h2>'+"".join(blk(b) for b in bs)+'</div>')
u+=['<p id="empty" class="sm" style="display:none;text-align:center">No further programs announced yet.</p></section>',JSF]
open('upcoming.html','w').write(page("Stanford Theatre — Upcoming","".join(u),"","up").replace('<body>','<body data-mode="up">',1))
P=['<section id="past"><h1 class="mqh">Past</h1><p class="sm" style="text-align:center">Finished programs, newest first.</p>']
for b in sorted(NB,key=lambda b:b[3],reverse=True):
    x=blk(b).replace('<section class="fest blk"','<section class="fest blk pastb'+('' if b[3]<TODAY else ' hid')+'"',1)
    P.append(x)
FJ=json.load(open('data/festivals.json'))
def hr(a,b):
    A=_dt.date.fromisoformat(a); B=_dt.date.fromisoformat(b or a); m=lambda d:d.strftime('%B')+' '+str(d.day)
    if A==B: return f"{m(A)}, {A.year}"
    if A.year!=B.year: return f"{m(A)}, {A.year} - {m(B)}, {B.year}"
    if A.month==B.month: return f"{m(A)} - {B.day}, {A.year}"
    return f"{m(A)} - {m(B)}, {A.year}"
DRMAX=38
def hr2(a,b,n):
    tail=f" · {n} bill"+("" if n==1 else "s"); full=hr(a,b)+tail
    if len(full)<=DRMAX: return full
    A=_dt.date.fromisoformat(a); B=_dt.date.fromisoformat(b or a); f=lambda d:f"{d.month}/{d.year%100:02d}"
    return (f(A) if f(A)==f(B) else f(A)+' - '+f(B))+tail
import re as _re
_MF={k:v for v in "January February March April May June July August September October November December".split() for k in (v[:3],v[:4])}
def fullmo(t): return _re.sub(r'\s*[-–—]\s*',' - ',_fm(t))
def _fm(t): return _re.sub(r'\b(Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)\b\.?(?=\s*\d)',lambda m:_MF.get(m.group(1),m.group(1))+' ',t).replace('  ',' ')
P.append('<h2 style="text-align:center;margin-top:30px">Festival archive</h2><p class="sm" style="text-align:center">From the Stanford Theatre&#39;s past calendars, newest first. Tap a festival for its bills.</p>')
for fe in sorted(FJ['festivals'],key=lambda x:(x['end'] or (str(x['year'])+'-12-31' if x['year'] else '0000')),reverse=True):
    en=fe['end'] or ''
    if en and en>=TODAY: continue
    dr=hr2(fe['start'],fe['end'],len(fe['blocks'])) if fe['start'] else (str(fe['year']) if fe['year'] else 'year not given')
    bl=''.join('<li><b class="bd">'+e(fullmo(b['dates']))+':</b>'+''.join('<span class="bf2">'+e(f['title'])+(' ('+str(f['year'])+')' if f['year'] else '')+(' <span class="tm2">'+e(f['times'])+'</span>' if f['times'] else '')+'</span>' for f in b['films'])+'</li>' for b in fe['blocks'])
    P.append(f'<details class="fest arch" data-end="{en}"><summary><span class="dr dtop">{dr}</span> <span class="an">{e(fe["name"][:110])}</span></summary><ul class="abl">{bl}</ul><p class="sm"><a href="festivals/archive/cal/{urllib.parse.quote(fe["file"])}">Archived calendar page</a> · <a href="https://www.stanfordtheatre.org/calendars/{urllib.parse.quote(fe["file"])}">Original</a></p></details>')
P.append('<p id="nopast" class="sm" style="text-align:center">No finished programs yet.</p></section>')
P.append("""<script>(function(){var t=new Intl.DateTimeFormat('en-CA',{timeZone:'America/Los_Angeles'}).format(new Date());var n=0;
document.querySelectorAll('.pastb').forEach(function(b){var p=b.dataset.end<t;b.classList.toggle('hid',!p);if(p)n++;});document.getElementById('nopast').style.display=n?'none':'';})();</script>""")
open('past.html','w').write(page("Past — Stanford Theatre","".join(P),"","past"))
for s,k in K.items():
    f=F[s];t=T[k]
    fest=[x for x in FEST if s in x[4]][0]
    sched="".join(f'<h3>{d}</h3><ul class="sched">'+"".join(f'<li>{"<b>" if a==s else ""}{ft(a)}: {tt}{"</b>" if a==s else ""}</li>' for a,tt in items)+'</ul>' for d,items in fest[3])
    runs="".join(f'<li><span class="rd">{int(r["start"][5:7])}/{r["start"][:4]}</span> {r["tickets"]:,} tickets'+(f'<br><span class="pair">w/ {e(r["pair"])}</span>' if r["pair"]!="alone" else '')+'</li>' for r in t['runs'])
    li=lambda L:"".join(f'<li>{x}</li>' for x in L)
    b=f'''<article class="film"><div class="top"><img class="poster" src="../posters/{s}.jpg" alt="{e(f['t'])} poster">
<div><h1>{e(f['t'])}</h1><div class="meta">{f['y']} ★ {f['rt']} min</div><p class="cr">{e(f['credit'])}</p><p class="plot">{e(f['plot'])}</p></div></div>
<section><h2>Schedule</h2><div class="dr"><a href="../festivals/{SLUG[fest[2]]}.html">{e(fest[0])}</a> · {fest[1]}</div>{sched}</section>
<section><h2>Trivia</h2><ul>{li(f['rick'])}</ul></section>
<section><h2>Filming Locations</h2><ul>{li(f['loc'])}</ul></section>
<section><h2>Previous Showings</h2><p class="big">{t['tc']} Showings • {t['fc']} Festivals</p><p class="big">{t['tk']} tickets sold</p><h3>Past runs (since '03):</h3><ul class="runs">{runs}</ul></section>
<section><h2>More</h2><ul><li><a href="https://tile.stanfordtheatre.org/tile?q={TQ[k]}">Tile: {e(f['t'])}</a></li><li><a href="https://www.imdb.com/title/{IMDB[k]}/">IMDb: {e(f['t'])}</a></li><li><a href="../infographics/{s}.png" download>Download infographic (PNG)</a></li></ul><a href="../infographics/{s}.png"><img class="ig" src="../infographics/{s}.png" alt="{e(f['t'])} infographic"></a></section></article>'''
    open(f'films/{s}.html','w').write(page(f"{f['t']} — Stanford Theatre",DT(b),"../"))

# ---- festival pages ----
SLUG={EMS:'remembering-eva-marie-saint',PW:'mary-poppins-the-wizard-of-oz'}
ARCH={EMS:'eva-marie-saint.html',PW:'poppins-wizard-2026.html'}
PRES={EMS:dict(title="Remembering Eva Marie Saint",sub="October 2026",days="Friday · Saturday · Sunday",
  blocks=[("October 16-18",[("North by Northwest (1959)","tt0053125","7:30 (plus 3:00 Sat/Sun)"),("On the Waterfront (1954)","tt0047296","5:30, 10:00")]),
          ("October 23-25",[("North by Northwest (1959)","tt0053125","7:30 (plus 3:00 Sat/Sun)"),("On the Waterfront (1954)","tt0047296","5:30, 10:00")])]),
 PW:dict(title=None,sub=None,days="Thursday · Friday · Saturday · Sunday",
  blocks=[("October 29 - November 1",[("Mary Poppins (1964)","tt0058331","7:30 (plus 3:05 Sat/Sun)"),("The Wizard of Oz (1939)","tt0032138","5:35, 10:00")]),
          ("November 5-8",[("Mary Poppins (1964)","tt0058331","7:30 (plus 3:05 Sat/Sun)"),("The Wizard of Oz (1939)","tt0032138","5:35, 10:00")])])}
NOTE='Additional movie information links provided courtesy of the <a href="https://www.imdb.com/">Internet Movie Database</a>. Note: The Internet Movie Database is a commercial enterprise. We link only so you can get additional movie info. We do not endorse any product on other sites.'
def cols(groups,films,root):
    o='<div class="cols">'
    for s in films:
        st="".join(f'<div class="dg">{fullmo(d)}</div><div class="tm">{t}</div>' for d,items in groups for a2,t in items if a2==s)
        o+=f'<div class="col"><a class="card" href="{root}films/{s}.html"><img src="{root}posters/{s}.jpg" alt="{e(F[s]["t"])} poster"><span>{ft(s)}</span><small>{F[s]["rt"]} min</small></a>{st}</div>'
    return o+'</div>'
for name,dr,url,groups,films in FEST:
    p=PRES[url]
    bl="".join(f'<h3>{_sp(d)}</h3><ul class="sched">'+"".join(f'<li>'+(f'<a href="https://www.imdb.com/title/{i}">{e(t)}</a>' if i else e(t))+(f': <b>{tm}</b>' if tm else '')+'</li>' for t,i,tm in it)+'</ul>' for d,it in p['blocks'])
    b=f'''<section class="fest"><div class="dr dtop" style="text-align:center">{dr}</div><h1>{e(name)}</h1>{cols(groups,films,"../")}</section>
<section class="fest pres"><h2>From the Stanford Theatre program page</h2><div class="sm">Preserved copy of the original page (text and images), saved Oct 23, 2026.</div>
<img class="logo" src="img/stanford_theatre.gif" alt="Stanford Theatre logo"><div class="ptitle">Stanford Theatre Movie Guide</div>
{f'<h3 class="pt">{p["title"]}</h3>' if p['title'] else ''}{f'<div class="dr">{p["sub"]}</div>' if p['sub'] else ''}<div class="days">{p['days']}</div>{bl}
<p class="sm">{NOTE}</p></section>
<p class="orig"><a href="{url}">Original Stanford Theatre page</a> · <a href="archive/{ARCH[url]}">archived HTML</a></p>'''
    open(f'festivals/{SLUG[url]}.html','w').write(page(f"{name} — Stanford Theatre",b,"../"))

# ---- search page ----
def tk(txt,c1,c2,gid): return f'<svg class="tk" viewBox="0 0 40 24" width="42" height="25" aria-hidden="true"><defs><linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient></defs><path d="M2 2h36v6a4 4 0 0 0 0 8v6H2v-6a4 4 0 0 0 0-8z" fill="url(#{gid})" stroke="#4a3a0a" stroke-width="1"/><path d="M10 4v16" stroke="#4a3a0a" stroke-width=".8" stroke-dasharray="1.6 1.6"/><text x="24" y="16" font-size="11" font-family="Georgia,serif" font-weight="700" fill="#3a0608" text-anchor="middle">{txt}</text></svg>'
OG=tk("OG","#d3c780","#8a7a2e","gog"); OR=tk("OR","#ffe58a","#d29a1c","gor"); S1=tk("1st","#f4f6f8","#9aa3ab","gs1")
TOG="From the Stanford Theatre&#39;s original billings"; TOR="Original Run — shown during the film&#39;s first release"
TICKET=OR
SJS=open('tools/search.js').read()
sb=f'''<section class="fest"><h1 class="mqh">Search Showings</h1><p class="sm">Billings from the theatre's history pages (1925 - 1961), its archived calendars (1997 - present) and Tile box-office records. </p>
<input id="q" type="search" placeholder="Film title, star, or year…" autofocus>
<div class="legend"><span class="li"><span class="badge og" title="{TOG}">{OG}</span> original billings (history pages)</span><span class="li"><span class="badge or" title="{TOR}">{OR}</span> Original Run (first release)</span><span class="li"><span class="src">Calendar</span> theatre calendars (1997–)</span><span class="li"><span class="badge s1">{S1}</span> first showing on record</span><span class="li"><span class="badge rt">{tk("5","#e8564f","#8e1a16","grt2")}</span> Nth run (history, calendars &amp; Tile combined)</span></div>
<div id="count" class="sm"></div><ul id="res" class="res"></ul></section>
<script src="data/showings.js"></script><script>var OG={json.dumps(OG)},OR={json.dumps(OR)},S1={json.dumps(S1)},RT={json.dumps(tk("@N@","#e8564f","#8e1a16","grt"))},TOG={json.dumps(TOG)},TOR={json.dumps(TOR)};'''+SJS+'''</script>'''
open('search.html','w').write(page("Search — Stanford Theatre",sb,"","search"))
