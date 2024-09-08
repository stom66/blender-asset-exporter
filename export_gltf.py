import bpy
import os
import json
from xml.etree.ElementTree import tostring

from . collections import FindCollectionsWithPrefix
from . logging import Log
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
		collection     : bpy.types.Collection, 
		export_settings: dict,
		ignore_transforms: bool
	) -> None:
		"""
		Export the specified collection to a GLTF file with the given export_settings.

		Args:
		- collection (bpy.types.Collection): The Blender collection containing objects to export.
		- export_settings (dict): The table containting all the export settings
		- ignore_transforms (bool): Should objects in the root of the collection will be moved back to 0,0,0 for the export 

		Returns:
		- None
		"""

		# Get settings
		settings = bpy.context.scene.ae_settings

		# Set the collection as the active collection
		bpy.context.view_layer.active_layer_collection = bpy.context.view_layer.layer_collection.children[collection.name]

		# Deselect all the objects
		bpy.ops.object.select_all(action='DESELECT')

		collection = bpy.data.collections.get(collection.name)
		all_objects = get_all_objects_in_collection(collection)

		# Save transforms
		orig_transforms = {}
		if ignore_transforms:
			for obj in all_objects:
				if obj.parent is None:
					print("Ignoring transform for ", obj.name)

					orig_transforms[obj] = {
						'location'      : obj.location.copy(),
						'rotation_euler': obj.rotation_euler.copy(),
						'scale'         : obj.scale.copy()
					}
					
					obj.location       = (0, 0, 0)
					obj.rotation_euler = (0, 0, 0)
					obj.scale          = (1, 1, 1)

		# Remove the "Smooth by Angle" modifiers if enabled
		if settings.gltf_remove_modifier_smooth_by_angle:
			for obj in all_objects:
				disable_smooth_by_angle_modifier(obj)

		# Remove custom properties
		if settings.gltf_hardops_bug_workaround:
			for obj in bpy.data.objects:
				clean_hardops_properties(obj)

		# Export using the custom exporter
		bpy.ops.export_scene.gltf(**export_settings)

		# Restore transformations
		if ignore_transforms:			
			for obj, transform in orig_transforms.items():
				obj.location       = transform['location']
				obj.rotation_euler = transform['rotation_euler']
				obj.scale          = transform['scale']

		
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
		if settings.fbx_preset != 'NONE':
			export_settings = read_export_operator_preset(settings.gltf_preset, "gltf")
			if not export_settings:
				self.report({'ERROR'}, f"Preset file not found: {settings.gltf_preset}")
				Log(f"Preset file not found: {settings.gltf_preset}")
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
		for name, col in collectionsToExport.items():
			
			# Set the export file name to match the collection name (minus the MATCH_STRING)
			file_path = str((path + '/' + name + '.gltf'))
			export_settings["filepath"] = file_path

			# Run the export
			Log("Exporting as " + name + " to path: " + file_path)
			self.export_collection_gltf(col, export_settings, settings.gltf_ignore_transform)

		self.report({'INFO'}, f"Exported {len(collectionsToExport)} collections")
		return {'FINISHED'}
