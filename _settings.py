import bpy
import os


# ███████╗███████╗████████╗████████╗██╗███╗   ██╗ ██████╗ ███████╗
# ██╔════╝██╔════╝╚══██╔══╝╚══██╔══╝██║████╗  ██║██╔════╝ ██╔════╝
# ███████╗█████╗     ██║      ██║   ██║██╔██╗ ██║██║  ███╗███████╗
# ╚════██║██╔══╝     ██║      ██║   ██║██║╚██╗██║██║   ██║╚════██║
# ███████║███████╗   ██║      ██║   ██║██║ ╚████║╚██████╔╝███████║
# ╚══════╝╚══════╝   ╚═╝      ╚═╝   ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝
#


def list_fbx_presets(self, context):
    preset_dir = bpy.utils.preset_paths('operator/export_scene.fbx/')
    if not preset_dir:
        return [('NONE', 'No Presets Found', '')]

    presets = []
    for preset_path in preset_dir:
        for fname in os.listdir(preset_path):
            if fname.endswith(".py"):
                preset_name = os.path.splitext(fname)[0].replace("_", " ")
                presets.append((preset_name, preset_name, ""))
    return presets or [('NONE', 'No Presets Found', '')]


def list_gltf_presets(self, context):
    preset_dir = bpy.utils.preset_paths('operator/export_scene.gltf/')
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

    # String: current status of the plugin
    # This onyl exists as a way to show messages in the UI panel
	export_status: bpy.props.StringProperty(
		name        = "Export status",
		default     = "Ready",
	) # type: ignore

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

	# Dropdown: glTF: Export format
	export_format: bpy.props.EnumProperty(
		name   = "Export method",
		items  = [
			("GLTF", "glTF", "Export to glTF format"),
			("FBX",  "FBX",  "Export to FBX")
		],
		default = "GLTF",
	)  # type: ignore




	
	#  ██████╗ ██╗  ████████╗███████╗    ███████╗███████╗████████╗████████╗██╗███╗   ██╗ ██████╗ ███████╗
	# ██╔════╝ ██║  ╚══██╔══╝██╔════╝    ██╔════╝██╔════╝╚══██╔══╝╚══██╔══╝██║████╗  ██║██╔════╝ ██╔════╝
	# ██║  ███╗██║     ██║   █████╗      ███████╗█████╗     ██║      ██║   ██║██╔██╗ ██║██║  ███╗███████╗
	# ██║   ██║██║     ██║   ██╔══╝      ╚════██║██╔══╝     ██║      ██║   ██║██║╚██╗██║██║   ██║╚════██║
	# ╚██████╔╝███████╗██║   ██║         ███████║███████╗   ██║      ██║   ██║██║ ╚████║╚██████╔╝███████║
	#  ╚═════╝ ╚══════╝╚═╝   ╚═╝         ╚══════╝╚══════╝   ╚═╝      ╚═╝   ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝


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

	# Toggle: Ignore root transform
	gltf_remove_modifier_smooth_by_angle: bpy.props.BoolProperty(
		name        = "Remove \"Smooth by Angle\" modifier",
		description = "Remove these modifiers on export as they currently cause problems with the glTF exporter",
		default     = True,
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

    # Dropdown: export preset
	gltf_preset: bpy.props.EnumProperty(
		name        = "glTF Preset",
		description = "Choose a glTF export preset",
		items       = list_gltf_presets
	) # type: ignore



    # ███████╗██████╗ ██╗  ██╗    ███████╗███████╗████████╗████████╗██╗███╗   ██╗ ██████╗ ███████╗
    # ██╔════╝██╔══██╗╚██╗██╔╝    ██╔════╝██╔════╝╚══██╔══╝╚══██╔══╝██║████╗  ██║██╔════╝ ██╔════╝
    # █████╗  ██████╔╝ ╚███╔╝     ███████╗█████╗     ██║      ██║   ██║██╔██╗ ██║██║  ███╗███████╗
    # ██╔══╝  ██╔══██╗ ██╔██╗     ╚════██║██╔══╝     ██║      ██║   ██║██║╚██╗██║██║   ██║╚════██║
    # ██║     ██████╔╝██╔╝ ██╗    ███████║███████╗   ██║      ██║   ██║██║ ╚████║╚██████╔╝███████║
    # ╚═╝     ╚═════╝ ╚═╝  ╚═╝    ╚══════╝╚══════╝   ╚═╝      ╚═╝   ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝
    #

	# Toggle: Split NLA tracks 
	fbx_split_nla: bpy.props.BoolProperty(
		name        = "Split NLA tracks",
		description = "If enabled then multiple exports will be created, featuring a single NLA track per file",
		default     = False,
	) # type: ignore

    # Dropdown: export preset
	fbx_preset: bpy.props.EnumProperty(
		name        = "FBX Preset",
		description = "Choose an FBX export preset",
		items       = list_fbx_presets
	) # type: ignore
