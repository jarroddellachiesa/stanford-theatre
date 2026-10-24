import json,urllib.request,urllib.parse,io,re
from PIL import Image
UA={'User-Agent':'StanfordTheatreFanSite/1.0 (jarroddellachiesa@users.noreply.github.com)'}
T=[ # studio (canonical era name), wikidata names, from, to, commons file
 ('Metro-Goldwyn-Mayer',['Metro-Goldwyn-Mayer'],1924,1964,'Metro-Goldwyn-Mayer 1924-1964.png'),
 ('Paramount Pictures',['Paramount Pictures'],1929,1936,'Paramount Pictures (1929-1936).jpg'),
 ('20th Century-Fox',['20th Century Studios'],1935,1984,'20th Century Fox logo.svg'),
 ('Radio Pictures',['RKO Pictures'],1929,1932,'Radio Pictures 1929.jpg'),
 ('RKO Radio Pictures',['RKO Pictures'],1933,1935,'RKO Radio Pictures 1933.png'),
 ('RKO Radio Pictures',['RKO Pictures'],1936,1936,'RKO Radio Pictures 1936.png'),
 ('RKO Radio Pictures',['RKO Pictures'],1937,1957,'RKO Radio Pictures 1937.png'),
 ('Warner Bros. Pictures',['Warner Bros. Entertainment'],1929,1936,'Warner Bros. Pictures Inc. 1929.jpg'),
 ('Warner Bros. Pictures',['Warner Bros. Entertainment'],1937,1967,'Warner Bros old logo.svg'),
# white-mark conversion too noisy (photo); text fallback
 #('Columbia Pictures',['Columbia Pictures'],1928,1931,'Columbia Pictures logo 1928.jpg'),
 ('Columbia Pictures',['Columbia Pictures'],1932,1932,'Columbia Pictures 1932-1933.png'),
 ('Columbia Pictures',['Columbia Pictures'],1933,1937,'Columbia Pictures 1933.png'),
 ('Columbia Pictures',['Columbia Pictures'],1938,1944,'Columbia Pictures 1938.png'),
 ('Columbia Pictures',['Columbia Pictures'],1945,1975,'Columbia Pictures 1945.jpg'),
 ('Universal Pictures',['Universal Pictures'],1936,1945,'Universal Pictures 1936.png'),
 ('Universal Pictures',['Universal Pictures'],1963,1990,'Universal Pictures 1963.png'),
 ('Toho',['Toho'],1932,2000,'Toho logo.svg'),
]
out=[]
for name,wd,a,b,f in T:
    u='https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode(dict(action='query',format='json',titles='File:'+f,prop='imageinfo',iiprop='url|extmetadata',iiurlwidth=480,iiextmetadatafilter='LicenseShortName|Artist'))
    p=list(json.load(urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=30))['query']['pages'].values())[0]; ii=p['imageinfo'][0]
    fn='assets/studios/'+re.sub(r'[^a-z0-9]+','-',f.rsplit('.',1)[0].lower()).strip('-')+'.png'
    im=Image.open(io.BytesIO(urllib.request.urlopen(urllib.request.Request(ii['thumburl'],headers=UA),timeout=30).read())).convert('RGBA'); im.thumbnail((480,200)); im.save(fn,optimize=True)
    out.append(dict(studio=name,wikidata_names=wd,from_year=a,to_year=b,file=fn,source=ii['descriptionurl'],license=ii['extmetadata'].get('LicenseShortName',{}).get('value')))
json.dump(dict(logos=out,renames=[
 dict(wikidata='Walt Disney Pictures',to_year=1985,name='Walt Disney Productions'),
 dict(wikidata='20th Century Studios',to_year=1934,name='Fox Film Corporation'),
 dict(wikidata='20th Century Studios',from_year=1935,to_year=1984,name='20th Century-Fox'),
 dict(wikidata='Warner Bros. Entertainment',name='Warner Bros. Pictures'),
 dict(wikidata='RKO Pictures',to_year=1932,name='Radio Pictures'),
 dict(wikidata='RKO Pictures',from_year=1933,to_year=1959,name='RKO Radio Pictures'),
 dict(wikidata='Universal Pictures',from_year=1946,to_year=1963,name='Universal-International')]),open('data/studio_logos.json','w'),indent=1)
print(len(out),[o['license'] for o in out])
