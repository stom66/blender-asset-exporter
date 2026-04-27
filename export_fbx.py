import bpy
import os
from xml.etree.ElementTree import tostring

from . addon_log import Log
from . util import *


class EXPORT_OT_AssetExporter_ExportToFBX(bpy.types.Operator):
	bl_idname  = "ae.export_fbx"
	bl_label   = "Export Collections to FBX"
	bl_options = {'REGISTER', 'UNDO'}
	bl_description = "Exports matching collections to FBX files"


	# ███████╗██╗  ██╗██████╗  ██████╗ ██████╗ ████████╗███████╗██████╗
	# ██╔════╝╚██╗██╔╝██╔══██╗██╔═══██╗██╔══██╗╚══██╔══╝██╔════╝██╔══██╗
	# █████╗   ╚███╔╝ ██████╔╝██║   ██║██████╔╝   ██║   █████╗  ██████╔╝
	# ██╔══╝   ██╔██╗ ██╔═══╝ ██║   ██║██╔══██╗   ██║   ██╔══╝  ██╔══██╗
	# ███████╗██╔╝ ██╗██║     ╚██████╔╝██║  ██║   ██║   ███████╗██║  ██║
	# ╚══════╝╚═╝  ╚═╝╚═╝      ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝
	#
	def export_collection_fbx(
		self,
		layer_col      : bpy.types.LayerCollection,
		export_settings: dict,
		ignore_transforms: bool
	) -> None:
		"""
		Export the specified collection to a FBX file with the given export_settings.

		Args:
		- layer_col (bpy.types.LayerCollection): View layer entry for the collection to export.
		- export_settings (dict): The table containting all the export settings

		Returns:
		- None
		"""

		# Get settings
		settings	= bpy.context.scene.ae_settings
		collection	= layer_col.collection

		# Set the collection as the active collection
		bpy.context.view_layer.active_layer_collection	= layer_col

		# Deselect all the objects
		bpy.ops.object.select_all(action='DESELECT')

		# Temporarily reset transforms if needed
		orig_transforms	= {}
		if ignore_transforms:
			orig_transforms	= apply_identity_transforms(self, collection)

		# Do the actual export, with big block of settings
		bpy.ops.export_scene.fbx(**export_settings)

		# Restore original transforms if needed
		if ignore_transforms:
			restore_original_transforms(self, orig_transforms)


	# ███╗   ██╗██╗      █████╗     ████████╗██████╗  █████╗  ██████╗██╗  ██╗███████╗
	# ████╗  ██║██║     ██╔══██╗    ╚══██╔══╝██╔══██╗██╔══██╗██╔════╝██║ ██╔╝██╔════╝
	# ██╔██╗ ██║██║     ███████║       ██║   ██████╔╝███████║██║     █████╔╝ ███████╗
	# ██║╚██╗██║██║     ██╔══██║       ██║   ██╔══██╗██╔══██║██║     ██╔═██╗ ╚════██║
	# ██║ ╚████║███████╗██║  ██║       ██║   ██║  ██║██║  ██║╚██████╗██║  ██╗███████║
	# ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝       ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝
	#                                                                                
	def export_single_nla_track_fbx(
		self,
		layer_col        : bpy.types.LayerCollection,
		armature         : bpy.types.Armature,
		nla_track        : bpy.types.NlaTrack,
		export_settings  : dict,
		ignore_transforms: bool
	):
		collection	= layer_col.collection

		# Deselect all objects
		bpy.ops.object.select_all(action='DESELECT')

		# Temporarily reset transforms if needed
		orig_transforms	= {}
		if ignore_transforms:
			orig_transforms	= apply_identity_transforms(self, collection)

		# Select the armature and its collection
		armature.select_set(True)
		bpy.context.view_layer.objects.active	= armature

		# Record the original states for the tracks
		orig_track_states	= {}

		# Disable all NLA tracks
		for key, track in armature.animation_data.nla_tracks.items():
			orig_track_states[key]	= track.mute
			track.mute	= True

		# Enable only the current NLA track
		nla_track.mute	= False

		# Set the collection as the active collection
		bpy.context.view_layer.active_layer_collection	= layer_col

		# Deselect all the objects
		bpy.ops.object.select_all(action='DESELECT')

		# Ensure we only export a single animation:
		export_settings["bake_anim_use_all_actions"] = False

		# Only export armatures
		# export_settings["object_types"]= {'ARMATURE'}

		# Do the actual export, with big block of settings
		bpy.ops.export_scene.fbx(**export_settings)

		# Re-enable all NLA tracks (optional, could leave them as-is)
		for key, track in armature.animation_data.nla_tracks.items():
			track.mute = orig_track_states[key]

		# Restore original transforms if needed
		if ignore_transforms:
			restore_original_transforms(self, orig_transforms)



	# ███╗   ███╗ █████╗ ██╗███╗   ██╗
	# ████╗ ████║██╔══██╗██║████╗  ██║
	# ██╔████╔██║███████║██║██╔██╗ ██║
	# ██║╚██╔╝██║██╔══██║██║██║╚██╗██║
	# ██║ ╚═╝ ██║██║  ██║██║██║ ╚████║
	# ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝
	#
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
			return {'CANCELLED'}	

		# Initialize export settings
		export_settings = {}
		
		# Read in export settings from selected preset
		if settings.fbx_preset != 'NONE':
			export_settings, preset_error = read_export_operator_preset(settings.fbx_preset, "fbx")
			if preset_error:
				self.report({'ERROR'}, preset_error)
				Log(f"read_export_operator_preset: {preset_error}")
				return {'CANCELLED'}

		else:
			self.report({'ERROR'}, "No export preset was selected")
			Log("No export preset was selected")
			return {'CANCELLED'}


		export_settings["use_selection"] = False
		export_settings["use_visible"]   = False
		export_settings["use_active_collection"] = True

		# Ensure we're in the right mode
		ensure_object_mode()

		# Export all the collections
		files = 0
		for name, layer_col in collectionsToExport.items():

			# Set the export file name to match the collection name (minus the MATCH_STRING)
			file_path	= str((path + '/' + name + '.fbx'))
			export_settings["filepath"]	= file_path

			# Run the export
			Log("Exporting as " + name + " to path: " + file_path)
			self.export_collection_fbx(layer_col, export_settings, settings.fbx_ignore_transform)
			files += 1

			# If we are splitting NLA tracks, eg exporting a single file per NLA track, then we need to loop through and check for amratures:
			if settings.fbx_split_nla:
				# Check for armatures with NLA tracks
				for obj in bpy.data.collections[layer_col.name].all_objects:
					if obj.type == 'ARMATURE' and obj.animation_data and obj.animation_data.nla_tracks:
						for track in obj.animation_data.nla_tracks:

							file_path	= str((path + '/' + name + '.' + track.name + '.fbx'))
							export_settings["filepath"]	= file_path

							Log(f"Exporting NLA Track: {track.name} for armature: {obj.name}")
							self.export_single_nla_track_fbx(
								layer_col,
								obj,
								track,
								export_settings,
								settings.fbx_ignore_transform
							)
							files += 1


			# Build the return info message
			info_msg = f"Exported {len(collectionsToExport)} collections"
			if settings.fbx_split_nla:
				info_msg = info_msg + f" to {files} files"

		self.report({'INFO'}, info_msg)

		return {'FINISHED'}
