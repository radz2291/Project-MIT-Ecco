import bpy,json,time
from pathlib import Path
R=Path(__file__).resolve().parents[5];T=R/'04-Production/Records/Tasks/T-054';records=[]
for name,frames in [('Digital_environment_demo_v005',[1]),('Measurement_reveal_demo_v002',[34,60])]:
 bpy.ops.wm.open_mainfile(filepath=str(T/'Demos'/f'{name}.blend'),load_ui=False);s=bpy.context.scene
 for f in frames:
  s.frame_set(f);s.render.filepath=str(T/'Previews'/f'{name}_f{f:03}.png');start=time.perf_counter();bpy.ops.render.render(write_still=True);elapsed=time.perf_counter()-start;records.append({'demo':name,'frame':f,'seconds':elapsed,'pass':elapsed<5,'settings':'640x360 Eevee4, no compositor/raytracing; full render-to-file'});(T/'Evidence/demo-render-timings.json').write_text(json.dumps(records,indent=2));assert elapsed<5,'Render limit failed; stop'
print('DEMO_STILLS_PASS')
