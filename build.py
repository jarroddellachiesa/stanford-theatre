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
ALI0=lambda t:_TA0.get(t,t)
_TA0=json.load(open('data/title_aliases.json'))['aliases']
SLUG={EMS:'remembering-eva-marie-saint',PW:'mary-poppins-the-wizard-of-oz'}
def page(title,body,root="",act=""):
    A=lambda k:' class="on" aria-current="page"' if k==act else ""
    return f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(title)}</title><link rel="stylesheet" href="{root}style.css"><link rel="icon" href="{root}favicon.ico" sizes="any"><link rel="icon" type="image/png" sizes="32x32" href="{root}icons/favicon-32.png"><link rel="apple-touch-icon" href="{root}icons/apple-touch-icon.png?v=4"><link rel="manifest" href="{root}manifest.webmanifest"><meta name="theme-color" content="#5a0e18"><meta name="apple-mobile-web-app-capable" content="yes"><meta name="mobile-web-app-capable" content="yes"><meta name="apple-mobile-web-app-title" content="Stanford"><meta name="apple-mobile-web-app-status-bar-style" content="black-translucent"><script>if("serviceWorker" in navigator)addEventListener("load",function(){{navigator.serviceWorker.register("{root}sw.js")}})</script></head><body>
<header class="mq"><a href="{root}index.html"><div class="m1">THE STANFORD THEATRE</div></a><nav class="nav"><a href="{root}index.html"{A("now")}>Now Showing</a><span class="sep" aria-hidden="true">·</span><a href="{root}upcoming.html"{A("up")}>Upcoming</a><span class="sep" aria-hidden="true">·</span><a href="{root}past.html"{A("past")}>Past</a><span class="sep" aria-hidden="true">·</span><a href="{root}search.html"{A("search")}>Search</a></nav></header><main>{body}</main><script>(function(){{var t=new Intl.DateTimeFormat('en-CA',{{timeZone:'America/Los_Angeles'}}).format(new Date());document.querySelectorAll('[data-day]').forEach(function(d){{if(d.dataset.day<t)d.remove()}});document.querySelectorAll('.bill').forEach(function(b){{if(!b.querySelector('[data-day]'))b.remove()}});document.querySelectorAll('.ups').forEach(function(u){{if(!u.querySelector('[data-day]'))u.remove()}});}})();</script>
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

SITE="https://stanfordtheatre.dellachiesa.us/"
def _times(t,wd):
    base=_re0.sub(r'\(.*?\)','',t); out=[x for x in _re0.findall(r'\d{1,2}:\d\d',base)]
    for m in _re0.finditer(r'\(plus ([^)]*?)\s*Sat/Sun\)',t):
        if wd>=5: out+=_re0.findall(r'\d{1,2}:\d\d',m.group(1))
    def k(x): h,mm=map(int,x.split(':')); return (h%12+12 if h<12 else h)*60+mm
    return sorted(set(out),key=k)
def _dt24(d,x):
    h,mm=map(int,x.split(':')); h=h%12+12 if h<12 else h
    return _dt.datetime(d.year,d.month,d.day,h,mm)
def GCAL(slug,d,x,partner,sl):
    f=F[slug]; a=_dt24(d,x); b=a+_dt.timedelta(minutes=int(f.get('rt') or 120))
    pl=(f.get('plot') or '').strip()
    if len(pl)>500:
        cut=pl[:500]; k=max(cut.rfind('. '),cut.rfind('! '),cut.rfind('? '))
        pl=cut[:k+1] if k>200 else cut.rsplit(' ',1)[0]+'…'
    det=(pl+'\n\n' if pl else '')+f"{f['t']} ({f['y']})"+(f" on a double bill with {partner}" if partner else '')+"."+"\n\n"+f'<a href="{SITE}festivals/{sl}.html">{html.escape({SLUG[u_]:n_ for n_,_,u_,_,_ in FEST}.get(sl,"Festival page"))}</a>'+"\n"+f'<a href="{SITE}films/{slug}.html">{html.escape(f["t"])} on our site</a>'
    q=urllib.parse.urlencode(dict(action='TEMPLATE',text=f['t'],dates=a.strftime('%Y%m%dT%H%M00')+'/'+b.strftime('%Y%m%dT%H%M00'),ctz='America/Los_Angeles',location='Stanford Theatre, 221 University Avenue, Palo Alto, CA 94301',details=det))
    return 'https://calendar.google.com/calendar/render?'+q
