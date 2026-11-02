"""Local final-display style: retain surface lines/fill but remove the point-marker branch."""
import bpy
def configure():
 ob=bpy.data.objects['Shared fine measurement display']
 wrapper=ob.modifiers[0].node_group.copy();ob.modifiers[0].node_group=wrapper
 node=next(n for n in wrapper.nodes if n.type=='GROUP');style=node.node_tree.copy();style.name='Final surface lines and fill — no point markers';node.node_tree=style
 def is_points(node,seen=None):
  seen=set() if seen is None else seen
  if node in seen:return False
  seen.add(node)
  if node.type=='INSTANCE_ON_POINTS':return True
  return any(is_points(link.from_node,seen) for socket in node.inputs for link in socket.links)
 removed=0
 for join in [n for n in style.nodes if n.type=='JOIN_GEOMETRY']:
  for link in list(join.inputs['Geometry'].links):
   if is_points(link.from_node):style.links.remove(link);removed+=1
 assert removed==1,removed
 ob['Final line-only style']=True;ob.hide_render=False;ob.hide_set(False)
 return removed
