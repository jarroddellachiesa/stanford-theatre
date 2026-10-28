# Make WebP poster variants: python3 tools/make_webp.py posters/s 480 ; python3 tools/make_webp.py posters/w 1200  (JPG originals untouched)
import sys
D,W=sys.argv[1],int(sys.argv[2])
import os,glob
from PIL import Image
from concurrent.futures import ProcessPoolExecutor
def f(p):
    o=D+'/'+p[len('posters/'):-4]+'.webp'
    if os.path.exists(o) and os.path.getmtime(o)>=os.path.getmtime(p): return 0
    os.makedirs(os.path.dirname(o),exist_ok=True)
    im=Image.open(p); im=im.convert('RGBA' if im.mode in('RGBA','LA','P') and 'transparency' in im.info or im.mode=='RGBA' else 'RGB')
    if D.endswith('/w') and im.width<=480: return 0
    if im.width>W: im=im.resize((W,round(im.height*W/im.width)),Image.LANCZOS)
    im.save(o,'WEBP',quality=80,method=6); return 1
ps=[p for p in glob.glob('posters/**/*.jpg',recursive=True) if not p.startswith(D+'/')]
with ProcessPoolExecutor() as ex: print(sum(ex.map(f,ps,chunksize=8)),len(ps))
# drop WebPs that don't save at least 10% vs the JPG (pages then fall back to the JPG)
for o in glob.glob(D+'/**/*.webp',recursive=True):
    j='posters/'+o[len(D)+1:-5]+'.jpg'
    if os.path.getsize(o)>=os.path.getsize(j)*0.9: os.remove(o)
