# coding=utf-8
"""
A fullscreen entry mode for Pi-MFD
"""
import traceback

from PiMFD.UI.DisplayManager import DisplayManager
from PiMFD.Options import MFDAppOptions


__author__ = 'Matt Eland'

log = open("PiMFD.log", "w")
try:
    # Initialize our settings. This will create a default settings file if none exists
    app_options = MFDAppOptions()
    app_options.load_from_settings()
    app_options.save_to_settings()

    # Create a new display in fullscreen mode without specifying resolution. Resolution will be auto-detected.
    display = DisplayManager(None, None)
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