def DAYS(st,en,items,sl,only=None,compact=False):
    A=_dt.date.fromisoformat(st);B=_dt.date.fromisoformat(en);o=''
    while A<=B:
        wd=A.weekday(); lab=A.strftime('%A, %B ')+str(A.day)+(' <span class="an100" title="The Stanford Theatre opened June 9, 1925">100th Anniversary</span>' if A.isoformat()=='2025-06-09' else ''); rows=''
        for s_,t_ in items:
            if only and s_!=only: continue
            ts=_times(t_,wd); partner=", ".join(F[x]['t'] for x,_ in items if x!=s_)
            if not ts: continue
            rows+=f'<li>'+('' if only else f'<span class="df">{ft(s_)}</span> ')+' '.join(f'<a class="st gct" href="{e(GCAL(s_,A,x,partner,sl))}" target="_blank" rel="noopener" title="Add {x} {e(F[s_]["t"])} to Google Calendar" aria-label="Add {x} {e(F[s_]["t"])} to Google Calendar">{x}</a>' for x in ts)+'</li>'
        if rows:
            o+=(f'<details class="day" data-day="{A.isoformat()}"><summary>{lab}</summary><ul class="dsch">{rows}</ul></details>' if compact else f'<div class="day" data-day="{A.isoformat()}"><h4>{lab}</h4><ul class="dsch">{rows}</ul></div>')
        A+=_dt.timedelta(days=1)
    return o
def blk(b):
    url,lab,st,en,items=b; nm,dr=FN[url]; sl=SLUG[url]
    head=f'<div class="bf"><div class="dr dtop">{dr}</div><h2><a href="festivals/{sl}.html">{e(nm)}</a></h2></div>'
    if items:
        body='<div class="cols">'+"".join(f'<div class="col"><a class="card" href="films/{s}.html"><img src="posters/{s}.jpg" alt="{e(F[s]["t"])} poster"><span>{ft(s)}</span><small>{F[s]["rt"]} min</small></a></div>' for s,t in items)+'</div>'
        body+='<div class="days">'+DAYS(st,en,items,sl,compact=True)+'</div>'
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
h=['<section id="now"><h1 class="vh">Now Showing</h1>']+[blk(b) for b in live]+['<p id="empty" class="sm" style="display:none;text-align:center">Nothing scheduled right now — see <a href="past.html">Past</a>.</p></section>',JSF]
open('index.html','w').write(page("Stanford Theatre — Now Showing","".join(h),"","now").replace('<body>','<body data-mode="now">',1))
u=['<section id="upcoming"><h1 class="vh">Upcoming</h1>']
for name,dr,url,groups,films in FEST:
    bs=[b for b in live if b[0]==url]
    if bs: u.append(f'<div class="fgrp" data-fest="{SLUG[url]}"><div class="dr dtop">{dr}</div><h2 class="gh"><a href="festivals/{SLUG[url]}.html">{e(name)}</a></h2>'+"".join(blk(b) for b in bs)+'</div>')
u+=['<p id="empty" class="sm" style="display:none;text-align:center">No further programs announced yet.</p></section>',JSF]
open('upcoming.html','w').write(page("Stanford Theatre — Upcoming","".join(u),"","up").replace('<body>','<body data-mode="up">',1))
P=['<section id="past"><h1 class="vh">Past</h1><p class="sm" style="text-align:center">Finished programs, newest first.</p>']
for b in sorted(NB,key=lambda b:b[3],reverse=True):
    x=blk(b).replace('<section class="fest blk"','<section class="fest blk pastb'+('' if b[3]<TODAY else ' hid')+'"',1)
    P.append(x)
FJ=json.load(open('data/festivals.json'))
_FIXN={'kurasawa':'Kurosawa','ray':'Satyajit Ray','fox':'20th Century-Fox','april':'April','horror':'Horror','holiday':'Holiday','summer':'Summer','winter':'Winter','cukor':'George Cukor','hitchcock':'Hitchcock'}
def FN(n):
    m=_re0.fullmatch(r'([a-z]+)(\d{4})',n or '')
    return (_FIXN.get(m.group(1),m.group(1).title())+' '+m.group(2)) if m else n
