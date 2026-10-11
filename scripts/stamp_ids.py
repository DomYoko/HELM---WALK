# Gives every object in the .blend a permanent hidden id (custom property "id") and saves a copy.
# Objects that already have an id keep it, so run this on every new delivery from the designer.
# blender -b --disable-autoexec in.blend --python scripts/stamp_ids.py -- out.blend
import bpy, sys, uuid
out = sys.argv[sys.argv.index('--') + 1]
used = {o['id'] for o in bpy.data.objects if 'id' in o.keys()}
new = 0
for o in bpy.data.objects:
    if 'id' not in o.keys():
        i = uuid.uuid4().hex[:10]
        while i in used: i = uuid.uuid4().hex[:10]
        o['id'] = i; used.add(i); new += 1
bpy.ops.wm.save_as_mainfile(filepath=out, copy=True)
print(f'STAMPED {new} new ids, {len(used)} total')
