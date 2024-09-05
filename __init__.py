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
	"version"    : (0, 2, 4),
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

classes = (
	AssetExporterSettings,
	EXPORT_OT_AssetExporter_ExportToGLTF,
	EXPORT_OT_AssetExporter_ExportToFBX,
	VIEW3D_PT_AssetExporter_UI_Main,
	VIEW3D_PT_AssetExporter_UI_FBX,
	VIEW3D_PT_AssetExporter_UI_FBX_Settings,
	VIEW3D_PT_AssetExporter_UI_FBX_Btn,
	VIEW3D_PT_AssetExporter_UI_GLTF,
	VIEW3D_PT_AssetExporter_UI_GLTF_Settings,
	VIEW3D_PT_AssetExporter_UI_GLTF_Btn
)

def register():
	# Register classes
	for cls in classes:
		bpy.utils.register_class(cls)

	# Register settings
	bpy.types.Scene.ae_settings = bpy.props.PointerProperty(type=AssetExporterSettings)

def unregister():
	# Unregister all classes
	for cls in classes:
		bpy.utils.unregister_class(cls)

	# Unregister settings
	del bpy.types.Scene.ae_settings
