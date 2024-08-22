import 	bpy
import 	os
import 	json
from 	collections 			import defaultdict
from 	xml.etree.ElementTree 	import tostring


# ██████╗  █████╗ ████████╗██╗  ██╗
# ██╔══██╗██╔══██╗╚══██╔══╝██║  ██║
# ██████╔╝███████║   ██║   ███████║
# ██╔═══╝ ██╔══██║   ██║   ██╔══██║
# ██║     ██║  ██║   ██║   ██║  ██║
# ╚═╝     ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝
#

def GetExportPath() -> str:
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
