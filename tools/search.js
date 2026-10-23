var D=window.SHOWINGS,q=document.getElementById('q'),R=document.getElementById('res'),C=document.getElementById('count');
var FP={"north by northwest":"films/north-by-northwest.html","on waterfront":"films/on-the-waterfront.html","mary poppins":"films/mary-poppins.html","wizard of oz":"films/the-wizard-of-oz.html"};
function esc(s){return String(s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function N(s){s=String(s).normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().replace(/&/g,' and ').replace(/['’`]/g,'').replace(/[^a-z0-9]+/g,' ');return s.split(' ').filter(function(w){return w&&w!='the'&&w!='a'&&w!='an'}).map(function(w){return w.length>4&&/ing$/.test(w)?w.slice(0,-1):w}).join(' ')}
function TK(s){return s?s.split(' '):[]}
function ED(a,b,k){if(Math.abs(a.length-b.length)>k)return false;var p=[],i,j;for(j=0;j<=b.length;j++)p[j]=j;for(i=1;i<=a.length;i++){var c=[i],mn=i;for(j=1;j<=b.length;j++){c[j]=Math.min(p[j]+1,c[j-1]+1,p[j-1]+(a[i-1]==b[j-1]?0:1));if(c[j]<mn)mn=c[j]}if(mn>k)return false;p=c}return p[b.length]<=k}
function ord(n){var s=['th','st','nd','rd'],v=n%100;return n+(s[(v-20)%10]||s[v]||s[0])}
function badge(o){if(o.source=='Stanford Theatre calendars')return '<span class="src">Calendar</span>'+(o.badge?' <span class="badge or" title="'+TOR+'">'+OR+'</span>':'');
if(o.source=='Tile')return o.n==1?'<span class="badge s1" title="First showing in Tile records">'+S1+'</span>':'<span class="badge rt" title="'+ord(o.n)+' time shown (Tile records)">'+RT.replace('@N@',o.n)+'</span>';
return '<span class="badge og" title="'+TOG+'">'+OG+'</span>'+(o.badge?' <span class="badge or" title="'+TOR+'">'+OR+'</span>':'')}
function dd(o){return o.source=='Tile'?(o.start+(o.end!=o.start?' – '+o.end:'')):o.date_text}
function score(nt,nq,qt){if(!nq)return -1;if(nt==nq)return 0;if(nt.indexOf(nq)>=0)return 1;var t=TK(nt);if(qt.length&&qt.every(function(x){return t.some(function(w){return w.indexOf(x)==0||(x.length>=4&&ED(x,w,x.length>=7?2:1))})}))return 2;return -1}
function go(){var v=q.value.trim();if(v.length<2){R.innerHTML='';C.textContent=D.length.toLocaleString()+' showings indexed. Type at least 2 characters.';return}
var nq=N(v),qa=TK(nq),qt=qa.filter(function(x){return x.length>=4});if(!qt.length)qt=qa;
if(/^[\d\s\/\-]+$/.test(v)){var m=D.filter(function(o){return (o.start+' '+(o.date_text||'')).indexOf(v)>=0});C.textContent=m.length.toLocaleString()+' matches'+(m.length>300?' (showing first 300)':'');
R.innerHTML=m.slice(0,300).map(function(o){return '<li class="sl">'+badge(o)+' <a href="'+esc(o.url)+'">'+esc(o.title)+'</a> <span class="rd2">'+esc(dd(o))+'</span></li>'}).join('');return}
var G={};D.forEach(function(o){if(!o._t)o._t=N(o.title);var s=score(o._t,nq,qt),key,name,pw='';
if(s>=0){key=o._t;name=o.title}else if(o.source=='Tile'&&o.note&&o.note.indexOf('w/ ')==0){var ps=o.note.slice(3).split(', ');for(var i=0;i<ps.length;i++){var np=N(ps[i]);if(score(np,nq,qt)>=0){key=np;name=ps[i];s=3;pw=o.title;break}}}
if(key==null)return;var g=G[key]||(G[key]={name:name,s:s,items:[],yr:null});if(s<g.s)g.s=s;if(s<3)g.name=o.title;if(o.fyear&&!g.yr)g.yr=o.fyear;g.items.push({o:o,pw:pw})});
var gs=Object.keys(G).map(function(k){var g=G[k];g.k=k;return g}).sort(function(a,b){return a.s-b.s||b.items.length-a.items.length});
var tot=gs.reduce(function(a,g){return a+g.items.length},0);C.textContent=gs.length+' film'+(gs.length==1?'':'s')+' · '+tot.toLocaleString()+' showings'+(gs.length>40?' (first 40 films)':'');
R.innerHTML=gs.slice(0,40).map(function(g){var t=esc(g.name)+(g.yr?' ('+g.yr+')':''),fp=FP[g.k];
var its=g.items.sort(function(a,b){return a.o.start<b.o.start?-1:a.o.start>b.o.start?1:0});
return '<li class="fg"><div class="fh">'+(fp?'<a href="'+fp+'">'+t+'</a>':t)+' <span class="fc">'+its.length+' showing'+(its.length==1?'':'s')+'</span></div><ul class="fl">'+its.map(function(x){var o=x.o,n=x.pw?'w/ '+x.pw:(o.note||'');
return '<li>'+badge(o)+' <a class="sd" href="'+esc(o.url)+'">'+esc(dd(o))+'</a>'+(o.tickets!=null?' · '+o.tickets.toLocaleString()+' tickets':'')+(n?' <span class="rn">· '+esc(n)+'</span>':'')+'</li>'}).join('')+'</ul></li>'}).join('')}
q.addEventListener('input',go);var u=new URLSearchParams(location.search).get('q');if(u)q.value=u;go();
