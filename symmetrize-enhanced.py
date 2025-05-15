bl_info = {
    "name": "Symmetrize Enhanced",
    "blender": (4, 0, 2),
    "category": "Object",
}

import bpy

class SimpleOperator(bpy.types.Operator):
    bl_idname = "object.symmetrize_enhanced"
    bl_label = "Symmetrize Enhanced"

    def execute(self, context):
        self.report({'INFO'}, "Hello World")
        return {'FINISHED'}

def register():
    bpy.utils.register_class(SimpleOperator)

def unregister():
    bpy.utils.unregister_class(SimpleOperator)

if __name__ == "__main__":
    register()
