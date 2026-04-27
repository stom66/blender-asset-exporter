import bpy
import os
from . addon_log import Log


def _output_path_is_blend_relative(raw: str) -> bool:
	"""True if the user path uses Blender's // (relative to the .blend file) convention."""
	n	= raw.replace("\\", "/").strip()
	return n.startswith("//")


def get_export_path_or_error() -> tuple[str | None, str | None]:
	"""
	Resolve the output *directory* from scene settings, create it if possible.

	Returns:
		(absolute_dir_path, None) on success,
		(None, user-facing error message) on failure.
	"""
	ae_settings	= bpy.context.scene.ae_settings
	raw		= (ae_settings.output_path or "").strip()
	if not raw:
		return None, "Set a valid output folder in Asset Exporter (the path is empty)."

	# //... is resolved relative to the .blend on disk. Unsaved files have no base, so exports end up in an arbitrary location.
	if _output_path_is_blend_relative(raw) and not bpy.data.filepath:
		return None, "Save the .blend file first, or set Output folder to a full path. Paths starting with // are relative to the saved file, so they are not reliable for an unsaved file."

	try:
		path	= bpy.path.abspath(raw)
	except Exception as e:
		Log(f"AssetExporter: get_export_path_or_error: abspath failed: {e!r}")
		return None, "Could not resolve the output path. Use a folder under the blend (e.g. //exports/) or a full path to a folder you can write to."

	path	= os.path.normpath(path)
	if not path:
		return None, "Set a valid output folder in Asset Exporter."

	try:
		os.makedirs(path, exist_ok=True)
	except OSError as e:
		Log(f"AssetExporter: get_export_path_or_error: makedirs failed: {e!r}")
		return None, "Cannot create or use the output folder. Choose a valid, writable path in Asset Exporter."

	return path, None


def read_export_operator_preset(preset: str, file_ext: str) -> tuple[dict | None, str | None]:
	"""
	Read and parse a Blender export operator preset.

	Args:
		preset (str): The name of the preset file (without the extension).
		file_ext (str): The file extension related to the export type (e.g., 'gltf', 'fbx').

	Returns:
		On success: (export_settings dict, None).
		On failure: (None, user-facing error message).
	"""

	export_settings = {}

	preset_subpath = f'operator/export_scene.{file_ext}/'
	preset_dirs = bpy.utils.preset_paths(preset_subpath)
	if not preset_dirs:
		msg = (
			f'No export preset support is registered for "{file_ext}" in this Blender build. '
			'Open File → Export for that format, configure the dialog, then save a preset from the preset menu; '
			'after that, choose it in Asset Exporter before exporting.'
		)
		return None, msg

	preset_file_path = os.path.join(preset_dirs[0], preset.replace(" ", "_") + ".py")
	if not os.path.exists(preset_file_path):
		msg = (
			f'Preset "{preset}" was not found. '
			'Save a preset with that name from the export dialog, or pick another preset in Asset Exporter settings.'
		)
		return None, msg

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
		export_settings[key] = op.__dict__[key]

	Log("Finished building export settings")

	return export_settings, None


def ensure_object_mode() -> None:
    """
    Ensure that the active object is in Object Mode. 
    If the current mode is not Object Mode, switch to Object Mode.
    
    Returns:
        None
    """
    # Ensure there is an active object
    if bpy.context.object:
        # Check if the current mode is not Object Mode
        if bpy.context.object.mode != 'OBJECT':
            # Switch to Object Mode
            bpy.ops.object.mode_set(mode='OBJECT')
    else:
        print("No active object to switch mode.")


def disable_smooth_by_angle_modifier(obj: bpy.types.Object) -> None:
    """
    Disable or remove the 'Smooth by Angle' modifier on the given object.
    
    Args:
        obj (bpy.types.Object): The object to process.

    Returns:
        None
    """
    for mod in obj.modifiers:
        if mod.name == '!!Smooth by Angle' or mod.name == "Smooth by Angle":
            Log(f"Disabling '!!Smooth by Angle' modifier for object: {obj.name}")
            obj.modifiers.remove(mod)


def clean_custom_properties(obj: bpy.types.Object) -> None:
    """
    Remove specific custom properties from the mesh data of the given object.

    Args:
        obj (bpy.types.Object): The object whose mesh data custom properties should be cleaned.

    Returns:
        None
    """
    if obj.type == 'MESH':
        if obj.data:
            keys_to_remove = [key for key in obj.data.keys() if key.startswith("_") or key == "hops"]
            for key in keys_to_remove:
                del obj.data[key]


def apply_identity_transforms(self, collection: bpy.types.Collection):
    """
    Temporarily reset transforms (location, rotation, scale) to identity values 
    for all top-level objects in the given collection.

    Args:
        collection (bpy.types.Collection): The collection containing the objects to process.

    Returns:
        dict: A dictionary mapping objects to their original transforms.
    """
    orig_transforms = {}
    for obj in bpy.data.collections.get(collection.name).objects:
        # Only reset transforms for top-level, non-armature objects.
        # Armatures often define the orientation for skinned meshes, and
        # touching their object transforms can lead to unexpected rotation
        # offsets in the scene after export.
        if obj.parent is None and obj.type != 'ARMATURE':
            print("Ignoring transform for", obj.name)
            orig_transforms[obj] = {
                'location': obj.location.copy(),
                'rotation_euler': obj.rotation_euler.copy(),
                'scale': obj.scale.copy()
            }
            obj.location = (0, 0, 0)
            obj.rotation_euler = (0, 0, 0)
            obj.scale = (1, 1, 1)
    return orig_transforms


def restore_original_transforms(self, orig_transforms: dict):
    """
    Restore original transforms (location, rotation, scale) to the objects 
    previously processed by apply_identity_transforms.

    Args:
        orig_transforms (dict): A dictionary mapping objects to their original transforms.

    Returns:
        None
    """
    for obj, transform in orig_transforms.items():
        obj.location = transform['location']
        obj.rotation_euler = transform['rotation_euler']
        obj.scale = transform['scale']


def FindCollectionsWithPrefix(prefix: str) -> dict[str, bpy.types.LayerCollection]:

	collections: dict[str, bpy.types.LayerCollection]	= {}

	if not prefix:
		return collections

	def visit_layer_collection(layer_col: bpy.types.LayerCollection) -> None:
		for child in layer_col.children:
			# Match only names that *start* with the prefix; export base name is the remainder (prefix length only)
			if child.name.startswith(prefix) and not child.exclude:
				Log("Found collection to export: " + child.name)
				col_name	= child.name[len(prefix):]
				collections[col_name]	= child
			visit_layer_collection(child)

	visit_layer_collection(bpy.context.view_layer.layer_collection)

	return collections