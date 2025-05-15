bl_info = {
    "name": "My First Add-on",
    "blender": (4, 0, 2),
    "category": "Object",
}

import bpy

class SimpleOperator(bpy.types.Operator):
    bl_idname = "object.simple_operator"
    bl_label = "Simple Operator"

    def execute(self, context):
        self.report({'INFO'}, "Hello World")
        return {'FINISHED'}

def register():
    bpy.utils.register_class(SimpleOperator)

def unregister():
    bpy.utils.unregister_class(SimpleOperator)

if __name__ == "__main__":
    register()
