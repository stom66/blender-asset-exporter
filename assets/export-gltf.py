# WhatDo:
#
# This is a backup of the original script

# This script is setup to export all of the _export collections to the folder decalred below
#
# How it works:
# 	Loops through the current collection structure
#		If a collection contains the string '_export.'
#			Export all objects within it as a glTF
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
OUTPUT_PATH = "//../GLTF"

# Set the name of the log file
# This will create a text window with this name to get some output without having to open the
# system console
LOG_PATH = "output.log"

#
# --------------------------------------------------------------------------------------------
#

import bpy
import os
from xml.etree.ElementTree import tostring

# ██╗      ██████╗  ██████╗  ██████╗ ██╗███╗   ██╗ ██████╗
# ██║     ██╔═══██╗██╔════╝ ██╔════╝ ██║████╗  ██║██╔════╝
# ██║     ██║   ██║██║  ███╗██║  ███╗██║██╔██╗ ██║██║  ███╗
# ██║     ██║   ██║██║   ██║██║   ██║██║██║╚██╗██║██║   ██║
# ███████╗╚██████╔╝╚██████╔╝╚██████╔╝██║██║ ╚████║╚██████╔╝
# ╚══════╝ ╚═════╝  ╚═════╝  ╚═════╝ ╚═╝╚═╝  ╚═══╝ ╚═════╝
#

if LOG_PATH not in bpy.data.texts:
    LOG_TXT = bpy.data.texts.new(LOG_PATH)
else:
    LOG_TXT = bpy.data.texts[LOG_PATH]
    LOG_TXT.clear()

def log(message):
    print(message)
    LOG_TXT.write(message + '\n')



# ███████╗██╗  ██╗██████╗  ██████╗ ██████╗ ████████╗    ██╗      ██████╗  ██████╗ ██████╗
# ██╔════╝╚██╗██╔╝██╔══██╗██╔═══██╗██╔══██╗╚══██╔══╝    ██║     ██╔═══██╗██╔═══██╗██╔══██╗
# █████╗   ╚███╔╝ ██████╔╝██║   ██║██████╔╝   ██║       ██║     ██║   ██║██║   ██║██████╔╝
# ██╔══╝   ██╔██╗ ██╔═══╝ ██║   ██║██╔══██╗   ██║       ██║     ██║   ██║██║   ██║██╔═══╝
# ███████╗██╔╝ ██╗██║     ╚██████╔╝██║  ██║   ██║       ███████╗╚██████╔╝╚██████╔╝██║
# ╚══════╝╚═╝  ╚═╝╚═╝      ╚═════╝ ╚═╝  ╚═╝   ╚═╝       ╚══════╝ ╚═════╝  ╚═════╝ ╚═╝
#
# Now onto the main functions
def export2gltf(path):

    # Check that the "_export" collection exists
    exportCollectionExists = False

    # Loop through all collections in the current view layer
    for col in bpy.context.view_layer.layer_collection.children:
        
        # Check the current collection to see if it should be exported
        if checkCollection(col):
            exportCollectionExists = True
        
        # Check the children of the collection to see if any of them need exporting
        for child_col in col.children:
            if checkCollection(child_col):
                exportCollectionExists = True
                

    # Throw an error if there's no export collection
    if not exportCollectionExists:
        log("--------------------------------------------")
        log("ERROR: a collection with '_export.' in the name could not be found. Nothing to do...")
        log("--------------------------------------------")


def checkCollection(col):

    # Check if the colelction name contains the MATCH_STRING
    if col.name.count(MATCH_STRING) and not col.exclude:

        # Log success: found a collection to export and flip found flag
        log("Found collection to export: " + col.name)

        # Set the export file name to match the collection name (minus the MATCH_STRING)
        file_name = col.name.replace(MATCH_STRING, '')
        file_path = str((path + '/' + file_name + '.gltf'))

        # Set the collection as the active collection
        bpy.context.view_layer.active_layer_collection = col

        # Run the export
        log("Exporting as " + file_name + " to path: " + file_path)
        doExport(col.name, file_path)
        
        # Return true to let the parent know a valid collection was found
        return True
    else:
        return False


# ███████╗██╗  ██╗██████╗  ██████╗ ██████╗ ████████╗███████╗██████╗
# ██╔════╝╚██╗██╔╝██╔══██╗██╔═══██╗██╔══██╗╚══██╔══╝██╔════╝██╔══██╗
# █████╗   ╚███╔╝ ██████╔╝██║   ██║██████╔╝   ██║   █████╗  ██████╔╝
# ██╔══╝   ██╔██╗ ██╔═══╝ ██║   ██║██╔══██╗   ██║   ██╔══╝  ██╔══██╗
# ███████╗██╔╝ ██╗██║     ╚██████╔╝██║  ██║   ██║   ███████╗██║  ██║
# ╚══════╝╚═╝  ╚═╝╚═╝      ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝
#

