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
def page(title,body,root=""):
    return f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(title)}</title><link rel="stylesheet" href="{root}style.css"></head><body>
<header class="mq"><a href="{root}index.html"><div class="m1">THE STANFORD THEATRE</div><div class="m2">PALO ALTO · NOW SHOWING</div></a><nav class="nav"><a href="{root}index.html#now">Now Showing</a><a href="{root}index.html#upcoming">Upcoming</a><a href="{root}past.html">Past</a><a href="{root}search.html">Search</a></nav></header><main>{body}</main>
<footer><a href="{MAP}">Stanford Theatre, 221 University Ave, Palo Alto, CA 94301</a><div class="sm">Schedules subject to change — check <a href="https://www.stanfordtheatre.org/calendar.html">stanfordtheatre.org</a>.</div></footer></body></html>'''
def ft(s): f=F[s]; return f"{e(f['t'])} ({f['y']})"

import datetime as _dt, zoneinfo as _zi
TODAY=_dt.datetime.now(_zi.ZoneInfo('America/Los_Angeles')).date().isoformat()
NB=[(EMS,"October 16–18","2026-10-16","2026-10-18",[("north-by-northwest","7:30 (plus 3:00 Sat/Sun)"),("on-the-waterfront","5:30, 10:00")]),
(EMS,"October 23–25","2026-10-23","2026-10-25",[("north-by-northwest","7:30 (plus 3:00 Sat/Sun)"),("on-the-waterfront","5:30, 10:00")]),
(EMS,"October 30-November 1","2026-10-30","2026-11-01",None),
(PW,"October 29–November 1","2026-10-29","2026-11-01",[("mary-poppins","7:30 (plus 3:05 Sat/Sun)"),("the-wizard-of-oz","5:35, 10:00")]),
(PW,"November 5–8","2026-11-05","2026-11-08",[("mary-poppins","7:30 (plus 3:05 Sat/Sun)"),("the-wizard-of-oz","5:35, 10:00")])]
FN={x[2]:(x[0],x[1]) for x in FEST}
NB=[b for b in NB if b[4] or not any(o[0]!=b[0] and o[4] and o[2]<=b[3] and b[2]<=o[3] for o in NB)]
def blk(b):
    url,lab,st,en,items=b; nm,dr=FN[url]; sl=SLUG[url]
    head=f'<div class="bf"><h2><a href="festivals/{sl}.html">{e(nm)} →</a></h2><div class="dr">{dr}</div></div>'
    if items:
        body='<div class="cols">'+"".join(f'<div class="col"><a class="card" href="films/{s}.html"><img src="posters/{s}.jpg" alt="{e(F[s]["t"])} poster"><span>{ft(s)}</span><small>{F[s]["rt"]} min</small></a><div class="tm">{t}</div></div>' for s,t in items)+'</div>'
    else: body='<p class="tba">To Be Announced</p>'
    return f'<section class="fest blk" data-start="{st}" data-end="{en}" data-fest="{sl}">{head}<h3 class="bl">{lab}</h3>{body}<a class="btn" href="festivals/{sl}.html">Festival page →</a></section>'
live=sorted([b for b in NB if b[3]>=TODAY],key=lambda b:b[2])
h=['<section id="now"><h1>Now Showing</h1>']
if live: h.append(blk(live[0]))
h.append('</section><section id="upcoming"><h1>Upcoming</h1>')
for name,dr,url,groups,films in FEST:
    bs=[b for b in live[1:] if b[0]==url]
    if bs: h.append(f'<div class="fgrp" data-fest="{SLUG[url]}"><h2 class="gh"><a href="festivals/{SLUG[url]}.html">{e(name)} →</a></h2><div class="dr">{dr}</div>'+"".join(blk(b) for b in bs)+'</div>')
h.append('</section>')
h.append("""<script>(function(){var t=new Intl.DateTimeFormat('en-CA',{timeZone:'America/Los_Angeles'}).format(new Date());
var all=[].slice.call(document.querySelectorAll('.blk'));all.forEach(function(b){if(b.dataset.end<t)b.remove();});
var now=document.getElementById('now');if(!now.querySelector('.blk')){var r=[].slice.call(document.querySelectorAll('#upcoming .blk')).sort(function(a,b){return a.dataset.start<b.dataset.start?-1:1;});if(r[0])now.appendChild(r[0]);}
document.querySelectorAll('.fgrp').forEach(function(g){if(!g.querySelector('.blk'))g.remove();});
if(!document.querySelector('#upcoming .blk'))document.getElementById('upcoming').style.display='none';})();</script>""")
open('index.html','w').write(page("Stanford Theatre — Now Showing","".join(h)))
P=['<section id="past"><h1>Past</h1><p class="sm" style="text-align:center">Finished programs, newest first.</p>']
for b in sorted(NB,key=lambda b:b[3],reverse=True):
    x=blk(b).replace('<section class="fest blk"','<section class="fest blk pastb'+('' if b[3]<TODAY else ' hid')+'"',1)
    P.append(x)
FJ=json.load(open('data/festivals.json'))
P.append('<h2 style="text-align:center;margin-top:30px">Festival archive</h2><p class="sm" style="text-align:center">From the Stanford Theatre&#39;s past calendars, newest first. Tap a festival for its bills.</p>')
for fe in sorted(FJ['festivals'],key=lambda x:(x['end'] or (str(x['year'])+'-12-31' if x['year'] else '0000')),reverse=True):
    en=fe['end'] or ''
    if en and en>=TODAY: continue
    dr=(fe['start']+' – '+fe['end']) if fe['start'] else (str(fe['year']) if fe['year'] else 'year not given')
    bl=''.join('<li><b>'+e(b['dates'])+'</b>: '+' / '.join(e(f['title'])+(' ('+str(f['year'])+')' if f['year'] else '')+(' '+e(f['times']) if f['times'] else '') for f in b['films'])+'</li>' for b in fe['blocks'])
    P.append(f'<details class="fest arch" data-end="{en}"><summary><span class="an">{e(fe["name"][:110])}</span> <span class="dr">{dr} · {len(fe["blocks"])} bills</span></summary><ul class="abl">{bl}</ul><p class="sm"><a href="festivals/archive/cal/{urllib.parse.quote(fe["file"])}">Archived calendar page</a> · <a href="https://www.stanfordtheatre.org/calendars/{urllib.parse.quote(fe["file"])}">Original</a></p></details>')
P.append('<p id="nopast" class="sm" style="text-align:center">No finished programs yet.</p></section>')
P.append("""<script>(function(){var t=new Intl.DateTimeFormat('en-CA',{timeZone:'America/Los_Angeles'}).format(new Date());var n=0;
document.querySelectorAll('.pastb').forEach(function(b){var p=b.dataset.end<t;b.classList.toggle('hid',!p);if(p)n++;});document.getElementById('nopast').style.display=n?'none':'';})();</script>""")
open('past.html','w').write(page("Past — Stanford Theatre","".join(P)))
for s,k in K.items():
    f=F[s];t=T[k]
    fest=[x for x in FEST if s in x[4]][0]
    sched="".join(f'<h3>{d}</h3><ul class="sched">'+"".join(f'<li>{"<b>" if a==s else ""}{ft(a)}: {tt}{"</b>" if a==s else ""}</li>' for a,tt in items)+'</ul>' for d,items in fest[3])
    runs="".join(f'<li><span class="rd">{int(r["start"][5:7])}/{r["start"][:4]}</span> {r["tickets"]:,} tickets'+(f'<br><span class="pair">w/ {e(r["pair"])}</span>' if r["pair"]!="alone" else '')+'</li>' for r in t['runs'])
    li=lambda L:"".join(f'<li>{x}</li>' for x in L)
    b=f'''<article class="film"><div class="top"><img class="poster" src="../posters/{s}.jpg" alt="{e(f['t'])} poster">
