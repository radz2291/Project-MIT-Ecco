"""Match playblast object visibility to render intent, preserving approved pixel guides.

Camera/material/effect animation remains native. No shared master is modified.
"""
import bpy
from contextlib import contextmanager

EXTRA_DISPLAY='Shared fine measurement display'

def render_allowed_objects(scene):
 allowed=set()
 def walk(collection,blocked=False):
  blocked=blocked or collection.hide_render
  if not blocked:allowed.update(o.name for o in collection.objects)
  for child in collection.children:walk(child,blocked)
 walk(scene.collection)
 return allowed

def excluded_objects(scene):
 allowed=render_allowed_objects(scene)
 return [o for o in scene.objects if o.hide_render or o.name not in allowed or (o.name==EXTRA_DISPLAY and not o.get('Final line-only style',False))]

def establish_final_visibility():
 """Persist per-view-layer hiding so viewport exports cannot draw render-only exclusions."""
 s=bpy.context.scene
 extra=bpy.data.objects.get(EXTRA_DISPLAY)
 if extra and not extra.get('Final line-only style',False):extra.hide_render=True
 names=[]
 for o in excluded_objects(s):
  if o.name in bpy.context.view_layer.objects:
   if o.visible_get():names.append(o.name)
   o.hide_set(True)
 return names

@contextmanager
def final_visibility():
 """Recheck animated render flags at the frame being exported."""
 previous=[]
 for o in excluded_objects(bpy.context.scene):
  if o.name in bpy.context.view_layer.objects:
   previous.append((o,o.hide_get()));o.hide_set(True)
 try:yield
 finally:
  for o,hidden in previous:o.hide_set(hidden)

def export(path,width=1920,height=1080):
 module=bpy.app.driver_namespace.get('ecco_pixel_module')
 if module is None:
  exec(bpy.data.texts['START HERE — pixel guides'].as_string())
  module=bpy.app.driver_namespace['ecco_pixel_module']
 handle=bpy.app.driver_namespace.pop(module.KEY,None)
 if handle:bpy.types.SpaceView3D.draw_handler_remove(handle,'WINDOW')
 with final_visibility():module.export(path,width,height)
