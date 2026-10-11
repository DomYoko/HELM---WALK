# Splits objects that hold several duplicates ("chairs 5", "table 2x") into one object per item.
# Loose mesh parts are grouped by position into N clusters, N taken from the name. Each cluster becomes
# one object named "<base> 1..N". The first keeps the original id, the rest get new ids from stamp_ids.py.
# blender -b --disable-autoexec in.blend --python scripts/split_merged.py -- out.blend   (omit out.blend for a dry run)
import bpy, sys, re
from mathutils import Vector
args = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
PAT = re.compile(r'^(.*?)\s*(\d+)\s*x?\s*$', re.I)

def desel():
    for x in bpy.context.view_layer.objects: x.select_set(False)

def bbox(o):
    pts = [o.matrix_world @ Vector(c) for c in o.bound_box]
    return Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts))), Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))

def clusters(parts, n):
    """Agglomerative: start with one group per loose part, keep merging the two closest (plan-view gap between boxes) until n remain."""
    groups = [[p] for p in parts]
    def box(g):
        bs = [bbox(p) for p in g]
        return (min(b[0].x for b in bs), min(b[0].y for b in bs), max(b[1].x for b in bs), max(b[1].y for b in bs))
    def gap(a, b):
        dx = max(a[0] - b[2], b[0] - a[2], 0); dy = max(a[1] - b[3], b[1] - a[3], 0)
        return (dx * dx + dy * dy) ** .5
    last = 0
    while len(groups) > n:
        bx = [box(g) for g in groups]
        d, i, j = min((gap(bx[i], bx[j]), i, j) for i in range(len(groups)) for j in range(i + 1, len(groups)))
        last = d; groups[i] += groups.pop(j)
    bx = [box(g) for g in groups]
    sep = min([gap(bx[i], bx[j]) for i in range(len(groups)) for j in range(i + 1, len(groups))] or [0])
    return groups, last, sep

# The designer may have saved the file in Edit Mode. Leave it first, or the mesh data read below is stale.
if bpy.context.mode != 'OBJECT': bpy.ops.object.mode_set(mode='OBJECT')
for o in [o for o in bpy.data.objects if o.type == 'MESH']:
    m = PAT.match(o.name.strip())
    if not m or int(m.group(2)) < 2: continue
    base, n = m.group(1).strip(), int(m.group(2))
    base = re.sub(r's$', '', base) if not base.endswith('ss') else base
    desel(); o.select_set(True); bpy.context.view_layer.objects.active = o
    bpy.ops.mesh.separate(type='LOOSE')
    parts = list(bpy.context.selected_objects)
    if len(parts) < n:
        print(f'SKIP {o.name!r}: {len(parts)} loose parts, name says {n}'); continue
    groups, last, sep = clusters(parts, n)
    print(f'SPLIT {o.name!r}: {len(parts)} loose parts -> {n} items, last merge gap {last:.3f} m, gap between items {sep:.3f} m')
    groups.sort(key=lambda g: (round(min(bbox(p)[0].x for p in g), 2), round(min(bbox(p)[0].y for p in g), 2)))
    for k, g in enumerate(groups):
        keep = o if o in g else g[0]
        desel()
        for p in g: p.select_set(True)
        bpy.context.view_layer.objects.active = keep
        if len(g) > 1: bpy.ops.object.join()
        g[:] = [keep]
    owner = next(g[0] for g in groups if g[0] == o) if any(g[0] == o for g in groups) else groups[0][0]
    for k, g in enumerate(groups):
        ob = g[0]; ob.name = f'{base} {k + 1}'
        if ob is not owner and 'id' in ob.keys(): del ob['id']
        desel(); ob.select_set(True); bpy.context.view_layer.objects.active = ob
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
if args:
    bpy.ops.wm.save_as_mainfile(filepath=args[0], copy=True); print('SAVED', args[0])
