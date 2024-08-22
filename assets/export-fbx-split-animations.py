import bpy
import os
from xml.etree.ElementTree import tostring

# WhatDo:
#
# This is a backup of the original script
# 
# It is setup to export all of the _export collections to the folder decalred below
#
# How it works:
# 	Loops through the current collection structure
#		If a collection contains the string '_export.'
#			Export all objects within it as a FBX
#
#
# How to use:
# 	Move all items that are to be exported together into a collection
# 	Name the collection, including the MATCH_STRING below, eg: `_export.floor.01`
# 	(Optionally) Go to Window -> Toggle System Console
# 	Click the play button to run the script
# 	Wait while it runs (approx 10s per object)

# Define the string to search for in collection names
MATCH_STRING = '_export.'

# Define the output path here:
# Note that blender uses "//" for relative paths
# Should NOT have a trailing slash, eg: `//../GLTF`
# Relative paths start from the blend file directory not the location of the script
OUTPUT_PATH = "//../fbx"

# Set the name of the log file
# This will create a text window with this name to get some output without having to open the
# system console
LOG_PATH = "output.log"

#
# --------------------------------------------------------------------------------------------
#



class ExportToFbxNLAOperator(bpy.types.Operator):
	"""Export _export collections to FBX"""  # Tooltip for the operator
	bl_idname  = "export_scene.export_to_fbx_nla"  # Unique identifier for the operator
	bl_label   = "Export to FBX - Split NLAs"  # Label in the UI
	bl_options = {'REGISTER', 'UNDO'}  # Options for the operator

	def log(self, message):
		print(message)
		self.LOG_TXT.write(message + '\n')

		
	def doExport(self, name, path):
		# Get absolute path:

		# Deselect all the objects
		bpy.ops.object.select_all(action='DESELECT')

		#Count all objects in the currently selected _export collection
		count = 0

		for obj in bpy.data.collections[name].all_objects:
			count+=1

		self.log(name + " contains " + str(count) + " objects") 

		# Do the actual export, with big block of settings
		bpy.ops.export_scene.fbx(
			filepath                        = path,  
			#collection                      = name,           # Source Collection, Export only objects from this collection (and its children)
			use_active_collection           = True,  		# Active Collection, Export only objects from the active collection
			use_selection                   = False,  		# Selected Objects, Export selected and visible objects only
			use_visible                     = False,  		# Visible Objects, Export visible objects only
			object_types                    = {'ARMATURE', 'EMPTY', 'MESH'},  # Types of objects to export: 'ARMATURE', 'CAMERA', 'EMPTY', 'LIGHT', 'MESH', 'OTHER'

			add_leaf_bones                  = False,            # Add Leaf Bones, Append a final bone to the end of each chain
			apply_scale_options             = 'FBX_SCALE_NONE',	# Apply Scalings, 'FBX_SCALE_NONE', 'FBX_SCALE_UNITS', 'FBX_SCALE_CUSTOM', 'FBX_SCALE_ALL'
			apply_unit_scale                = True,            	# Apply Unit, Take into account current Blender units settings
			armature_nodetype               = 'NULL',          	# Armature FBXNode Type, FBX type of node used for Blender’s armatures
			axis_forward                    = '-Z',            	# Forward, Forward axis for the FBX file
			axis_up                         = 'Y',             	# Up, Up axis for the FBX file
			bake_anim                       = True,            	# Baked Animation, Export baked keyframe animation
			bake_anim_force_startend_keying = True,            	# Force Start/End Keying, Always add a keyframe at start and end of actions
			bake_anim_simplify_factor       = 1.0,             	# Simplify, How much to simplify baked values
			bake_anim_step                  = 1.0,             	# Sampling Rate, How often to evaluate animated values (in frames)
			bake_anim_use_all_actions       = False,            # All Actions, Export each action as a separated FBX’s AnimStack
			bake_anim_use_all_bones         = False,            # Key All Bones, Force exporting at least one key for all bones
			bake_anim_use_nla_strips        = False,            # NLA Strips, Export each non-muted NLA strip as a separate FBX’s AnimStack
			bake_space_transform            = True,           	# Apply Transform, Bake space transform into object data
			batch_mode                      = 'OFF',           	# Batch Mode, Export multiple objects to separate files
			check_existing                  = True,            	# Check Existing, Check and warn on overwriting existing files
			colors_type                     = 'SRGB',          	# Vertex Colors, Export vertex color attributes in sRGB color space
			embed_textures                  = False,           	# Embed Textures, Embed textures in FBX binary file
			global_scale                    = 1.0,             	# Scale, Scale all data (Some importers do not support scaled armatures)
			mesh_smooth_type                = 'OFF',           	# Smoothing, Export smoothing information (Normals Only)
			path_mode                       = 'AUTO',  		    # Path Mode, Method used to reference paths
			primary_bone_axis               = 'Y',  		    # Primary Bone Axis, Main axis for bone direction
			prioritize_active_color         = False,  		    # Prioritize Active Color, Ensure the active color is exported first
			secondary_bone_axis             = 'X',  		    # Secondary Bone Axis, Secondary axis for bone direction
			use_armature_deform_only        = False,  		    # Only Deform Bones, Only export bones used for deformation
			use_batch_own_dir               = True,  		    # Batch Own Dir, Create a directory for each exported file
			use_custom_props                = False,  		    # Custom Properties, Export custom properties
			use_mesh_edges                  = False,  		    # Loose Edges, Export loose edges as two-vertices polygons
			use_mesh_modifiers              = True,  		    # Apply Modifiers, Apply modifiers to mesh objects (except Armature ones)
			use_mesh_modifiers_render       = True,  		    # Use Modifiers Render Setting, Use render settings when applying modifiers
			use_metadata                    = True,  		    # Use Metadata, Include metadata in the exported file
			use_space_transform             = True,  		    # Use Space Transform, Apply global space transform to object rotations
			use_subsurf                     = False,  		    # Export Subdivision Surface, Export the last Catmull-Rom subdivision modifier as FBX subdivision
			use_triangles                   = True,  		    # Triangulate Faces, Convert all faces to triangles
			use_tspace                      = False,  		    # Tangent Space, Add binormal and tangent vectors for tangent space
		)

		self.log("Finished attempting to export: " + name)
		self.log("------------------------------------------------")


	def export_with_nla_track(self, col_name, armature, nla_track, path):
		# Deselect all objects
		bpy.ops.object.select_all(action='DESELECT')

		# Select the armature and its collection
		armature.select_set(True)
		bpy.context.view_layer.objects.active = armature

		# Disable all NLA tracks
		for track in armature.animation_data.nla_tracks:
			track.mute = True

		# Enable only the current NLA track
		nla_track.mute = False

		# Export
		self.doExport(col_name, path)

		# Re-enable all NLA tracks (optional, could leave them as-is)
		for track in armature.animation_data.nla_tracks:
			track.mute = False


	def checkCollection(self, col, path):

		# Check if the colelction name contains the MATCH_STRING
		if col.name.count(MATCH_STRING) and not col.exclude:

			# Log success: found a collection to export and flip found flag
			self.log("Found collection to export: " + col.name)

			# Set the export file name to match the collection name (minus the MATCH_STRING)
			file_name = col.name.replace(MATCH_STRING, '')
			file_path = str((path + '/' + file_name + '.fbx'))

			# Set the collection as the active collection
			bpy.context.view_layer.active_layer_collection = col

			# Run the export

			# Check for armatures with NLA tracks
			for obj in bpy.data.collections[col.name].all_objects:
				if obj.type == 'ARMATURE' and obj.animation_data and obj.animation_data.nla_tracks:
					for track in obj.animation_data.nla_tracks:
						
						file_path = str((path + '/' + file_name + '.' + track.name + '.fbx'))

						self.log(f"Exporting NLA Track: {track.name} for armature: {obj.name}")
						self.export_with_nla_track(col.name, obj, track, file_path)
					return True

			# If no armature with NLA, just export normally
			self.log("Exporting as " + file_name + " to path: " + file_path)
			self.doExport(col.name, file_path)
			
			# Return true to let the parent know a valid collection was found
			return True
		else:
			return False


	def execute(self, context):
				
		# ██╗      ██████╗  ██████╗  ██████╗ ██╗███╗   ██╗ ██████╗
		# ██║     ██╔═══██╗██╔════╝ ██╔════╝ ██║████╗  ██║██╔════╝
		# ██║     ██║   ██║██║  ███╗██║  ███╗██║██╔██╗ ██║██║  ███╗
		# ██║     ██║   ██║██║   ██║██║   ██║██║██║╚██╗██║██║   ██║
		# ███████╗╚██████╔╝╚██████╔╝╚██████╔╝██║██║ ╚████║╚██████╔╝
		# ╚══════╝ ╚═════╝  ╚═════╝  ╚═════╝ ╚═╝╚═╝  ╚═══╝ ╚═════╝
		#

		if LOG_PATH not in bpy.data.texts:
			self.LOG_TXT = bpy.data.texts.new(LOG_PATH)
		else:
			self.LOG_TXT = bpy.data.texts[LOG_PATH]
			self.LOG_TXT.clear()

		
		# ██████╗  █████╗ ████████╗██╗  ██╗
		# ██╔══██╗██╔══██╗╚══██╔══╝██║  ██║
		# ██████╔╝███████║   ██║   ███████║
		# ██╔═══╝ ██╔══██║   ██║   ██╔══██║
		# ██║     ██║  ██║   ██║   ██║  ██║
		# ╚═╝     ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝
		#                                  
		path = bpy.path.abspath(OUTPUT_PATH)

		if not os.path.exists(path):
			self.log("--------------------------------------------")
			self.log("ERROR: " + path)
			self.log("ERROR: the path above does not exist")
			self.log("--------------------------------------------")
			return {'CANCELLED'}
		
		self.log("Export path is determined as: " + path)


		# Check that the "_export" collection exists
		exportCollectionExists = False

		# Loop through all collections in the current view layer
		for col in bpy.context.view_layer.layer_collection.children:
			
			# Check the current collection to see if it should be exported
			if self.checkCollection(col, path):
				exportCollectionExists = True
			
			# Also Check the children of the collection to see if any of them need exporting
			for child_col in col.children:
				if self.checkCollection(child_col, path):
					exportCollectionExists = True
					

		# Throw an error if there's no export collection
		if not exportCollectionExists:
			self.log("--------------------------------------------")
			self.log("ERROR: a collection with '_export.' in the name could not be found. Nothing to do...")
			self.log("--------------------------------------------")
			return {'CANCELLED'}
		
		return {'FINISHED'}


		


		# ███████╗██╗  ██╗██████╗  ██████╗ ██████╗ ████████╗███████╗██████╗
		# ██╔════╝╚██╗██╔╝██╔══██╗██╔═══██╗██╔══██╗╚══██╔══╝██╔════╝██╔══██╗
		# █████╗   ╚███╔╝ ██████╔╝██║   ██║██████╔╝   ██║   █████╗  ██████╔╝
		# ██╔══╝   ██╔██╗ ██╔═══╝ ██║   ██║██╔══██╗   ██║   ██╔══╝  ██╔══██╗
		# ███████╗██╔╝ ██╗██║     ╚██████╔╝██║  ██║   ██║   ███████╗██║  ██║
		# ╚══════╝╚═╝  ╚═╝╚═╝      ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝
		#




def register():
	bpy.utils.register_class(ExportToFbxNLAOperator)

def unregister():
	bpy.utils.unregister_class(ExportToFbxNLAOperator)

if __name__ == "__main__":
	register()
