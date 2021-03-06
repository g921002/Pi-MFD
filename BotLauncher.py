# coding=utf-8
"""
A full screen entry point for Raspberry Pi robot display usages.
"""
import traceback

from PiMFD.Options import MFDAppOptions
from PiMFD.UI.DisplayManager import DisplayManager


__author__ = 'Matt Eland'

log = open("PiMFD.log", "w")

try:
    # Initialize our settings. This will create a default settings file if none exists
    app_options = MFDAppOptions()
    app_options.load_from_settings()
    app_options.save_to_settings()
    app_options.save_map_to_disk = False

    # We really need to conserve space here
    app_options.font_scaling = 7
    app_options.min_font_size = 8

    # Create a new display in fullscreen mode without specifying resolution. Resolution will be auto-detected.
    display = DisplayManager(None, None)
    display.frames_per_second = 30
    display.show_mouse = False
    display.is_fullscreen = True

    # Launch!
    display.start_mfd(app_options)

except Exception as e:
    error_message = "Unhandled error {0}\n".format(str(traceback.format_exc()))

    print(error_message)
    log.write(error_message)

finally:
    log.close()
    pass