for _fe in FJ['festivals']: _fe['name']=FN(_fe['name'])
AN100='<span class="an100" title="The Stanford Theatre opened June 9, 1925">100th Anniversary</span>'
def ANB(b): return (' '+AN100) if b.get('start')=='2025-06-09' else ''
def PSLUG(fe): return _re0.sub(r'[^a-z0-9]+','-',urllib.parse.unquote(fe['file']).rsplit('.',1)[0].lower()).strip('-')
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
    bl=''.join('<li><b class="bd">'+e(fullmo(b['dates']))+':</b>'+ANB(b)+''.join('<span class="bf2">'+e(_TA0.get(f['title'],f['title']))+(' ('+str(f['year'])+')' if f['year'] else '')+(' <span class="tm2">'+e(f['times'])+'</span>' if f['times'] else '')+'</span>' for f in b['films'])+'</li>' for b in fe['blocks'])
    P.append(f'<details class="fest arch" data-end="{en}"><summary><span class="dr dtop">{dr}</span> <span class="an"><a class="pfl" href="festivals/past/{PSLUG(fe)}.html">{e(fe["name"][:110])}</a></span></summary><ul class="abl">{bl}</ul><p class="sm"><a href="festivals/archive/cal/{urllib.parse.quote(fe["file"])}">Archived calendar page</a> · <a href="https://www.stanfordtheatre.org/calendars/{urllib.parse.quote(fe["file"])}">Original</a></p></details>')
P.append('<p id="nopast" class="sm" style="text-align:center">No finished programs yet.</p></section>')
P.append("""<script>(function(){var t=new Intl.DateTimeFormat('en-CA',{timeZone:'America/Los_Angeles'}).format(new Date());var n=0;
document.querySelectorAll('.pastb').forEach(function(b){var p=b.dataset.end<t;b.classList.toggle('hid',!p);if(p)n++;});document.getElementById('nopast').style.display=n?'none':'';})();</script>""")
open('past.html','w').write(page("Past — Stanford Theatre","".join(P),"","past"))
def tk(txt,c1,c2,gid): return f'<svg class="tk" viewBox="0 0 40 24" width="42" height="25" aria-hidden="true"><defs><linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient></defs><path d="M2 2h36v6a4 4 0 0 0 0 8v6H2v-6a4 4 0 0 0 0-8z" fill="url(#{gid})" stroke="#4a3a0a" stroke-width="1"/><path d="M10 4v16" stroke="#4a3a0a" stroke-width=".8" stroke-dasharray="1.6 1.6"/><text x="24" y="16" font-size="11" font-family="Georgia,serif" font-weight="700" fill="#3a0608" text-anchor="middle">{txt}</text></svg>'
OG=tk("OG","#d3c780","#8a7a2e","gog"); OR=tk("OR","#ffe58a","#d29a1c","gor"); S1=tk("1st","#f4f6f8","#9aa3ab","gs1")
TOG="From the Stanford Theatre&#39;s original billings"; TOR="Original Run — shown during the film&#39;s first release"
TICKET=OR

import unicodedata as _ud
RT=tk("@N@","#e8564f","#8e1a16","grt")
SH=json.load(open('data/showings.json'))
ETY=json.load(open('data/entry_types.json')) if __import__('os').path.exists('data/entry_types.json') else {}
for o in SH:
    if o.get('badge')=='Original Run': o['type']=ETY.get(o['title']+'|'+o['start'],'unknown')
TYL={'short':'Short','newsreel':'Newsreel','vaudeville/stage act':'Stage act','special event':'Special event','unknown':'Unverified'}
def TYB(o):
    t=o.get('type'); return f'<span class="ety ety-{t.split("/")[0].replace(" ","-")}" title="Entry type: {t}">{TYL[t]}</span> ' if t in TYL else ''
_PFM={'festivals/archive/cal/'+_fe['file']:_fe for _fe in FJ['festivals']}
_PFM.update({'festivals/archive/cal/'+urllib.parse.quote(_fe['file']):_fe for _fe in FJ['festivals']})
NMATCH=[0,0]
for o in SH:
    if o['source']!='Stanford Theatre calendars': continue
    fe=_PFM.get(o['url'])
    if not fe or not fe['blocks']: NMATCH[1]+=1; continue
    NMATCH[0]+=1
    o['url']='festivals/past/'+PSLUG(fe)+'.html'
    pw=[]
    for b in fe['blocks']:
        if b.get('start')==o['start'] or (b['start'] and b['start']<=o['start']<=(b.get('end') or b['start'])):
            ts=[ALI0(f['title']) for f in b['films']]
            if ALI0(o['title']) in ts: pw=[t for t in ts if t!=ALI0(o['title'])]; break
    o['note']=fe['name'][:80]+(' · w/ '+', '.join(pw) if pw else '')
