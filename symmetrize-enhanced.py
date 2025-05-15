bl_info = {
    "name": "Symmetrize Enhanced",
    "blender": (4, 0, 2),
    "category": "Mesh",
}

import bpy
from bpy.types import Operator
from bpy.utils import register_class, unregister_class

class MESH_OT_symmetrize_enhanced(Operator):
    bl_idname = "mesh.symmetrize_enhanced"
    bl_label = "Symmetrize Enhanced"
    bl_options = {'REGISTER', 'UNDO'}

    mirror_origin_point: bpy.props.EnumProperty(
    name="Mirror Origin",
    items=[
        ('OBJECT_ORIGIN', "Object Origin", ""),
        ('CURSOR', "3D Cursor", ""),
        ('ACTIVE_ELEMENT', "Active Element", "")
    ],
    default='OBJECT_ORIGIN',
    description="Point to mirror around"
    ) # type: ignore

    
    mirror_direction: bpy.props.EnumProperty(
    name="Mirror Direction",
    items=[
        ('NEGATIVE_X', "-X to +X", ""),
        ('POSITIVE_X', "+X to -X", ""),
        ('NEGATIVE_Y', "-Y to +Y", ""),
        ('POSITIVE_Y', "+Y to -Y", ""),
        ('NEGATIVE_Z', "-Z to +Z", ""),
        ('POSITIVE_Z', "+Z to -Z", ""),
    ],
    default='NEGATIVE_X',
    description="Direction to mirror"
    ) # type: ignore

    def execute(self, context):
        obj = context.object
        cursor_loc = context.scene.cursor.location.copy()

        origin = None

        if self.mirror_origin_point == 'CURSOR':
            origin = context.scene.cursor.location.copy()
        elif self.mirror_origin_point == 'ACTIVE_ELEMENT':
            import bmesh
            bpy.ops.object.mode_set(mode='EDIT')
            bm = bmesh.from_edit_mesh(context.object.data)
            bm.verts.ensure_lookup_table()
            bm.edges.ensure_lookup_table()
            bm.faces.ensure_lookup_table()

            active = bm.select_history.active
            if not active:
                self.report({'ERROR'}, "No active element")
                return {'CANCELLED'}

            if isinstance(active, bmesh.types.BMVert):
                origin = active.co.copy()
            elif isinstance(active, bmesh.types.BMEdge):
                origin = (active.verts[0].co + active.verts[1].co) / 2
            elif isinstance(active, bmesh.types.BMFace):
                origin = active.calc_center_median().copy()
            else:
                self.report({'ERROR'}, "Unsupported active element")
                return {'CANCELLED'}
            bpy.ops.object.mode_set(mode='OBJECT')

        if origin:
            for vert in context.object.data.vertices:
                vert.co -= origin
            bpy.ops.object.mode_set(mode='EDIT')

        bpy.ops.mesh.symmetrize(direction=self.mirror_direction)

        if origin:
            bpy.ops.object.mode_set(mode='OBJECT')
            for vert in context.object.data.vertices:
                vert.co += origin
            bpy.ops.object.mode_set(mode='EDIT')

        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(MESH_OT_symmetrize_enhanced.bl_idname)

def register():
    register_class(MESH_OT_symmetrize_enhanced)
    bpy.types.VIEW3D_MT_edit_mesh.append(menu_func)

def unregister():
    unregister_class(MESH_OT_symmetrize_enhanced)
    bpy.types.VIEW3D_MT_edit_mesh.remove(menu_func)

if __name__ == "__main__":
    register()
