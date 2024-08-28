import bpy
import os


# ███████╗███████╗████████╗████████╗██╗███╗   ██╗ ██████╗ ███████╗
# ██╔════╝██╔════╝╚══██╔══╝╚══██╔══╝██║████╗  ██║██╔════╝ ██╔════╝
# ███████╗█████╗     ██║      ██║   ██║██╔██╗ ██║██║  ███╗███████╗
# ╚════██║██╔══╝     ██║      ██║   ██║██║╚██╗██║██║   ██║╚════██║
# ███████║███████╗   ██║      ██║   ██║██║ ╚████║╚██████╔╝███████║
# ╚══════╝╚══════╝   ╚═╝      ╚═╝   ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝
#

# Return a list of the available export operator presets
def list_presets(file_ext):
    preset_dir = bpy.utils.preset_paths(f'operator/export_scene.{file_ext}/')
    if not preset_dir:
        return [('NONE', 'No Presets Found', '')]

    presets = []
    for preset_path in preset_dir:
        for fname in os.listdir(preset_path):
            if fname.endswith(".py"):
                preset_name = os.path.splitext(fname)[0].replace("_", " ")
                presets.append((preset_name, preset_name, ""))
    return presets or [('NONE', 'No Presets Found', '')]



# Define default settings
class AssetExporterSettings(bpy.types.PropertyGroup):

    # String: Export collection prefix
	export_prefix: bpy.props.StringProperty(
		name        = "Collection prefix",
		description = "Specify the prefix used to search for collections",
		default     = "_export.",
	) # type: ignore

	# String: Output path
	output_path: bpy.props.StringProperty(
		name        = "Output folder",
		description = "Choose the folder to export to",
		default     = "//",
		subtype     = 'FILE_PATH'
	) # type: ignore


	
	#  ██████╗ ██╗  ████████╗███████╗
	# ██╔════╝ ██║  ╚══██╔══╝██╔════╝
	# ██║  ███╗██║     ██║   █████╗  
	# ██║   ██║██║     ██║   ██╔══╝  
	# ╚██████╔╝███████╗██║   ██║     
	#  ╚═════╝ ╚══════╝╚═╝   ╚═╝     


    # Dropdown: export preset
	gltf_preset: bpy.props.EnumProperty(
		name        = "glTF Preset",
		description = "Choose a glTF export preset",
		items       = list_presets("gltf")
	) # type: ignore

	# Dropdown: File format: gltf or glb
	gltf_export_format: bpy.props.EnumProperty(
		name        = "glTF Export format",
		description = "Output format. Binary is most efficient, but JSON maybe be easier to edit later. Separate textures allow for texture re-use.",
		default     = "GLTF_SEPARATE",
		items       = [
			("GLB",   		  "glTF Binary (.glb)",   					"Exports a single file, with all data packed in binary form. Most efficient and portable, more difficult to edit later and does not support texture re-use."),
			("GLTF_SEPARATE", "glTF Separate (.gltf + .bin + texture)", "Exports multiple files, with separate JSON, binary and texture data. Easiest to edit later and allows for textu re-reuse."),
		],
	) # type: ignore

	# --- Settings

	# Toggle: Draco compression
	gltf_use_draco: bpy.props.BoolProperty(
		name        = "Use Draco compression",
		description = "Should Draco compression be enabled - note this does not work with certain glTF viewers",
		default     = False,
	) # type: ignore

	# Toggle: Ignore root transform
	gltf_ignore_transform: bpy.props.BoolProperty(
		name        = "Ignore root transform",
		description = "If enabled, objects in the root of the collection will be moved back to 0,0,0 for the export. This is used to similar effect as the FBX option 'Apply transform'.",
		default     = False,
	) # type: ignore


	# Toggle: Workaround: Ignore root transform
	gltf_remove_modifier_smooth_by_angle: bpy.props.BoolProperty(
		name        = "Remove \"Smooth by Angle\" modifier",
		description = "Workaround for a bug with HardOps and the glTF exporter: Remove these modifiers on export as they currently cause problems with the glTF exporter",
		default     = True,
	) # type: ignore

	# Toggle: Workaround: Clean custom properties
	gltf_clean_custom_props: bpy.props.BoolProperty(
		name        = "Clean custom properties",
		description = "Workaround for a bug with HardOps and the glTF exporter: removes any custom properties from the mesh data block",
		default     = False,
	) # type: ignore




    # ███████╗██████╗ ██╗  ██╗ 
    # ██╔════╝██╔══██╗╚██╗██╔╝ 
    # █████╗  ██████╔╝ ╚███╔╝  
    # ██╔══╝  ██╔══██╗ ██╔██╗  
    # ██║     ██████╔╝██╔╝ ██╗ 
    # ╚═╝     ╚═════╝ ╚═╝  ╚═╝ 
    #

    # Dropdown: export preset
	fbx_preset: bpy.props.EnumProperty(
		name        = "FBX Preset",
		description = "Choose an FBX export preset",
		items       = list_presets("fbx")
	) # type: ignore

	# --- Settings

	# Toggle: Split NLA tracks 
	fbx_split_nla: bpy.props.BoolProperty(
		name        = "Split NLA tracks",
		description = "If enabled then multiple exports will be created, featuring a single NLA track per file",
		default     = False,
	) # type: ignore