print('RUNLINKS ours',NMATCH[0],'fallback',NMATCH[1])
open('data/showings.js','w').write('window.SHOWINGS='+json.dumps(SH,ensure_ascii=False)+';')
def NJ(t):
    t=_ud.normalize('NFD',str(t)); t=''.join(c for c in t if not _ud.combining(c)).lower().replace('&',' and ')
    t=_re0.sub(r"['’`]",'',t); w=[x for x in _re0.sub(r'[^a-z0-9]+',' ',t).split() if x and x not in('the','a','an')]
    return ' '.join(x[:-1] if len(x)>4 and x.endswith('ing') else x for x in w)
_MNL="January February March April May June July August September October November December".split()
def FRp(a,b):
    A=[int(x) for x in a.split('-')]; B=[int(x) for x in (b or a).split('-')] if (b or a).count('-')==2 else A
    if not A[1] or not A[2]: return None
    m=lambda x:f"{_MNL[x[1]-1]} {x[2]}"
    if not B[1] or not B[2] or a==b or not b: f=f"{m(A)}, {A[0]}"
    elif A[0]!=B[0]: f=f"{m(A)}, {A[0]} - {m(B)}, {B[0]}"
    elif A[1]==B[1]: f=f"{m(A)} - {B[2]}, {A[0]}"
    else: f=f"{m(A)} - {m(B)}, {A[0]}"
    if len(f)>38:
        g=lambda x:f"{x[1]}/{x[0]%100:02d}"; f=g(A) if g(A)==g(B) else g(A)+' - '+g(B)
    return f
def ORD(n): return str(n)+({1:'st',2:'nd',3:'rd'}.get(n%10 if n%100 not in(11,12,13) else 0,'th'))
def BADGE(o):
    h=TYB(o)
    if o['source'] not in ('Tile','Stanford Theatre calendars'): h+=f'<span class="badge og" title="{TOG}">{OG}</span> '
    if o.get('badge'): h+=f'<span class="badge or" title="{TOR}">{OR}</span> '
    n=o.get('n')
    if n==1 and not o.get('badge'): h+=f'<span class="badge s1" title="First showing at the Stanford Theatre on record">{S1}</span>'
    elif n and n>1: h+=f'<span class="badge rt" title="{ORD(n)} run at the Stanford Theatre on record">'+RT.replace('@N@',str(n))+'</span>'
    return h
def FILMRUNS(title,key=None):
    k=NJ(title); its=sorted([o for o in SH if (o.get('run','').rsplit('|',1)[0]==key if key else NJ(o['title'])==k)],key=lambda o:o['start']); R=[];M={}
    for o in its:
        if not o.get('run'): R.append(dict(o,srcs={o['source']:1})); continue
        m=M.get(o['run'])
        if not m:
            m=M[o['run']]=dict(title=o['title'],source=o['source'],start=o['start'],end=o.get('end'),date_text=o.get('date_text'),url=o['url'],note=o.get('note') or '',n=o['n'],badge=o.get('badge') or '',tickets=None,srcs={},nn=0); R.append(m)
        m['srcs'][o['source']]=1
        if o.get('badge'): m['badge']=o['badge']
        if o.get('type') and m.get('type')!='feature': m['type']=o['type']
        if o['start']<m['start']: m['start']=o['start']
        if (o.get('end') or o['start'])>(m['end'] or m['start']): m['end']=o.get('end')
        if o['source']!='Tile' and m['source']=='Tile': m['source']=o['source']; m['url']=o['url']; m['date_text']=o.get('date_text')
        if o['source']!='Tile' and o.get('note') and not m['nn']: m['note']=o['note']; m['nn']=1
        elif not m['note'] and o.get('note'): m['note']=o['note']
        if o.get('tickets') is not None: m['tickets']=(m['tickets'] or 0)+o['tickets']
    for m in R:
        if 'Tile' in m['srcs'] and m['source']!='Tile': m['date_text']=None
    return R
