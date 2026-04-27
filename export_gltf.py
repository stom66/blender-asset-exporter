import bpy
import os
import json
from xml.etree.ElementTree import tostring

from . addon_log import Log
from . util import *


class EXPORT_OT_AssetExporter_ExportToGLTF(bpy.types.Operator):
	bl_idname  = "ae.export_gltf"
	bl_label   = "Export Collections to glTF"
	bl_options = {'REGISTER', 'UNDO'}
	bl_description = "Exports matching collections to glTF files"



	# ███████╗██╗  ██╗██████╗  ██████╗ ██████╗ ████████╗███████╗██████╗
	# ██╔════╝╚██╗██╔╝██╔══██╗██╔═══██╗██╔══██╗╚══██╔══╝██╔════╝██╔══██╗
	# █████╗   ╚███╔╝ ██████╔╝██║   ██║██████╔╝   ██║   █████╗  ██████╔╝
	# ██╔══╝   ██╔██╗ ██╔═══╝ ██║   ██║██╔══██╗   ██║   ██╔══╝  ██╔══██╗
	# ███████╗██╔╝ ██╗██║     ╚██████╔╝██║  ██║   ██║   ███████╗██║  ██║
	# ╚══════╝╚═╝  ╚═╝╚═╝      ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝
	#
	def export_collection_gltf(
		self,
		layer_col      : bpy.types.LayerCollection,
		export_settings: dict,
		ignore_transforms: bool
	) -> None:
		"""
		Export the specified collection to a GLTF file with the given export_settings.

		Args:
		- layer_col (bpy.types.LayerCollection): View layer entry for the collection to export.
		- export_settings (dict): The table containting all the export settings
		- ignore_transforms (bool): Should objects in the root of the collection will be moved back to 0,0,0 for the export 

		Returns:
		- None
		"""

		# Get settings
		settings		= bpy.context.scene.ae_settings
		collection	= layer_col.collection

		# Set the collection as the active collection
		bpy.context.view_layer.active_layer_collection	= layer_col

		# Deselect all the objects
		bpy.ops.object.select_all(action='DESELECT')

		# Temporarily reset transforms if needed
		orig_transforms	= {}
		if ignore_transforms:
			orig_transforms	= apply_identity_transforms(self, collection)

		# Remove the "Smooth by Angle" modifiers if enabled
		if settings.gltf_remove_modifier_smooth_by_angle:
			for obj in bpy.data.collections.get(collection.name).objects:
				disable_smooth_by_angle_modifier(obj)

		# Remove custom properties
		if settings.gltf_clean_custom_props:
			for obj in bpy.data.collections.get(collection.name).objects:
				if obj.type == 'MESH':
					clean_custom_properties(obj)

		# Export using the custom exporter
		bpy.ops.export_scene.gltf(**export_settings)

		# Restore original transforms if needed
		if ignore_transforms:
			restore_original_transforms(self, orig_transforms)

		
	def execute(self, context):

		# Get settings
		settings = bpy.context.scene.ae_settings

        # Get output path:
		path = get_export_path()

		# Get a dict of the collections to export with their name as the key
		collectionsToExport = FindCollectionsWithPrefix(settings.export_prefix)
		
 		# Check if there are any collections to export
		if len(collectionsToExport) < 1:
			Log("No collections found to export")
			self.report({'ERROR'}, "No collections found to export")
			settings.export_status = "No collections found to export"
			return {'CANCELLED'}	

		# Initialize export settings
		export_settings = {}

		# Read in export settings from selected preset
		if settings.gltf_preset != 'NONE':
			export_settings, preset_error = read_export_operator_preset(settings.gltf_preset, "gltf")
			if preset_error:
				self.report({'ERROR'}, preset_error)
				Log(f"read_export_operator_preset: {preset_error}")
				return {'CANCELLED'}

		else:
			self.report({'ERROR'}, "No export preset was selected")
			Log("No export preset was selected")
			return {'CANCELLED'}

		# Over-ride some export settings		
		export_settings["export_format"]                        = settings.gltf_export_format
		export_settings["export_draco_mesh_compression_enable"] = settings.gltf_use_draco		
		export_settings["use_active_collection"]                = True
		export_settings["use_active_collection_with_nested"]    = True
		export_settings["use_active_scene"]                     = False
		export_settings["use_mesh_edges"]                       = False
		export_settings["use_mesh_vertices"]                    = False
		export_settings["use_renderable"]                       = False
		export_settings["use_selection"]                        = False
		export_settings["use_visible"]                          = False

		# Ensure we're in the right mode
		ensure_object_mode()

		# Loop through all collections to export
		for name, layer_col in collectionsToExport.items():

			# Set the export file name to match the collection name (minus the MATCH_STRING)
			file_path	= str((path + '/' + name + '.gltf'))
			export_settings["filepath"]	= file_path

			# Run the export
			Log("Exporting as " + name + " to path: " + file_path)
			self.export_collection_gltf(layer_col, export_settings, settings.gltf_ignore_transform)

		self.report({'INFO'}, f"Exported {len(collectionsToExport)} collections")
		return {'FINISHED'}
