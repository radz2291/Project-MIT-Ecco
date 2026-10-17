import bpy,bmesh
h=bpy.data.objects['ECCO_HOUSING_SOURCE_MESH'];bm=bmesh.new();bm.from_mesh(h.data);print('SOURCE VOLUME',bm.calc_volume(signed=True),'boundary',sum(e.is_boundary for e in bm.edges),'nonmanifold',sum(not e.is_manifold for e in bm.edges));bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));print('RECALC VOLUME',bm.calc_volume(signed=True))