def DD(o):
    if o['source']=='Tile' or not o.get('date_text'): return FRp(o['start'],o.get('end')) or o['start']
    x=_re0.search(r'\(([^)]*day[^)]*)\)',o['date_text']); r=FRp(o['start'],o.get('end'))
    return (r+(' ('+DT(x.group(1)).replace('–',' - ')+')' if x else '')) if r else DT(o['date_text'])
def FESTLINK(o):
    for n_,d_,u_,g_,fl_ in FEST:
        a_,b_=_rng[u_]
        if o['start']<=b_ and (o.get('end') or o['start'])>=a_: return '../festivals/'+SLUG[u_]+'.html'
    u=o['url']; return u if u.startswith('http') else '../'+u
for s,k in K.items():
    f=F[s];t=T[k]
    fest=[x for x in FEST if s in x[4]][0]
    sl_=SLUG[fest[2]]; sched="".join(f'<div class="bill" data-end="{en}">'+DAYS(st,en,items,sl_,only=s)+'</div>' for u,lab,st,en,items in NB if items and any(a==s for a,_ in items))
    FR_=FILMRUNS(f['t'])
    runs="".join(f'<li>{BADGE(o)} <a class="sd" href="{e(FESTLINK(o))}">{e(DD(o))}</a>'+(f' · {o["tickets"]:,} tickets' if o.get('tickets') is not None else '')+(f' <span class="rn">· {e(o["note"])}</span>' if o.get('note') else '')+'</li>' for o in FR_)
    OGR=[o for o in FR_ if 'Stanford Theatre history page' in o.get('srcs',{})]
    ORR=[o for o in FR_ if o.get('badge')]
    OGS=''
    if OGR:
        rng=FRp(OGR[0]['start'],max((o.get('end') or o['start']) for o in OGR)) if len(OGR)>1 else FRp(OGR[0]['start'],OGR[0].get('end'))
        OGS+=f'<p class="big ogsum"><span class="badge og" title="{TOG}">{OG}</span> Original Billings: {len(OGR)} run{"s" if len(OGR)!=1 else ""} ({rng})</p>'
        if ORR: OGS+=f'<p class="big ogsum"><span class="badge or" title="{TOR}">{OR}</span> Original Run: {e(DD(ORR[0]))}</p>'
    print('FILMRUNS',f['t'],len(FR_),'old',len(t['runs']))
    li=lambda L:"".join(f'<li>{x}</li>' for x in L)
    b=f'''<article class="film"><div class="top"><img class="poster" src="../posters/{s}.jpg" alt="{e(f['t'])} poster">
<div><h1>{e(f['t'])}</h1><div class="meta">{f['y']} ★ {f['rt']} min</div><p class="cr">{e(f['credit'])}</p><p class="plot">{e(f['plot'])}</p></div></div>
<section class="ups"><h2>Upcoming Showings</h2>{sched}</section>
<section><h2>Trivia</h2><ul>{li(f['rick'])}</ul></section>
<section><h2>Filming Locations</h2><ul>{li(f['loc'])}</ul></section>
<section><h2>Previous Showings</h2><p class="big">{t['tc']} Showings • {t['fc']} Festivals</p><p class="big">{t['tk']} tickets sold</p>{OGS}<h3>All runs on record ({len(FR_)}):</h3><ul class="runs fl">{runs}</ul></section>
<section><h2>More</h2><ul><li><a href="https://tile.stanfordtheatre.org/tile?q={TQ[k]}">Tile: {e(f['t'])}</a></li><li><a href="https://www.imdb.com/title/{IMDB[k]}/">IMDb: {e(f['t'])}</a></li></ul></section></article>'''
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

# ---- covered films (last 5 years + top 200) ----
import unicodedata as _ud2
def NKT(t):
    t=_ud2.normalize('NFD',t); t=''.join(c for c in t if not _ud2.combining(c)).lower()
    t=_re0.sub(r'\s*\((?:19|20)\d\d\)\s*$','',t).replace('&',' and ')
    t=_re0.sub(r"['’`]",'',t); return ' '.join(x for x in _re0.sub(r'[^a-z0-9]+',' ',t).split() if x not in('the','a','an'))
TA=json.load(open('data/title_aliases.json')); ALI=lambda t:TA['aliases'].get(t,t); RMK={k:v for k,v in TA['remakes'].items() if len(v)>1}
def FKEY(t,y=None):
    k=NKT(ALI(t))
    if k in RMK and y in RMK[k]: k+='#'+str(y)
    return k
