import re
def clean(t):
    t=re.sub(r'^(week \d+( & \d+)?|plus|also|extra!?|new|latest)\s*[-:]?\s*','',t,flags=re.I)
    t=re.sub(r'\s*\((?:19|20)\d\d\)\s*$','',t); t=re.sub(r'\s*[\(—–;].*$','',t) if not re.match(r'^[^(]*\)$',t) else t
    return t.strip(' "-:')
