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

    def execute(self, context):
        bpy.ops.mesh.symmetrize()
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
