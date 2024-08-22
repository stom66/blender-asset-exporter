import bpy

from . logging import Log

def FindCollectionsWithPrefix(prefix: str):

	collections = {}

	# Loop through all collections in the current view layer
	for col in bpy.context.view_layer.layer_collection.children:

		# Check if the colelction name contains the MATCH_STRING
		if col.name.count(prefix) and not col.exclude:

			# Log success: found a collection to export and flip found flag
			Log("Found collection to export: " + col.name)

			# Set the export file name to match the collection name (minus the MATCH_STRING)
			col_name = col.name.replace(prefix, '')

			collections[col_name] = col
	
	return collections