def doExport(name, path):

    # Deselect all the objects
    bpy.ops.object.select_all(action='DESELECT')

    #Count all objects in the currently selected _export collection
    count = 0

    for obj in bpy.data.collections[name].all_objects:
        count+=1

    log(name + " contains " + str(count) + " objects")


    # Do the actual export, with big block of settings
    bpy.ops.export_scene.gltf( #Export settings:
        # Selection
        use_renderable                          = False,
        use_selection                           = False,
        use_visible                             = False,
        use_active_scene                        = False,
        use_active_collection                   = True,
        use_active_collection_with_nested       = True,

        # Basic export settings
        filepath                                = path,
        export_format                           = 'GLTF_SEPARATE',

        # Texture settings
        export_keep_originals                   = False, 	#
        export_image_format                     = 'AUTO', 	# `AUTO` | Images, Output format for images. PNG is lossless and generally preferred, but JPEG might be preferable for web applications due to the smaller file size. Alternatively they can be omitted if they are not needed\
        export_texture_dir                      = 'tex', 	#
        export_materials                        = 'EXPORT', #
        export_original_specular 				= False,    # false |  Export original PBR Specular, Export original glTF PBR Specular, instead of Blender Principled Shader Specular
        export_import_convert_lighting_mode     = 'SPEC',   # `SPEC` | Lighting Mode, Optional backwards compatibility for non-standard render engines. Applies to lights

        # Compression settings
        export_draco_mesh_compression_enable 	= False, 	# false | Draco mesh compression, Compress mesh using Draco
        export_draco_mesh_compression_level 	= 6, 		# 6  	| Compression level, Compression level (0 = most speed, 6 = most compression, higher values currently not supported)

        export_draco_color_quantization 		= 10,		# 10 	| Color quantization bits, Quantization bits for color values (0 = no quantization)
        export_draco_generic_quantization 		= 12, 		# 12 	| Generic quantization bits, Quantization bits for generic values like weights or joints (0 = no quantization)
        export_draco_normal_quantization 		= 10, 		# 10 	| Normal quantization bits, Quantization bits for normal values (0 = no quantization)
        export_draco_position_quantization 		= 14, 	 	# 14 	| Position quantization bits, Quantization bits for position values (0 = no quantization)
        export_draco_texcoord_quantization 		= 12, 		# 12 	| Texcoord quantization bits, Quantization bits for texture coordinate values (0 = no quantization)

        # Object data
        export_apply                            = True,      # true  | Apply Modifiers, Apply modifiers (excluding Armatures) to mesh objects -WARNING: prevents exporting shape keys
        export_attributes 						= False, 	 # false | Attributes, Export Attributes (when starting with underscore)
        export_colors                           = False,     # false | Vertex Colors, Export vertex colors with meshes
        export_copyright                        = '',        # ''    | Copyright, Legal rights and conditions for the model
        export_extras                           = False,     # false | Custom Properties, Export custom properties as glTF extras
        export_morph                            = True,      # true  | Shape Keys, Export shape keys (morph targets)
        export_morph_normal                     = True,      # true  | Shape Key Normals, Export vertex normals with shape keys (morph targets)
        export_morph_tangent                    = False,     # false | Shape Key Tangents, Export vertex tangents with shape keys (morph targets)
        export_normals                          = True,      # true  | Normals, Export vertex normals with meshes
        export_skins                            = True,      # true  | Skinning, Export skinning (armature) data
        export_tangents                         = True,      # true  | Tangents, Export vertex tangents with meshes
        export_texcoords                        = True,      # true  | UVs, Export UVs (texture coordinates) with meshes
        export_yup                              = True,      # true  | +Y Up, Export using glTF convention, +Y up
        use_mesh_edges                          = False,     # false | Loose Edges, Export loose edges as lines, using the material from the first material slot
        use_mesh_vertices                       = False,     # false | Loose Points, Export loose points as glTF points, using the material from the first material slot

        # Animation settings
        export_animations                       = True,      # true  | Animations, Exports active actions and NLA tracks as glTF animations
        export_current_frame                    = False,     # false | Use Current Frame, Export the scene in the current animation frame
        export_force_sampling                   = True,      # true  | Always Sample Animations, Apply sampling to all animations
        export_frame_range                      = True,      # true  | Limit to Playback Range, Clips animations to selected playback range
        export_frame_step                       = 1,         # 1     | Sampling Rate, How often to evaluate animated values (in frames)
        export_nla_strips                       = True,      # true  | Group by NLA Track, When on, multiple actions become part of the same glTF animation if they’re pushed onto NLA tracks with the same name. When off, all the currently assigned actions become one glTF animation
        export_nla_strips_merged_animation_name = 'action',  # 'Animation' | Merged Animation Name, Name of single glTF animation to be exported
        export_optimize_animation_size          = True,      # true  | Optimize Animation Size, Reduce exported file size by removing duplicate keyframes (can cause problems with stepped animation)

        # Armature settings
        export_all_influences                   = True,      # true  | Include All Bone Influences, Allow >4 joint vertex influences. Models may appear incorrectly in many viewers
        export_anim_single_armature             = True,      # true  | Export all Armature Actions, Export all actions, bound to a single armature. WARNING: Option does not support exports including multiple armatures
        export_def_bones                        = True,      # true  | Export Deformation Bones Only, Export Deformation bones only
        export_reset_pose_bones                 = True,      # true  | Reset pose bones between actions, Reset pose bones between each action exported. This is needed when some bones are not keyed on some animations

        # Extra objects
        export_cameras                          = False,  	 # Export camera
        export_lights                           = False  	 #
    )
    log("Finished attempting to export: " + name)
    log("------------------------------------------------")



# ███╗   ███╗ █████╗ ██╗███╗   ██╗
# ████╗ ████║██╔══██╗██║████╗  ██║
# ██╔████╔██║███████║██║██╔██╗ ██║
# ██║╚██╔╝██║██╔══██║██║██║╚██╗██║
# ██║ ╚═╝ ██║██║  ██║██║██║ ╚████║
# ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝
#

# Get absolute path:
path = bpy.path.abspath(OUTPUT_PATH)

if not os.path.exists(path):
    log("--------------------------------------------")
    log("ERROR: " + path)
    log("ERROR: the path above does not exist")
    log("--------------------------------------------")
else:
    log("Export path is determined as: " + path)

    # Trigger the export
    export2gltf(path)
    log("Export complete!")
