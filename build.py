import json,html,datetime
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
def page(title,body,root=""):
    return f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(title)}</title><link rel="stylesheet" href="{root}style.css"></head><body>
<header class="mq"><a href="{root}index.html"><div class="m1">THE STANFORD THEATRE</div><div class="m2">PALO ALTO · NOW SHOWING</div></a></header><main>{body}</main>
<footer><a href="{MAP}">Stanford Theatre, 221 University Ave, Palo Alto, CA 94301</a><div class="sm">Schedules subject to change — check <a href="https://www.stanfordtheatre.org/calendar.html">stanfordtheatre.org</a>.</div></footer></body></html>'''
def ft(s): f=F[s]; return f"{e(f['t'])} ({f['y']})"
h=['<section class="intro"><h1>Upcoming Programs</h1></section>']
for name,dr,url,groups,films in FEST:
    h.append(f'<section class="fest"><h2><a href="{url}">{e(name)}</a></h2><div class="dr">{dr}</div><div class="cols">')
    for s in films:
        st="".join(f'<div class="dg">{d}</div><div class="tm">{t}</div>' for d,items in groups for a2,t in items if a2==s)
        h.append(f'<div class="col"><a class="card" href="films/{s}.html"><img src="posters/{s}.jpg" alt="{e(F[s]["t"])} poster"><span>{ft(s)}</span><small>{F[s]["rt"]} min</small></a>{st}</div>')
    h.append('</div></section>')
open('index.html','w').write(page("Stanford Theatre — Now Showing","".join(h)))
for s,k in K.items():
    f=F[s];t=T[k]
    fest=[x for x in FEST if s in x[4]][0]
    sched="".join(f'<h3>{d}</h3><ul class="sched">'+"".join(f'<li>{"<b>" if a==s else ""}{ft(a)}: {tt}{"</b>" if a==s else ""}</li>' for a,tt in items)+'</ul>' for d,items in fest[3])
    runs="".join(f'<li><span class="rd">{int(r["start"][5:7])}/{r["start"][:4]}</span> {r["tickets"]:,} tickets'+(f'<br><span class="pair">w/ {e(r["pair"])}</span>' if r["pair"]!="alone" else '')+'</li>' for r in t['runs'])
    li=lambda L:"".join(f'<li>{x}</li>' for x in L)
    b=f'''<article class="film"><div class="top"><img class="poster" src="../posters/{s}.jpg" alt="{e(f['t'])} poster">
<div><h1>{e(f['t'])}</h1><div class="meta">{f['y']} ★ {f['rt']} min</div><p class="cr">{e(f['credit'])}</p><p class="plot">{e(f['plot'])}</p></div></div>
<section><h2>Schedule</h2><div class="dr"><a href="{fest[2]}">{e(fest[0])}</a> · {fest[1]}</div>{sched}</section>
<section><h2>Trivia</h2><ul>{li(f['rick'])}</ul></section>
<section><h2>Filming Locations</h2><ul>{li(f['loc'])}</ul></section>
<section><h2>Previous Showings</h2><p class="big">{t['tc']} Showings • {t['fc']} Festivals</p><p class="big">{t['tk']} tickets sold</p><h3>Past runs (since '03):</h3><ul class="runs">{runs}</ul></section>
<section><h2>More</h2><ul><li><a href="https://tile.stanfordtheatre.org/tile?q={TQ[k]}">Tile: {e(f['t'])}</a></li><li><a href="https://www.imdb.com/title/{IMDB[k]}/">IMDb: {e(f['t'])}</a></li><li><a href="../infographics/{s}.png" download>Download infographic (PNG)</a></li></ul><a href="../infographics/{s}.png"><img class="ig" src="../infographics/{s}.png" alt="{e(f['t'])} infographic"></a></section></article>'''
    open(f'films/{s}.html','w').write(page(f"{f['t']} — Stanford Theatre",b,"../"))
