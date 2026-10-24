# builds data/title_aliases.json from alias_gen heuristics + curated rules
import json,re,collections
exec(open('tools/alias_gen.py').read().split('# fuzzy')[0])
DROP_GROUPS=['bad seed','seventh heaven','christmas carol','babes in toyland']   # questions, not merged
for t in list(AL):
    if any(x in NK(t) or x in NK(AL[t]) for x in DROP_GROUPS): del AL[t]
# Gaslight: keep UK 1940 separate from Gaslight 1944
for t in ['Gaslight (UK version)','Gaslight (UK)','Gaslight']: AL.pop(t,None)
AL['Gaslight (UK)']='Gaslight (UK version)'
# Big City (1937) is not Mahanagar
AL.pop('Big City',None); AL['The Big City (Mahanagar)']='Mahanagar'
for t in [k for k,v in AL.items() if NK(v)=='big city']: AL.pop(t)
CANON={'bride of frankenstein':'Bride of Frankenstein','bachelor and bobby soxer':'The Bachelor and the Bobby-Soxer','100 men and girl':'One Hundred Men and a Girl','adventures of robin hood':'The Adventures of Robin Hood','freshman':'The Freshman','show boat':'Show Boat','3 godfathers':'3 Godfathers'}
FIX={'Bah, Wilderness!':'Ah, Wilderness!','Captain from Castille':'Captain from Castile','Diary of Ann Frank':'The Diary of Anne Frank','Gold Digger of 1933':'Gold Diggers of 1933',
"Interns Can't Take Money":"Internes Can't Take Money",'Kanchenjunga':'Kanchenjungha',"Lady Windemere's Fan":"Lady Windermere's Fan",'Libelled Lady':'Libeled Lady',
'Lightening Strikes Twice':'Lightning Strikes Twice','Madame Satan':'Madam Satan','The Man Who Shot Liberty Valence':'The Man Who Shot Liberty Valance',
'Passage to Marseilles':'Passage to Marseille','The Scarlett Empress':'The Scarlet Empress','The Scarlett Pimpernel':'The Scarlet Pimpernel','Syvia Scarlett':'Sylvia Scarlett',
'Tanks a Million':'Thanks a Million','The Thief of Baghdad':'The Thief of Bagdad','Ziegfield Girl':'Ziegfeld Girl','Stanley and Livingston':'Stanley and Livingstone'}
# map fuzzy fixes by key to actual raw variants
for bad,good in FIX.items():
    kb,kg=SK(bad),SK(good)
    for t in src:
        s=SK(t)
        if s==kb: AL[t]=good
        elif s==kg: AL[t]=good
for t in src:
    c=CANON.get(NK(AL.get(t,t)))
    if c: AL[t]=c
AL.update({'Sunset Blvd':'Sunset Boulevard','Sunset Blvd.':'Sunset Boulevard','Sherlock, Jr.':'Sherlock Jr.','The Little Kidnappers (The Kidnappers)':'The Kidnappers','The Seven Samurai':'Seven Samurai','100 Men and a Girl':'One Hundred Men and a Girl'})
AL={k:v for k,v in AL.items() if k!=v}
REMAKES={'beau geste':[1926,1939],'cat and canary':[1927,1939],'monkey business':[1931,1952],'waterloo bridge':[1931,1940],'merry widow':[1925,1934],'mark of zorro':[1920,1940],'man who knew too much':[1934,1956],'lover come back':[1946,1961],'little women':[1933,1949],'liliom':[1930,1934],'state fair':[1933,1945],'imitation of life':[1934,1959],'kismet':[1944,1955],'cleopatra':[1934,1963],'stella dallas':[1925,1937],'importance of being earnest':[1952],'phantom of opera':[1925,1943]}
_old=json.load(open('data/title_aliases.json'))['aliases'] if __import__('os').path.exists('data/title_aliases.json') else {}
_old.update(AL); AL=_old
json.dump(dict(aliases=dict(sorted(AL.items())),remakes=REMAKES),open('data/title_aliases.json','w'),indent=1,ensure_ascii=False)
print('aliases',len(AL))