<div><h1>{e(f['t'])}</h1><div class="meta">{f['y']} ★ {f['rt']} min</div><p class="cr">{e(f['credit'])}</p><p class="plot">{e(f['plot'])}</p></div></div>
<section><h2>Schedule</h2><div class="dr"><a href="../festivals/{SLUG[fest[2]]}.html">{e(fest[0])} →</a> · {fest[1]}</div>{sched}<a class="btn" href="../festivals/{SLUG[fest[2]]}.html">Festival page →</a></section>
<section><h2>Trivia</h2><ul>{li(f['rick'])}</ul></section>
<section><h2>Filming Locations</h2><ul>{li(f['loc'])}</ul></section>
<section><h2>Previous Showings</h2><p class="big">{t['tc']} Showings • {t['fc']} Festivals</p><p class="big">{t['tk']} tickets sold</p><h3>Past runs (since '03):</h3><ul class="runs">{runs}</ul></section>
<section><h2>More</h2><ul><li><a href="https://tile.stanfordtheatre.org/tile?q={TQ[k]}">Tile: {e(f['t'])}</a></li><li><a href="https://www.imdb.com/title/{IMDB[k]}/">IMDb: {e(f['t'])}</a></li><li><a href="../infographics/{s}.png" download>Download infographic (PNG)</a></li></ul><a href="../infographics/{s}.png"><img class="ig" src="../infographics/{s}.png" alt="{e(f['t'])} infographic"></a></section></article>'''
    open(f'films/{s}.html','w').write(page(f"{f['t']} — Stanford Theatre",b,"../"))

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
        st="".join(f'<div class="dg">{d}</div><div class="tm">{t}</div>' for d,items in groups for a2,t in items if a2==s)
        o+=f'<div class="col"><a class="card" href="{root}films/{s}.html"><img src="{root}posters/{s}.jpg" alt="{e(F[s]["t"])} poster"><span>{ft(s)}</span><small>{F[s]["rt"]} min</small></a>{st}</div>'
    return o+'</div>'
for name,dr,url,groups,films in FEST:
    p=PRES[url]
    bl="".join(f'<h3>{d}</h3><ul class="sched">'+"".join(f'<li>'+(f'<a href="https://www.imdb.com/title/{i}">{e(t)}</a>' if i else e(t))+(f': <b>{tm}</b>' if tm else '')+'</li>' for t,i,tm in it)+'</ul>' for d,it in p['blocks'])
    b=f'''<section class="fest"><h1>{e(name)}</h1><div class="dr" style="text-align:center">{dr}</div>{cols(groups,films,"../")}</section>
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
sb=f'''<section class="fest"><h1>Search Showings</h1><p class="sm">Billings from the theatre's history pages (1925–1961), its archived calendars (1997–present) and Tile box-office records. </p>
<input id="q" type="search" placeholder="Film title, star, or year…" autofocus>
<div class="legend"><span class="badge og" title="{TOG}">{OG}OG</span> = from the Stanford Theatre&#39;s original billings (history pages) &nbsp; <span class="badge or" title="{TOR}">{OR}OR</span> = Original Run, shown during the film&#39;s first release &nbsp; <span class="src">Calendar</span> = stanfordtheatre.org past calendars (1997–) &nbsp; <span class="badge s1">{S1}1st</span> = first showing in Tile records &nbsp; <span class="badge rt">{tk("5","#e8564f","#8e1a16","grt2")}#5</span> = Nth time shown (Tile records)</div>
<div id="count" class="sm"></div><ul id="res" class="res"></ul></section>
<script src="data/showings.js"></script><script>
var OG={json.dumps(OG)},OR={json.dumps(OR)},S1={json.dumps(S1)},RT={json.dumps(tk("@N@","#e8564f","#8e1a16","grt"))},TOG={json.dumps(TOG)},TOR={json.dumps(TOR)};var D=window.SHOWINGS,q=document.getElementById('q'),R=document.getElementById('res'),C=document.getElementById('count');
function esc(s){{return String(s).replace(/[&<>"]/g,function(c){{return{{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}}[c]}})}}
function go(){{var v=q.value.trim().toLowerCase();if(v.length<2){{R.innerHTML='';C.textContent=D.length.toLocaleString()+' showings indexed. Type at least 2 characters.';return}}
var m=D.filter(function(o){{return (o.title+' '+o.note+' '+o.start).toLowerCase().indexOf(v)>=0}});C.textContent=m.length.toLocaleString()+' matches'+(m.length>300?' (showing first 300)':'');
R.innerHTML=m.slice(0,300).map(function(o){{var d=o.source=='Tile'?(o.start+(o.end!=o.start?' – '+o.end:'')):o.date_text;
function ord(n){{var s=['th','st','nd','rd'],v=n%100;return n+(s[(v-20)%10]||s[v]||s[0])}}
var b=o.source=='Stanford Theatre calendars'?'<span class="src">Calendar</span>'+(o.badge?' <span class="badge or" title="'+TOR+'">'+OR+'OR</span>':''):(o.source=='Tile'?(o.n==1?'<span class="badge s1" title="First showing in Tile records">'+S1+'1st</span>':'<span class="badge rt" title="'+ord(o.n)+' time shown (Tile records)">'+RT.replace('@N@',o.n)+'#'+o.n+'</span>'):'<span class="badge og" title="'+TOG+'">'+OG+'OG</span>')+(o.badge?' <span class="badge or" title="'+TOR+'">'+OR+'OR</span>':'');
return '<li><div class="rt"><a href="'+esc(o.url)+'">'+esc(o.title)+'</a> '+b+'</div><div class="rd2">'+esc(d)+(o.tickets!=null?' · '+o.tickets.toLocaleString()+' tickets':'')+'</div>'+(o.note?'<div class="rn">'+esc(o.note)+'</div>':'')+'</li>'}}).join('')}}
q.addEventListener('input',go);var u=new URLSearchParams(location.search).get('q');if(u)q.value=u;go();</script>'''
open('search.html','w').write(page("Search — Stanford Theatre",sb))
