"""Persistent export buffers for long sequences; same approved pixel-guide draw."""
import bpy,gpu,numpy as np
import final_render_visibility as display
class Exporter:
 def __init__(self,width,height):
  self.width=width;self.height=height
  if bpy.app.driver_namespace.get('ecco_pixel_module') is None:exec(bpy.data.texts['START HERE — pixel guides'].as_string())
  self.module=bpy.app.driver_namespace['ecco_pixel_module'];h=bpy.app.driver_namespace.pop(self.module.KEY,None)
  if h:bpy.types.SpaceView3D.draw_handler_remove(h,'WINDOW')
  self.off=gpu.types.GPUOffScreen(width,height)
  self.image=bpy.data.images.new('Full v026 reusable export buffer',width,height,alpha=True,float_buffer=True)
 def export(self,path):
  s=bpy.context.scene;bpy.context.view_layer.update();area=next(a for a in bpy.context.screen.areas if a.type=='VIEW_3D');region=next(r for r in area.regions if r.type=='WINDOW');space=area.spaces.active;old=space.overlay.show_overlays;space.overlay.show_overlays=False
  try:
   with display.final_visibility():
    dg=bpy.context.evaluated_depsgraph_get();cam=s.camera.evaluated_get(dg);view=cam.matrix_world.inverted();projection=cam.calc_matrix_camera(dg,x=self.width,y=self.height);prepared=self.module.batches()
    with bpy.context.temp_override(window=bpy.context.window,area=area,region=region):self.off.draw_view3d(s,bpy.context.view_layer,space,region,view,projection,do_color_management=False)
    with self.off.bind():
     gpu.matrix.push();gpu.matrix.push_projection()
     try:
      gpu.matrix.load_matrix(view);gpu.matrix.load_projection_matrix(projection);self.module.draw((self.width,self.height),prepared)
      pixels=np.asarray(gpu.state.active_framebuffer_get().read_color(0,0,self.width,self.height,4,0,'FLOAT')).copy().reshape(-1)
     finally:gpu.matrix.pop_projection();gpu.matrix.pop()
    self.image.pixels.foreach_set(pixels);self.image.save_render(str(path),scene=s)
  finally:space.overlay.show_overlays=old
 def close(self):
  self.off.free();bpy.data.images.remove(self.image)
