import bpy
import os
from . logging import Log

def get_export_path() -> str:
	"""
	Get the export path for the collection.

	Returns:
	- str: The export path.
	"""
	# Get settings
	ae_settings = bpy.context.scene.ae_settings

	# Get the export path based on the current settings value
	path = bpy.path.abspath(ae_settings.output_path)

	# Ensure the output folder exists
	try:
		# Ensure filepath exists, create it if it doesn't
		os.makedirs(os.path.dirname(path))
	except FileExistsError:
		pass  # The directory already exists, no need to create

	# Normalise the output path, ensuring correct os.sep is used
	path = os.path.normpath(path)

	return path


def read_export_operator_preset(preset: str, file_ext: str) -> dict:
	"""
	Read and parse a Blender export operator preset.

	Args:
		preset (str): The name of the preset file (without the extension).
		file_ext (str): The file extension related to the export type (e.g., 'gltf', 'fbx').

	Returns:
		dict: A dictionary containing export settings if the preset exists.
		bool: False if the preset file does not exist.
	"""

	# Get ready to store contents
	export_settings = {}

	preset_file_path = os.path.join(bpy.utils.preset_paths(f'operator/export_scene.{file_ext}/')[0], preset.replace(" ", "_") + ".py")
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
			export_settings[key] = op.__dict__[key]

		Log("Finished building export settings")

		return export_settings

	else:
		return False


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


def clean_hardops_properties(obj: bpy.types.Object) -> None:
	"""
	Remove specific custom properties from the mesh data of the given object.

	Args:
		obj (bpy.types.Object): The object whose mesh data custom properties should be cleaned.

	Returns:
		None
	"""

	# Check if the object has custom properties (ID properties)
	if obj.data and hasattr(obj.data, 'keys'):
		# Iterate over the keys (properties)
		keys_to_remove = []
		for key in obj.data.keys():
			# Identify HardOps-related properties
			if key.startswith('hops'):
				keys_to_remove.append(key)
		
		# Remove the identified properties
		for key in keys_to_remove:
			del obj.data[key]
			print(f"Removed custom property '{key}' from object '{obj.name}'.")

	print("Finished removing HardOps custom properties.")


def get_all_objects_in_collection(collection):
	objects = set()

	for obj in collection.objects:
		objects.add(obj)
	for child_collection in collection.children:
		objects.update(get_all_objects_in_collection(child_collection))

	return objects