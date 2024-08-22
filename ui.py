import bpy

from . export_gltf import *
from . export_fbx import *

# Main panel
class VIEW3D_PT_AssetExporter_UI_Main(bpy.types.Panel):
	bl_label       = 'Asset Exporter'
	bl_category    = 'Asset Exporter'
	bl_region_type = 'UI'
	bl_space_type  = 'VIEW_3D'

	def draw(self, context):
		layout = self.layout

		# String: Output path
		row = layout.row()
		row.label(text="Output path")
		row.prop(context.scene.ae_settings, "output_path", text="")

		# String: Collection prefix
		row = layout.row()
		row.label(text="Collection prefix")
		row.prop(context.scene.ae_settings, "export_prefix", text="")


# FBX Export
class VIEW3D_PT_AssetExporter_UI_FBX(bpy.types.Panel):
	bl_label       = 'FBX Export'
	bl_category    = 'Asset Exporter'
	bl_region_type = 'UI'
	bl_space_type  = 'VIEW_3D'
	bl_parent_id   = 'VIEW3D_PT_AssetExporter_UI_Main'

	def draw(self, context):
		layout = self.layout
        
		# Dropdown: FBX Presets
		row = layout.row()
		row.label(text="FBX Preset")
		row.prop(context.scene.ae_settings, "fbx_preset", text="")

		# Checkbox: FBX: split NLA tracks
		row = layout.row()
		col = row.column(align=False)
		col.label(text="FBX: split NLA tracks")
		col = row.column(align=True)
		col.prop(context.scene.ae_settings, "fbx_split_nla", text="")

		# Btn: Export FBX
		row = layout.row()
		row.operator(EXPORT_OT_AssetExporter_ExportToFBX.bl_idname, text="Export to FBX", icon="FILE_VOLUME")


# glTF Export
class VIEW3D_PT_AssetExporter_UI_GLTF(bpy.types.Panel):
	bl_label       = 'glTF Export'
	bl_category    = 'Asset Exporter'
	bl_region_type = 'UI'
	bl_space_type  = 'VIEW_3D'
	bl_parent_id   = 'VIEW3D_PT_AssetExporter_UI_Main'

	def draw(self, context):
		layout = self.layout

		# Dropdown: glTF Presets
		row = layout.row()
		row.label(text="glTF export preset")
		row.prop(context.scene.ae_settings, "gltf_preset", text="")


		# Checkbox: glTF: export format
		row = layout.row()
		col = row.column(align=False)
		col.label(text="Export format")
		col = row.column(align=True)
		col.prop(context.scene.ae_settings, "gltf_export_format", text="")
        
		# Checkbox: glTF: use Draco
		row = layout.row()
		col = row.column(align=False)
		col.label(text="Use Draco compression")
		col = row.column(align=True)
		col.prop(context.scene.ae_settings, "gltf_use_draco", text="")

		# Btn: Export GLTF
		row = layout.row()
		row.operator(EXPORT_OT_AssetExporter_ExportToGLTF.bl_idname, text="Export to glTF", icon="FILE_VOLUME")