import os as _o0
CV=json.load(open('data/cover.json')); CM=json.load(open('data/cover_meta.json'))
FEATK={'north by northwest':'north-by-northwest','on waterfront':'on-the-waterfront','mary poppins':'mary-poppins','wizard of oz':'the-wizard-of-oz'}
COV={}  # key -> dict(slug,title,year,rt,poster)
def _syn(x):
    x=_re0.sub(r'\s+',' ',x or '').strip(); ss=_re0.split(r'(?<=[.!?])\s+',x); o=''
    for t_ in ss:
        if len(o)+len(t_)>420 and o: break
        o+=(' ' if o else '')+t_
    return o
_used=set(FEATK.values())
for c in CV:
    k=c['key']; m=CM.get(k)
    if k in FEATK or not m: continue
    if _o0.environ.get('PHASE')=='1' and not c['recent']: continue
    tt=ALI(c['title']); tt=_re0.sub(r'\s*\((?:19|20)\d\d\)$','',tt)
    yr=int(k.split('#')[1]) if '#' in k else (c['year'] or (int(m['pd']) if m.get('pd') else m.get('wy')))
    sl=_re0.sub(r'[^a-z0-9]+','-',tt.lower()).strip('-')
    if sl in _used or '#' in k: sl+=f'-{yr}'
    _used.add(sl)
    COV[k]=dict(slug=sl,title=tt,year=yr,rt=m.get('rt'),poster=(lambda f_:f_ if _o0.path.exists(f_) else None)('posters/c/'+_re0.sub(r'[^a-z0-9]+','-',k.replace('#','-')).strip('-')+'.jpg'),syn=_syn(m.get('ext')),desc=m.get('desc') or '',imdb=m.get('imdb'),wt=m['wt'])
NFP=0
CFX=json.load(open('data/cover_facts.json')) if _o0.path.exists('data/cover_facts.json') else {}
import os as _o2
if _o2.environ.get('NOCOVER'): COV={}
for k,v in COV.items():
    FR_=FILMRUNS(v['title'],key=k)
    if not FR_: continue
    if all(o.get('type') not in (None,'feature') for o in FR_) and not _o2.path.exists(f'films/{v["slug"]}.html'): continue  # non-feature entries never get new film pages
    runs="".join(f'<li>{BADGE(o)} <a class="sd" href="{e(FESTLINK(o))}">{e(DD(o))}</a>'+(f' · {o["tickets"]:,} tickets' if o.get('tickets') is not None else '')+(f' <span class="rn">· {e(o["note"])}</span>' if o.get('note') else '')+'</li>' for o in FR_)
    OGR=[o for o in FR_ if 'Stanford Theatre history page' in o.get('srcs',{})]; ORR=[o for o in FR_ if o.get('badge')]; OGS=''
    if OGR:
        rng=FRp(OGR[0]['start'],max((o.get('end') or o['start']) for o in OGR)) if len(OGR)>1 else FRp(OGR[0]['start'],OGR[0].get('end'))
        OGS+=f'<p class="big ogsum"><span class="badge og" title="{TOG}">{OG}</span> Original Billings: {len(OGR)} run{"s" if len(OGR)!=1 else ""} ({rng})</p>'
        if ORR: OGS+=f'<p class="big ogsum"><span class="badge or" title="{TOR}">{OR}</span> Original Run: {e(DD(ORR[0]))}</p>'
    tks=sum(o['tickets'] for o in FR_ if o.get('tickets')); fcs=len({o['url'] for o in SH if o.get('run','').rsplit('|',1)[0]==k and o['source']=='Stanford Theatre calendars'})
    meta=' ★ '.join(x for x in [str(v['year']) if v['year'] else '',f"{v['rt']} min" if v['rt'] else ''] if x)
    img=f'<img class="poster" src="../{v["poster"]}" alt="{e(v["title"])} poster">' if v['poster'] else ''
    more=f'<li><a href="https://tile.stanfordtheatre.org/tile?q={urllib.parse.quote_plus(v["title"])}">Tile: {e(v["title"])}</a></li>'+(f'<li><a href="https://www.imdb.com/title/{v["imdb"]}/">IMDb: {e(v["title"])}</a></li>' if v['imdb'] else '')+f'<li><a href="https://en.wikipedia.org/wiki/{urllib.parse.quote(v["wt"].replace(" ","_"))}">Wikipedia: {e(v["wt"])}</a></li>'
    b=f'''<article class="film"><div class="top">{img}
<div><h1>{e(v['title'])}</h1><div class="meta">{meta}</div>{f'<p class="cr">{e(v["desc"][:1].upper()+v["desc"][1:])}</p>' if v['desc'] else ''}<p class="plot">{e(v['syn'])}</p></div></div>
{(lambda fx:(f'<section><h2>Trivia</h2><ul>'+''.join(f'<li>{e(x)}</li>' for x in fx['trivia'])+'</ul></section>' if fx.get('trivia') else '')+(f'<section><h2>Filming Locations</h2><ul>'+''.join(f'<li>{e(x)}</li>' for x in fx['loc'])+'</ul></section>' if fx.get('loc') else ''))(CFX.get(k,{}))}
<section><h2>Previous Showings</h2><p class="big">{len(FR_)} Run{"s" if len(FR_)!=1 else ""} • {fcs} Festival{"s" if fcs!=1 else ""}</p>{f'<p class="big">{tks:,} tickets sold</p>' if tks else ''}{OGS}<h3>All runs on record ({len(FR_)}):</h3><ul class="runs fl">{runs}</ul></section>
<section><h2>More</h2><ul>{more}</ul></section></article>'''
    open(f'films/{v["slug"]}.html','w').write(page(f"{v['title']} — Stanford Theatre",DT(b),"../")); NFP+=1
