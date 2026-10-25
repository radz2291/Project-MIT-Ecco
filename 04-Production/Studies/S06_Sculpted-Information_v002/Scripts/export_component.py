"""Export the retained unfolding objects as an appendable Blender collection."""
import bpy,json
from pathlib import Path
B=Path(__file__).resolve().parents[1]
bpy.ops.wm.open_mainfile(filepath=str(B/'Scenes/S06_cinematic-study_v002.blend'))
s=bpy.context.scene;s.frame_set(1)
c=bpy.data.collections.new('S06_UNFOLD_COMPONENT_v002')
names=[]
for ob in s.objects:
    if ob.name.startswith(('Recorded geometry','Registration','Seam','Measured section')):
        c.objects.link(ob);names.append(ob.name)
c['source']='S03 illustrative samples, unchanged from S06 v001'
c['use']='Append this collection. Frames 1-73 closed; 73-211 unfold; 211-288 flat. Native sample attributes retained.'
path=B/'Scenes/S06_unfolding-component_v002.blend'
bpy.data.libraries.write(str(path),{c},path_remap='RELATIVE',fake_user=True,compress=True)
with bpy.data.libraries.load(str(path),link=False) as (src,dst):
    assert 'S06_UNFOLD_COMPONENT_v002' in src.collections
    assert 'Recorded geometry | illustrative S03 source' in src.objects
(B/'Records/component.json').write_text(json.dumps({'path':path.name,'objects':names,'appendable_collection_verified':True},indent=2),encoding='utf-8')
print('COMPONENT EXPORTED',len(names))
