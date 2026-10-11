import bpy, collections
s=bpy.context.scene
print("SCENES",[x.name for x in bpy.data.scenes])
print("OBJECTS",len(bpy.data.objects))
types=collections.Counter(o.type for o in bpy.data.objects); print(types)
def walk(c,d=0):
    print("  "*d+"[C] "+c.name, len(c.objects))
    for ch in c.children: walk(ch,d+1)
walk(s.collection)
for o in bpy.data.objects:
    props={k:o[k] for k in o.keys() if not k.startswith('_')}
    v=len(o.data.vertices) if o.type=='MESH' else ''
    print(o.type, repr(o.name), 'parent=',o.parent.name if o.parent else None, 'verts=',v, 'mats=',[m.name for m in o.data.materials if m] if o.type=='MESH' else '', 'dims=',tuple(round(x,2) for x in o.dimensions), props or '')
print("MATERIALS",[m.name for m in bpy.data.materials])
print("IMAGES",[(i.name,i.size[:]) for i in bpy.data.images])