print('COVERPAGES',NFP)
REDIR={'bread':'bread-love-and-dreams-pane-amore-e-fantasia','the-little-kidnappers-the-kidnappers':'the-kidnappers','steamboat-bill':'steamboat-bill-jr'}
for a_,b_ in REDIR.items():
    open(f'films/{a_}.html','w').write(f'<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>Moved</title><link rel="canonical" href="{SITE}films/{b_}.html"><meta http-equiv="refresh" content="0; url={b_}.html"></head><body><p>This page moved to <a href="{b_}.html">{b_}.html</a>.</p></body></html>')
FPM=dict({k:'films/'+s_+'.html' for k,s_ in FEATK.items()},**{k:'films/'+v['slug']+'.html' for k,v in COV.items()})
# ---- search page ----
SJS=open('tools/search.js').read(); SJS=_re0.sub(r'^var FP=\{.*?\};','var FP='+json.dumps(FPM)+';',SJS,count=1,flags=_re0.M)
sb=f'''<section class="fest"><h1 class="vh">Search Showings</h1><p class="sm">Billings from the theatre's history pages (1925 - 1961), its archived calendars (1997 - present) and Tile box-office records. </p>
<input id="q" type="search" placeholder="Film title, star, or year…" autofocus>
<div class="legend"><span class="li"><span class="badge og" title="{TOG}">{OG}</span> Original Billings (history pages)</span><span class="li"><span class="badge or" title="{TOR}">{OR}</span> Original Run</span><span class="li"><span class="badge s1">{S1}</span> first showing on record</span><span class="li"><span class="badge rt">{tk("5","#e8564f","#8e1a16","grt2")}</span> Nth run at the theatre</span></div>
<div id="count" class="sm"></div><ul id="res" class="res"></ul></section>
<script src="data/showings.js"></script><script>var OG={json.dumps(OG)},OR={json.dumps(OR)},S1={json.dumps(S1)},RT={json.dumps(tk("@N@","#e8564f","#8e1a16","grt"))},TOG={json.dumps(TOG)},TOR={json.dumps(TOR)};'''+SJS+'''</script>'''
open('search.html','w').write(page("Search — Stanford Theatre",sb,"","search"))

# ---- past festival pages ----
import os as _os
_os.makedirs('festivals/past',exist_ok=True)
for _f in [x for x in _os.listdir('festivals/past') if x.endswith('.html')]: _os.remove('festivals/past/'+_f)
_PF={}
for s_ in F: _PF[(NJ(F[s_]['t']),F[s_]['y'])]=s_
NPAST=0
def _pcard(fm):
    sl_=_PF.get((NJ(fm['title']),fm.get('year')))
    cv=COV.get(FKEY(fm['title'],fm.get('year')))
    if not sl_ and cv:
        im=f'<img src="../../{cv["poster"]}" alt="{e(cv["title"])} poster">' if cv['poster'] else ''
        return f'<div class="col"><a class="card{"" if im else " noimg"}" href="../../films/{cv["slug"]}.html">{im}<span>{e(cv["title"])}'+(f' ({cv["year"]})' if cv['year'] else '')+'</span>'+(f'<small>{cv["rt"]} min</small>' if cv['rt'] else '')+'</a></div>'
    fm=dict(fm,title=ALI(fm['title']))
    yr=f" ({fm['year']})" if fm.get('year') else ''
    tm=''
    if sl_:
        return f'<div class="col"><a class="card" href="../../films/{sl_}.html"><img src="../../posters/{sl_}.jpg" alt="{e(F[sl_]["t"])} poster"><span>{e(F[sl_]["t"])} ({F[sl_]["y"]})</span><small>{F[sl_]["rt"]} min</small></a>{tm}</div>'
    return f'<div class="col"><div class="card noimg"><span>{e(fm["title"])}{yr}</span></div>{tm}</div>'
