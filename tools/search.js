var D=window.SHOWINGS,q=document.getElementById('q'),R=document.getElementById('res'),C=document.getElementById('count');
var FP={"north by northwest":"films/north-by-northwest.html","on waterfront":"films/on-the-waterfront.html","mary poppins":"films/mary-poppins.html","wizard of oz":"films/the-wizard-of-oz.html"};
function esc(s){return String(s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function N(s){s=String(s).normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().replace(/&/g,' and ').replace(/['’`]/g,'').replace(/[^a-z0-9]+/g,' ');return s.split(' ').filter(function(w){return w&&w!='the'&&w!='a'&&w!='an'}).map(function(w){return w.length>4&&/ing$/.test(w)?w.slice(0,-1):w}).join(' ')}
function TK(s){return s?s.split(' '):[]}
function ED(a,b,k){if(Math.abs(a.length-b.length)>k)return false;var p=[],i,j;for(j=0;j<=b.length;j++)p[j]=j;for(i=1;i<=a.length;i++){var c=[i],mn=i;for(j=1;j<=b.length;j++){c[j]=Math.min(p[j]+1,c[j-1]+1,p[j-1]+(a[i-1]==b[j-1]?0:1));if(c[j]<mn)mn=c[j]}if(mn>k)return false;p=c}return p[b.length]<=k}
function ord(n){var s=['th','st','nd','rd'],v=n%100;return n+(s[(v-20)%10]||s[v]||s[0])}
function badge(o){var h='';if(o.source!='Tile'&&o.source!='Stanford Theatre calendars')h+='<span class="badge og" title="'+TOG+'">'+OG+'</span> ';
if(o.badge)h+='<span class="badge or" title="'+TOR+'">'+OR+'</span> ';
if(o.n==1&&!o.badge)h+='<span class="badge s1" title="First showing at the Stanford Theatre on record">'+S1+'</span>';else if(o.n>1)h+='<span class="badge rt" title="'+ord(o.n)+' run at the Stanford Theatre on record">'+RT.replace('@N@',o.n)+'</span>';return h}
function MR(its){var R=[],M={};its.forEach(function(x){var o=x.o;if(!o.run){R.push(o);return}var m=M[o.run];
if(!m){m=M[o.run]={title:o.title,source:o.source,start:o.start,end:o.end,date_text:o.date_text,url:o.url,note:o.note||'',n:o.n,badge:o.badge||'',run:o.run,tickets:null,srcs:{}};R.push(m)}
m.srcs[o.source]=1;if(o.badge)m.badge=o.badge;if(o.start<m.start)m.start=o.start;if((o.end||o.start)>(m.end||m.start))m.end=o.end;
if(o.source!='Tile'&&m.source=='Tile'){m.source=o.source;m.url=o.url;m.date_text=o.date_text}if(o.source!='Tile'&&o.note&&!m._nn){m.note=o.note;m._nn=1}else if(!m.note&&o.note)m.note=o.note;
if(o.tickets!=null)m.tickets=(m.tickets||0)+o.tickets});
R.forEach(function(m){if(m.srcs&&m.srcs['Tile']&&m.source!='Tile'){m.date_text=null}});return R}
var MN=['January','February','March','April','May','June','July','August','September','October','November','December'];
function MX(t){var ab={Jan:0,Feb:1,Mar:2,Apr:3,Jun:5,Jul:6,Aug:7,Sep:8,Sept:8,Oct:9,Nov:10,Dec:11};t=String(t).replace(/\b(Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sept|Sep|Oct|Nov|Dec)\b\.?(?=\s*\d)/g,function(m,a){return MN[ab[a]]});
return t.replace(new RegExp('\\b(('+MN.join('|')+') \\d{1,2})\\s*[–—-]\\s*(?=\\d|(?:'+MN.join('|')+') )','g'),'$1 - ').replace(/(day)\s*[–—]\s*(?=[A-Z])/g,'$1 - ')}
function FR(a,b){var A=a.split('-').map(Number),B=(b||a).split('-').map(Number);if(!A[1]||!A[2])return null;var m=function(x){return MN[x[1]-1]+' '+x[2]},f;
if(!B[1]||!B[2]||a==b||!b)f=m(A)+', '+A[0];else if(A[0]!=B[0])f=m(A)+', '+A[0]+' - '+m(B)+', '+B[0];else if(A[1]==B[1])f=m(A)+' - '+B[2]+', '+A[0];else f=m(A)+' - '+m(B)+', '+A[0];
if(f.length>38){var g=function(x){return x[1]+'/'+String(x[0]%100).padStart(2,'0')};f=g(A)==g(B)?g(A):g(A)+' - '+g(B)}return f}
function dd(o){if(o.source=='Tile'||!o.date_text)return FR(o.start,o.end)||o.start;var x=(o.date_text||'').match(/\(([^)]*day[^)]*)\)/),r=FR(o.start,o.end);return r?r+(x?' ('+MX(x[1])+')':''):MX(o.date_text||o.start)}
function score(nt,nq,qt){if(!nq)return -1;if(nt==nq)return 0;if(nt.indexOf(nq)>=0)return 1;var t=TK(nt);if(qt.length&&qt.every(function(x){return t.some(function(w){return w.indexOf(x)==0||(x.length>=4&&ED(x,w,x.length>=7?2:1))})}))return 2;return -1}
function go(){var v=q.value.trim();if(v.length<2){R.innerHTML='';C.textContent=D.length.toLocaleString()+' showings indexed. Type at least 2 characters.';return}
var nq=N(v),qa=TK(nq),qt=qa.filter(function(x){return x.length>=4});if(!qt.length)qt=qa;
if(/^[\d\s\/\-]+$/.test(v)){var m=D.filter(function(o){return (o.start+' '+(o.date_text||'')).indexOf(v)>=0});C.textContent=m.length.toLocaleString()+' matches'+(m.length>300?' (showing first 300)':'');
R.innerHTML=m.slice(0,300).map(function(o){return '<li class="sl">'+badge(o)+' <a href="'+esc(o.url)+'">'+esc(o.title)+'</a> <span class="rd2">'+esc(dd(o))+'</span></li>'}).join('');return}
var G={};D.forEach(function(o){if(!o._t)o._t=N(o.title);var s=score(o._t,nq,qt),key,name,pw='';
if(s>=0){key=o.run?o.run.replace(/\|\d+$/,''):o._t;name=o.title}
if(key==null)return;var g=G[key]||(G[key]={name:name,s:s,items:[],yr:null});if(s<g.s)g.s=s;if(s<3)g.name=o.title;if(o.year)g.yr=o.year;else if(o.fyear&&!g.yr)g.yr=o.fyear;g.items.push({o:o,pw:pw})});
var gs=Object.keys(G).map(function(k){var g=G[k];g.k=k;return g}).sort(function(a,b){return a.s-b.s||b.items.length-a.items.length});
var tot=gs.reduce(function(a,g){return a+g.items.length},0);C.textContent=gs.length+' film'+(gs.length==1?'':'s')+' · '+tot.toLocaleString()+' showings'+(gs.length>40?' (first 40 films)':'');
R.innerHTML=gs.slice(0,40).map(function(g){var t=esc(g.name)+(g.yr?' ('+g.yr+')':''),fp=FP[g.k];
var its=MR(g.items.sort(function(a,b){return a.o.start<b.o.start?-1:a.o.start>b.o.start?1:0})).map(function(o){return {o:o,pw:''}});
return '<li class="fg"><div class="fh">'+(fp?'<a href="'+fp+'">'+t+'</a>':t)+' <span class="fc">'+its.length+' run'+(its.length==1?'':'s')+'</span></div><ul class="fl">'+its.map(function(x){var o=x.o,n=x.pw?'w/ '+x.pw:(o.note||'');
return '<li>'+badge(o)+' <a class="sd" href="'+esc(o.url)+'">'+esc(dd(o))+'</a>'+(o.tickets!=null?' · '+o.tickets.toLocaleString()+' tickets':'')+(n?' <span class="rn">· '+esc(n)+'</span>':'')+'</li>'}).join('')+'</ul></li>'}).join('')}
q.addEventListener('input',go);var u=new URLSearchParams(location.search).get('q');if(u)q.value=u;go();
