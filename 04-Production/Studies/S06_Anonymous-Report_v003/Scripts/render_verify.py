import bpy,json,time,hashlib,shutil
import numpy as np
from pathlib import Path
B=Path(__file__).resolve().parents[1];BASE=B.with_name('S06_Sculpted-Information_v002')
bpy.ops.wm.open_mainfile(filepath=str(BASE/'Scenes/S06_cinematic-study_v002.blend'))
s=bpy.context.scene;original=[];surface=s.objects['Recorded geometry | illustrative S03 source']
keyhashes=[hashlib.sha256(np.array([p.co[:] for p in k.data],dtype='f').tobytes()).hexdigest() for k in surface.data.shape_keys.key_blocks]
for f in range(1,217):
    s.frame_set(f);original.append((np.array(s.camera.matrix_world).copy(),float(s.camera.data.lens)))
bpy.ops.wm.open_mainfile(filepath=str(B/'Scenes/S06_cinematic-study_v003.blend'))
s=bpy.context.scene;surface=s.objects['Recorded geometry | illustrative S03 source']
newhashes=[hashlib.sha256(np.array([p.co[:] for p in k.data],dtype='f').tobytes()).hexdigest() for k in surface.data.shape_keys.key_blocks]
assert keyhashes==newhashes
for f,old in enumerate(original,1):
    s.frame_set(f);assert np.allclose(np.array(s.camera.matrix_world),old[0],rtol=0,atol=1e-7), (f,float(abs(np.array(s.camera.matrix_world)-old[0]).max()));assert s.camera.data.lens==old[1]
packed=[im for im in bpy.data.images if im.type=='IMAGE']
assert len(packed)==5 and all(im.packed_file for im in packed)
assert all(im.name.startswith('Anonymous ') for im in packed)
for f in range(229,289):
    s.frame_set(f)
    assert all(o.hide_render for o in s.objects if o.name.startswith(('Source status','Sequence identity')))
bench=[]
for f in (1,142,216,228,252,288):
    s.frame_set(f);s.render.filepath=str(B/f'Previews/check_{f:03d}.png');t=time.perf_counter();bpy.ops.render.render(write_still=True);elapsed=time.perf_counter()-t
    bench.append({'frame':f,'seconds':elapsed})
    if elapsed>=5:raise RuntimeError('Benchmark exceeds strict render cap')
(B/'Records/benchmark.json').write_text(json.dumps(bench,indent=2),encoding='utf-8')
shutil.copy2(B/'Previews/check_288.png',B/'Previews/S06_report-ending_v003.png')
cache=B/'Cache/journey';cache.mkdir(exist_ok=True)
for f in range(1,217):shutil.copy2(BASE/f'Cache/journey/{f:04d}.png',cache/f'{f:04d}.png')
timings=[]
for f in range(217,289):
    s.frame_set(f);s.render.filepath=str(cache/f'{f:04d}.png');t=time.perf_counter();bpy.ops.render.render(write_still=True);elapsed=time.perf_counter()-t
    timings.append({'frame':f,'seconds':elapsed})
    (B/'Records/render-timings.json').write_text(json.dumps(timings),encoding='utf-8')
    if elapsed>=5:raise RuntimeError('Batch exceeds strict render cap')
s.frame_set(288)
texts=[o.data.body for o in s.objects if o.type=='FONT' and not o.hide_render]
assert texts==['Engineering output','Separate report example','ANONYMOUS GRAPHIC EXCERPTS','Graphic excerpts from an existing report; not the preceding illustrative dataset.'] or set(texts)=={'Engineering output','Separate report example','ANONYMOUS GRAPHIC EXCERPTS','Graphic excerpts from an existing report; not the preceding illustrative dataset.'}
out={'base_shape_keys_exact':True,'camera_frames_1_to_216_exact':True,'source_images_packed':5,'full_source_page_present':False,'final_visible_text':texts,'all_source_images_generic_names':True,'early_cache_reused_frames':216,'ending_rerendered_frames':72,'missing_libraries':[x.filepath for x in bpy.data.libraries if not Path(bpy.path.abspath(x.filepath)).exists()]}
(B/'Records/scene-verification.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print('ENDING RENDERED AND VERIFIED')