for fe in FJ['festivals']:
    if not fe['blocks']: continue
    dr=hr(fe['start'],fe['end']) if fe['start'] else (str(fe['year']) if fe['year'] else 'Year not given')
    bills=''.join(f'<section class="fest blk"><h3 class="bl">{e(fullmo(b["dates"]))}{ANB(b)}</h3><div class="cols">'+''.join(_pcard(fm) for fm in b['films'])+'</div></section>' for b in fe['blocks'])
    q=urllib.parse.quote(fe['file'])
    body=f'<section class="fest"><div class="dr dtop" style="text-align:center">{e(dr)}</div><h1>{e(fe["name"])}</h1><p class="sm" style="text-align:center">{len(fe["blocks"])} bill{"s" if len(fe["blocks"])!=1 else ""}</p></section>'+bills+f'<p class="sm" style="text-align:center"><a href="../archive/cal/{q}">Archived calendar page</a> · <a href="https://www.stanfordtheatre.org/calendars/{q}">Original</a> · <a href="../../past.html">All past festivals</a></p>'
    open(f'festivals/past/{PSLUG(fe)}.html','w').write(page(f"{fe['name']} — Stanford Theatre",body,"../../","past")); NPAST+=1
print('PASTPAGES',NPAST)
# --- Original runs by year on past.html (pre-festival era) ---
_OR=sorted([o for o in SH if o.get('badge')=='Original Run'],key=lambda o:(o['start'],o.get('n',0)))
_YRS={}
for o in _OR: _YRS.setdefault(o['start'][:4],[]).append(o)
Y=['<section class="fest oryrs" id="original-runs"><h2 style="text-align:center;margin-top:30px">Original Runs by Year</h2><p class="sm" style="text-align:center">The theatre&#39;s first-run billings, '+min(_YRS)+'–'+max(_YRS)+', from its history pages. Labels mark shorts, newsreels, stage acts, special events, and entries not yet verified as films.</p><nav class="yrnav">'+''.join(f'<a href="#y{y}">{y}</a>' for y in sorted(_YRS))+'</nav>']
for y in sorted(_YRS):
    li=''
    for o in _YRS[y]:
        fp=FPM.get(FKEY(o['title'],int(o['start'][:4]))) if o.get('type')=='feature' else None
        tt=f'<a href="{e(fp)}">{e(o["title"])}</a>' if fp else e(o['title'])
        if o['start']=='1925-06-09' and '<p class="opd"' not in li: li+='<p class="opd"><span class="an100">Opening Day</span> June 9, 1925 — the Stanford Theatre opens</p>'
        li+=f'<li><span class="yd">{e(FRp(o["start"],o.get("end")) or o["start"])}</span> {TYB(o)}<b>{tt}</b>'+(f' <span class="rn">· {e(o["note"])}</span>' if o.get('note') else '')+'</li>'
    Y.append(f'<details class="fest arch yr" id="y{y}"><summary><span class="an yh">{y}</span> <span class="dr">{len(_YRS[y])} showing{"s" if len(_YRS[y])!=1 else ""}</span></summary><ul class="yl">{li}</ul><p class="sm"><a href="history/years/{y}.htm">Archived history page</a></p></details>')
Y.append('</section><script>(function(){function o(){var h=location.hash;if(/^#y\\d{4}$/.test(h)){var d=document.querySelector(h);if(d)d.open=true;}}addEventListener("hashchange",o);o();})();</script>')
open('past.html','w').write(page("Past — Stanford Theatre","".join(P)+"".join(Y),"","past"))
print('ORYEARS',len(_YRS),len(_OR))
