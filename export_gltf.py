import bpy
import os
import json
from xml.etree.ElementTree import tostring

from . collections import FindCollectionsWithPrefix
from . export_utils import GetExportPath
from . logging import Log


class EXPORT_OT_AssetExporter_ExportToGLTF(bpy.types.Operator):
	bl_idname  = "ae.export_gltf"
	bl_label   = "Export Collections to glTF"
	bl_options = {'REGISTER', 'UNDO'}



	# ███████╗██╗  ██╗██████╗  ██████╗ ██████╗ ████████╗███████╗██████╗
	# ██╔════╝╚██╗██╔╝██╔══██╗██╔═══██╗██╔══██╗╚══██╔══╝██╔════╝██╔══██╗
	# █████╗   ╚███╔╝ ██████╔╝██║   ██║██████╔╝   ██║   █████╗  ██████╔╝
	# ██╔══╝   ██╔██╗ ██╔═══╝ ██║   ██║██╔══██╗   ██║   ██╔══╝  ██╔══██╗
	# ███████╗██╔╝ ██╗██║     ╚██████╔╝██║  ██║   ██║   ███████╗██║  ██║
	# ╚══════╝╚═╝  ╚═╝╚═╝      ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝
	#
	def ExportCollectionToGLtf(
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

		# Set the collection as the active collection
		bpy.context.view_layer.active_layer_collection = bpy.context.view_layer.layer_collection.children[collection.name]

		# Deselect all the objects
		bpy.ops.object.select_all(action='DESELECT')

		# Save transforms
		orig_transforms = {}
		if ignore_transforms:
			for obj in bpy.data.collections.get(collection.name).objects:
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
		path = GetExportPath()

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
			preset_file_path = os.path.join(bpy.utils.preset_paths('operator/export_scene.gltf/')[0], settings.gltf_preset.replace(" ", "_") + ".py")
			if os.path.exists(preset_file_path):

				# Create a dummy containter class to hold the settings in
				class Container(object):
					__slots__ = ('__dict__',)

				op = Container()
				file = open(preset_file_path, 'r')

				# storing the values from the preset on the class
				for line in file.readlines()[3::]:
					exec(line, globals(), locals())

				# pass class dictionary to the operator				
				for key in op.__dict__:
					if key.startswith("export_") or key.startswith("use_"):
						export_settings[key] = op.__dict__[key]
				
				Log("Finished building export settings")

			else:
				Log(f"Preset file not found: {preset_file_path}")
				self.report({'ERROR'}, f"Preset file not found: {preset_file_path}")
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


		# Loop through all collections to export
		for name, col in collectionsToExport.items():
			
			# Set the export file name to match the collection name (minus the MATCH_STRING)
			file_path = str((path + '/' + name + '.gltf'))
			export_settings["filepath"] = file_path

			# Run the export
			Log("Exporting as " + name + " to path: " + file_path)
			self.ExportCollectionToGLtf(col, export_settings, settings.gltf_ignore_transform)

		self.report({'INFO'}, f"Exported {len(collectionsToExport)} collections")
		return {'FINISHED'}
