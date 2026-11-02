"""Underground proof only; restore distant objects even on cap failure. No scene save."""
import bpy
from pathlib import Path
Q=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco/04-Production/Shots/S01-S02')
names=['Shared continuous World','Shared offshore equipment','Shared ocean'];old={n:bpy.data.objects[n].hide_render for n in names};src=bpy.data.objects[names[0]]
with bpy.data.libraries.load(bpy.path.abspath(src.instance_collection.library.filepath),link=True) as (a,b):b.collections=['WORLD_S02_PHYSICAL_CUTAWAY']
ob=bpy.data.objects.new('PREVIEW local wall only',None);bpy.context.scene.collection.objects.link(ob);ob.instance_type='COLLECTION';ob.instance_collection=b.collections[0];ob.matrix_world=src.matrix_world
try:
 for n in names:bpy.data.objects[n].hide_render=True
 proof_width=480;proof_height=270;proof_aa='OFF'
 for proof_frames,proof_record in [(list(range(299,327)),'motion_cycle1_v002.json'),(list(range(440,465)),'motion_history_v002.json')]:
  exec(compile((Q/'Scripts/preview_v002.py').read_text(encoding='utf8'),'preview_v002.py','exec'))
finally:
 for n,v in old.items():bpy.data.objects[n].hide_render=v
 bpy.data.objects.remove(ob,do_unlink=True)
