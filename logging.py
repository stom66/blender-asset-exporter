import bpy

LOG_PATH = "asset-exporter.log"

# Safely attempt to access bpy.data.texts
if hasattr(bpy.data, 'texts'):
    if LOG_PATH not in bpy.data.texts:
        LOG_TXT = bpy.data.texts.new(LOG_PATH)
    else:
        LOG_TXT = bpy.data.texts[LOG_PATH]
        LOG_TXT.clear()
else:
    LOG_TXT = None

def Log(message):
    print(message)
    if LOG_TXT:
        LOG_TXT.write(message + '\n')
