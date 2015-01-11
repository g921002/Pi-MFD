import pygame
from PiMFD.Pages.MFDPage import MFDRootPage
from PiMFD.Button import MFDButton

__author__ = 'Matt Eland'


class MFDController(object):

    display = None
    active_page = None
    continue_executing = True
    clock = None

    def __init__(self, display, app_options):

        self.display = display
        self.clock = pygame.time.Clock()

        if app_options is not None:
            self.app_name = app_options.app_name
            self.app_version = app_options.app_version

    def process_events(self):
        # Process all events
        events = pygame.event.get()
        for event in events:

            # Check for Window Close
            if event.type == pygame.QUIT:
                self.continue_executing = False

            # Check for Keyboard Input
            if event.type == pygame.KEYDOWN:

                # Handle escape by closing the app.
                if event.key == pygame.K_ESCAPE:
                    self.continue_executing = False

    def update_application(self):

        page = self.active_page

        page.top_headers = list()
        page.top_headers.append(MFDButton("SCH"))
        page.top_headers.append(MFDButton("NAV"))
        page.top_headers.append(MFDButton("SOC"))
        page.top_headers.append(MFDButton("MED"))
        page.top_headers.append(MFDButton("SYS", selected=True))

        page.bottom_headers = list()
        page.bottom_headers.append(MFDButton('TIME', selected=True))
        page.bottom_headers.append(MFDButton('PERF'))
        page.bottom_headers.append(MFDButton('NET'))
        page.bottom_headers.append(MFDButton('OPTS'))
        page.bottom_headers.append(MFDButton('EXIT'))

    def execute_main_loop(self):

        # Fill the background with black
        self.display.surface.fill(self.display.color_scheme.background)

        # Ensure a page is selected
        if self.active_page is None:
            self.active_page = MFDRootPage(self)

        # Update the headers
        self.update_application()

        # Render the current page
        self.active_page.render(self.display)

        # Handle input, allow user to close window / exit / control the app
        self.process_events()

        # Update the UI and give a bit of time before going again
        pygame.display.update()
        self.clock.tick(self.display.frames_per_second)

        pass