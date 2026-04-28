import requests
import json
from pathlib import Path

DATA_DIR = Path('C:/Users/Administrator/.gemini/antigravity/data/fb-publisher')
with open(DATA_DIR / 'config' / 'fanpages.json', 'r', encoding='utf-8') as f:
    cfg = json.load(f)

base = 'https://graph.facebook.com/v19.0'

for page in cfg['pages']:
    name = page['name']
    pid = page['id']
    token = page['access_token']
    try:
        r = requests.get(
            base + '/' + pid,
            params={'fields': 'name,id', 'access_token': token},
            timeout=10
        )
        d = r.json()
        if 'error' in d:
            err_msg = d['error']['message'][:100]
            print('FAIL [' + name + ']: ' + err_msg)
        else:
            print('OK   [' + name + '] => page_name=' + str(d.get('name')))
    except Exception as e:
        print('ERR  [' + name + ']: ' + str(e))
