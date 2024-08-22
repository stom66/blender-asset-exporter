#    <Asset Exporter - a Blender addon to quickly extract collections of assets to glTF or FBX>
#
#    Copyright (C) <2024> <Tom Steventon>
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
	"name"       : "Asset Exporter",
	"description": "Quickly export multiple Collections to glTF or FBX",
	"author"     : "Tom Steventon - stom66",
	"version"    : (1, 0, 0),
	"blender"    : (4, 1, 0),
	"location"   : "3D Viewport -> Sidebar -> Asset Exporter",
	"category"   : "Import-Export",
	"doc_url"    : "https://github.com/stom66/blender-asset-exporter"
}

from . export_gltf  import *
from . export_fbx 	import *
from . _settings 	import *
from . ui 			import *


# ██████╗ ███████╗ ██████╗ ██╗███████╗████████╗██████╗  █████╗ ████████╗██╗ ██████╗ ███╗   ██╗
# ██╔══██╗██╔════╝██╔════╝ ██║██╔════╝╚══██╔══╝██╔══██╗██╔══██╗╚══██╔══╝██║██╔═══██╗████╗  ██║
# ██████╔╝█████╗  ██║  ███╗██║███████╗   ██║   ██████╔╝███████║   ██║   ██║██║   ██║██╔██╗ ██║
# ██╔══██╗██╔══╝  ██║   ██║██║╚════██║   ██║   ██╔══██╗██╔══██║   ██║   ██║██║   ██║██║╚██╗██║
# ██║  ██║███████╗╚██████╔╝██║███████║   ██║   ██║  ██║██║  ██║   ██║   ██║╚██████╔╝██║ ╚████║
# ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝
#
		
def register():
	# Register settings class
	bpy.utils.register_class(AssetExporterSettings)
	bpy.types.Scene.ae_settings = bpy.props.PointerProperty(type=AssetExporterSettings)

	bpy.utils.register_class(EXPORT_OT_AssetExporter_ExportToGLTF)
	bpy.utils.register_class(EXPORT_OT_AssetExporter_ExportToFBX)
	bpy.utils.register_class(VIEW3D_PT_AssetExporter_UI_Main)
	bpy.utils.register_class(VIEW3D_PT_AssetExporter_UI_FBX)
	bpy.utils.register_class(VIEW3D_PT_AssetExporter_UI_GLTF)


	

def unregister():
	# Unregister various UI component classes
	bpy.utils.unregister_class(VIEW3D_PT_AssetExporter_UI_Main)
	bpy.utils.unregister_class(VIEW3D_PT_AssetExporter_UI_FBX)
	bpy.utils.unregister_class(VIEW3D_PT_AssetExporter_UI_GLTF)
	bpy.utils.unregister_class(EXPORT_OT_AssetExporter_ExportToFBX)
	bpy.utils.unregister_class(EXPORT_OT_AssetExporter_ExportToGLTF)

	# Unregister settings class
	bpy.utils.unregister_class(AssetExporterSettings)
	del bpy.types.Scene.ae_settings
