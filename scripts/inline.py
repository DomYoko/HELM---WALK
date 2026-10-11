import json, base64, sys, os
src, out = sys.argv[1], sys.argv[2]
g = json.load(open(src))
for b in g['buffers']:
    b['uri'] = 'data:application/octet-stream;base64,' + base64.b64encode(open(os.path.join(os.path.dirname(src), b['uri']), 'rb').read()).decode()
json.dump(g, open(out, 'w'))
