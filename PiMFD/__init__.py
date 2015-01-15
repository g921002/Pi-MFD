import pygame

from PiMFD.Applications.System.SystemApplication import SysApplication
from PiMFD.Controller import MFDController
from PiMFD.Applications.System.SystemPages import SysClockPage
from PiMFD.PygameHelpers import init_pygame_graphics


__author__ = 'Matt Eland'


class MFDAppOptions(object):
    app_name = 'Pi-MFD'
    app_version = '0.01 Development Version'
    app_author = 'Matt Eland'
    copyright_year = 2015
    font_name = 'Fonts/VeraMono.ttf'
    display = None
    location = '43035'


def start_mfd(display, app_options):

    # Start up the graphics engine
    init_pygame_graphics(display, app_options.app_name, app_options.font_name)

    # Initialize the controller
    controller = MFDController(display, app_options)

    # Main Processing Loop
    while not controller.requested_exit:
        controller.execute_main_loop()

    # Shutdown things that require it
    pygame.quit()