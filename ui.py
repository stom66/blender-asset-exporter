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
		row.label(text="FBX export preset")
		row.prop(context.scene.ae_settings, "fbx_preset", text="")

# FBX Export Settings
class VIEW3D_PT_AssetExporter_UI_FBX_Settings(bpy.types.Panel):
	bl_label       = 'Settings'
	bl_category    = 'Asset Exporter'
	bl_region_type = 'UI'
	bl_space_type  = 'VIEW_3D'
	bl_parent_id   = 'VIEW3D_PT_AssetExporter_UI_FBX'

	def draw(self, context):
		layout = self.layout
		settings = context.scene.ae_settings

		# Checkbox: FBX: split NLA tracks
		row = layout.row()
		col = row.column(align=False)
		col.label(text="Split NLA tracks")
		col = row.column(align=True) 
		col.prop(context.scene.ae_settings, "fbx_split_nla", text="")


# glTF Export Button
class VIEW3D_PT_AssetExporter_UI_FBX_Btn(bpy.types.Panel):
	bl_label       = 'FBX Export'
	bl_category    = 'Asset Exporter'
	bl_region_type = 'UI'
	bl_space_type  = 'VIEW_3D'
	bl_parent_id   = 'VIEW3D_PT_AssetExporter_UI_FBX'
	bl_options     = {'HIDE_HEADER', 'HEADER_LAYOUT_EXPAND'}

	def draw(self, context):
		layout = self.layout
		settings = context.scene.ae_settings

		# Btn: Export FBX
		row = layout.row()
		row.operator(EXPORT_OT_AssetExporter_ExportToFBX.bl_idname, text="Export collections to FBX", icon="FILE_VOLUME")



# glTF Export
class VIEW3D_PT_AssetExporter_UI_GLTF(bpy.types.Panel):
	bl_label       = 'glTF Export'
	bl_category    = 'Asset Exporter'
	bl_region_type = 'UI'
	bl_space_type  = 'VIEW_3D'
	bl_parent_id   = 'VIEW3D_PT_AssetExporter_UI_Main'

	def draw(self, context):
		layout = self.layout
		settings = context.scene.ae_settings

		# Dropdown: glTF Presets
		row = layout.row()
		row.label(text="glTF export preset")
		row.prop(settings, "gltf_preset", text="")

		# Checkbox: glTF: export format
		row = layout.row()
		col = row.column(align=False)
		col.label(text="Export format")
		col = row.column(align=True)
		col.prop(settings, "gltf_export_format", text="")


# glTF Export Settings
class VIEW3D_PT_AssetExporter_UI_GLTF_Settings(bpy.types.Panel):
	bl_label       = 'Settings'
	bl_category    = 'Asset Exporter'
	bl_region_type = 'UI'
	bl_space_type  = 'VIEW_3D'
	bl_parent_id   = 'VIEW3D_PT_AssetExporter_UI_GLTF'

	def draw(self, context):
		layout = self.layout
		settings = context.scene.ae_settings
		
		# Checkbox: glTF: use Draco
		row = layout.row()
		col = row.column(align=False)
		col.label(text="Use Draco compression")
		col = row.column(align=True)
		col.prop(settings, "gltf_use_draco", text="")
		
		# Checkbox: glTF: ignore root transforms
		row = layout.row()
		col = row.column(align=False)
		col.label(text="Ignore root transforms")
		col = row.column(align=True)
		col.prop(settings, "gltf_ignore_transform", text="")

		# Checkbox: glTF: remove "Smooth by Angle"
		row = layout.row()
		col = row.column(align=False)
		col.label(text="Remove \"Smooth by Angle\" modifiers")
		col = row.column(align=True)
		col.prop(settings, "gltf_remove_modifier_smooth_by_angle", text="")

		# Checkbox: glTF: clean custom props
		row = layout.row()
		col = row.column(align=False)
		col.label(text="Remove custom properties")
		col = row.column(align=True)
		col.prop(settings, "gltf_clean_custom_props", text="")

		


# glTF Export Button
class VIEW3D_PT_AssetExporter_UI_GLTF_Btn(bpy.types.Panel):
	bl_label       = 'glTF Export'
	bl_category    = 'Asset Exporter'
	bl_region_type = 'UI'
	bl_space_type  = 'VIEW_3D'
	bl_parent_id   = 'VIEW3D_PT_AssetExporter_UI_GLTF'
	bl_options     = {'HIDE_HEADER'}

	def draw(self, context):
		layout = self.layout
		settings = context.scene.ae_settings

		# Btn: Export GLTF
		row = layout.row()
		row.operator(EXPORT_OT_AssetExporter_ExportToGLTF.bl_idname, text="Export collections to glTF", icon="FILE_VOLUME")