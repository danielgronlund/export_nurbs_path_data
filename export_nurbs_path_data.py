bl_info = {
    "name": "Export NURBS Path Data",
    "blender": (2, 80, 0),
    "category": "Import-Export",
    "description": "Export NURBS path data to a JSON file",
    "author": "Your Name",
    "version": (1, 0),
    "location": "File > Export > Export NURBS Path Data (.json)"
}

import bpy
import json
from bpy_extras.io_utils import ExportHelper
from bpy.types import Operator
from bpy.props import StringProperty

class ExportNURBSPathData(Operator, ExportHelper):
    """Export NURBS Path Data"""
    bl_idname = "export_scene.nurbs_path_data"
    bl_label = "Export NURBS Path Data"
    bl_options = {'PRESET'}

    filename_ext = ".json"
    filter_glob: StringProperty(
        default="*.json",
        options={'HIDDEN'},
    )

    def execute(self, context):
        export_nurbs_path_data(self.filepath)
        return {'FINISHED'}

def export_nurbs_path_data(filepath):
    data = []
    for obj in bpy.context.scene.objects:
        if obj.type == 'CURVE' and obj.data.dimensions == '3D':
            if obj.data.splines[0].type == 'NURBS':
                spline = obj.data.splines[0]
                path_data = {
                    "name": obj.name,
                    "type": spline.type,
                    "degree": spline.order_u - 1,
                    "control_points": [point.co[:] for point in spline.points],
                    "knot_vector": [point.co[0] for point in spline.points]
                }
                data.append(path_data)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)

def menu_func_export(self, context):
    self.layout.operator(ExportNURBSPathData.bl_idname, text="Export NURBS Path Data (.json)")

def register():
    bpy.utils.register_class(ExportNURBSPathData)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)

def unregister():
    bpy.utils.unregister_class(ExportNURBSPathData)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)

if __name__ == "__main__":
    register()
