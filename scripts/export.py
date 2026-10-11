import bpy, sys
out=sys.argv[sys.argv.index('--')+1]
bpy.ops.export_scene.gltf(filepath=out, export_format='GLTF_SEPARATE', export_extras=True, export_apply=True, export_yup=True)
