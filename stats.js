/* Box-office stats: AES-GCM ciphertext in data/stats.enc.json, unlocked in-browser with a password (PBKDF2). */
(function(){
var R=(document.currentScript&&document.currentScript.dataset.root)||'',K='st-stats-key',D=null;
function b64(s){var b=atob(s),u=new Uint8Array(b.length);for(var i=0;i<b.length;i++)u[i]=b.charCodeAt(i);return u}
function u2b(u){var s='';u=new Uint8Array(u);for(var i=0;i<u.length;i++)s+=String.fromCharCode(u[i]);return btoa(s)}
function enc(){return fetch(R+'data/stats.enc.json',{cache:'no-cache'}).then(function(r){if(!r.ok)throw 0;return r.json()})}
function derive(pw,E){return crypto.subtle.importKey('raw',new TextEncoder().encode(pw),'PBKDF2',false,['deriveBits']).then(function(k){return crypto.subtle.deriveBits({name:'PBKDF2',hash:'SHA-256',salt:b64(E.salt),iterations:E.iter},k,256)})}
function dec(raw,E){return crypto.subtle.importKey('raw',raw,'AES-GCM',false,['decrypt']).then(function(k){return crypto.subtle.decrypt({name:'AES-GCM',iv:b64(E.iv)},k,b64(E.ct))}).then(function(p){return JSON.parse(new TextDecoder().decode(p))})}
function stored(){try{return sessionStorage.getItem(K)||localStorage.getItem(K)}catch(e){return null}}
function n(x){return x.toLocaleString()} function $(x){return '$'+x.toLocaleString()}
function fd(d){var p=d.split('-');return ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'][+p[1]-1]+' '+(+p[2])+', '+p[0]}
function sum(days){var a=0,g=0;days.forEach(function(d){a+=d[2];g+=d[3]});return [a,g]}
function reveal(){
  document.documentElement.classList.add('st-unlocked');var L=document.getElementById('stlock');if(L){L.innerHTML='&#128275;';L.title='Lock stats'}
  var F=D.films||{},m=location.pathname.match(/films\/([^\/]+)\.html$/);
  var TL=D.tile||{},mu=document.getElementById('more');if(m&&TL[m[1]]&&mu&&!document.getElementById('stl')){var li=document.createElement('li');li.id='stl';var al=document.createElement('a');al.href=TL[m[1]];al.textContent=(D.tl||'')+': '+((document.querySelector('h1')||{}).textContent||'');li.appendChild(al);mu.insertBefore(li,mu.firstChild)}
  if(m&&F[m[1]]&&!document.getElementById('stx')){
    var runs=F[m[1]],T=[0,0],h='<section id="stx" class="stx"><h2>Box Office</h2>';
    runs.forEach(function(r){var s=sum(r.days);T[0]+=s[0];T[1]+=s[1];
      h+='<div class="strun"><div class="sth">Program <b>'+r.prog+'</b>'+(r.pair.length?' · w/ '+r.pair.join(', '):' · plays alone')+'</div><table><tr><th>Date</th><th></th><th>Attend.</th><th>Gross</th></tr>'+
      r.days.map(function(d){return '<tr><td>'+fd(d[0])+'</td><td>'+d[1]+'</td><td>'+n(d[2])+'</td><td>'+$(d[3])+'</td></tr>'}).join('')+
      '<tr class="stt"><td colspan="2">Run total</td><td>'+n(s[0])+'</td><td>'+$(s[1])+'</td></tr></table></div>'});
    h+='<p class="stft">All runs: <b>'+n(T[0])+'</b> admissions · <b>'+$(T[1])+'</b> gross · '+runs.length+' program'+(runs.length!=1?'s':'')+'</p></section>';
    var tgt=document.querySelector('main')||document.body,ft=document.querySelector('footer');
    var w=document.createElement('div');w.innerHTML=h;ft?ft.parentNode.insertBefore(w.firstChild,ft):tgt.appendChild(w.firstChild);
  }
  document.querySelectorAll('section[data-start]').forEach(function(sec){
    var a=sec.dataset.start,b=sec.dataset.end||a;if(!a||sec.querySelector('.stb'))return;
    var P={},seen={},A=0,G=0;
    sec.querySelectorAll('a.card').forEach(function(c){var mm=(c.getAttribute('href')||'').match(/films\/([^\/]+)\.html/);if(!mm||!F[mm[1]])return;
      F[mm[1]].forEach(function(r){r.days.forEach(function(d){if(d[0]>=a&&d[0]<=b){P[r.prog]=1;var k=r.prog+'|'+d[0];if(!seen[k]){seen[k]=1;A+=d[2];G+=d[3]}}})})});
    var ks=Object.keys(P);if(!ks.length)return;var x=document.createElement('div');x.className='stb';
    x.textContent='Program #'+ks.join(', #')+' · '+n(A)+' admissions · '+$(G);
    var cols=sec.querySelector('.cols');cols?cols.parentNode.insertBefore(x,cols.nextSibling):sec.appendChild(x)});
}
function unlock(raw){return enc().then(function(E){return dec(raw,E)}).then(function(d){D=d;reveal();return true})}
function lock(){try{sessionStorage.removeItem(K);localStorage.removeItem(K)}catch(e){}location.reload()}
function ask(){
  var dlg=document.createElement('div');dlg.className='stdlg';dlg.innerHTML='<form><label>Stats password</label><input type="password" autocomplete="current-password" required><label class="strem"><input type="checkbox"> Remember on this device</label><p class="sterr" hidden>That password didn\u2019t work — please try again.</p><div><button type="button" class="stc0">Cancel</button><button type="submit">Unlock</button></div></form>';
  document.body.appendChild(dlg);var f=dlg.querySelector('form'),i=f.querySelector('input[type=password]');i.focus();
  dlg.querySelector('.stc0').onclick=function(){dlg.remove()};
  f.onsubmit=function(ev){ev.preventDefault();var er=f.querySelector('.sterr');er.hidden=true;
    enc().then(function(E){return derive(i.value,E).then(function(raw){return dec(raw,E).then(function(d){
      var s=u2b(raw);try{(f.querySelector('.strem input').checked?localStorage:sessionStorage).setItem(K,s)}catch(e){}D=d;dlg.remove();reveal()})})})
    .catch(function(){er.hidden=false;i.select()})};
}
document.addEventListener('DOMContentLoaded',function(){
  var L=document.getElementById('stlock');if(!L||!window.crypto||!crypto.subtle){if(L)L.hidden=true;return}
  L.onclick=function(){D?lock():ask()};
  var s=stored();if(s)unlock(b64(s)).catch(function(){try{sessionStorage.removeItem(K);localStorage.removeItem(K)}catch(e){}});
});
})();
