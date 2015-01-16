__author__ = 'Matt Eland'


class MFDPage(object):
    top_headers = list()
    bottom_headers = list()

    application = None
    controller = None
    display = None

    def __init__(self, controller, application):
        self.controller = controller
        self.display = controller.display
        self.application = application

    def handle_unselected(self):
        pass

    def handle_selected(self):
        pass

    def handle_reselected(self):
        self.application.page_reselected(self)

    def get_button_text(self):
        return 'UNKN'

    def render(self, display):
        pass


class SimpleMessagePage(MFDPage):

    button_text = "NI"
    message = "Not Implemented"

    def __init__(self, controller, application, label, message='Not Implemented'):
        super(SimpleMessagePage, self).__init__(controller, application)
        self.button_text = label
        self.message = message

    def get_button_text(self):
        return self.button_text

    def render(self, display):
        super(SimpleMessagePage, self).render(display)

        display.render_text_centered(self.display.font_normal,
                                     self.message,
                                     self.display.res_x / 2,
                                     (self.display.res_y / 2) - (self.display.font_size_normal / 2),
                                     self.display.color_scheme.foreground)