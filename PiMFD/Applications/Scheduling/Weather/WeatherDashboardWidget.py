# coding=utf-8

"""
This file contains definitions for a custom dashboard widget for weather conditions and forecasts
"""
from pygame.rect import Rect

from PiMFD.Applications.Scheduling.Weather.WeatherData import get_condition_status, get_condition_icon
from PiMFD.UI.Panels import StackPanel
from PiMFD.UI.Rendering import render_rectangle
from PiMFD.UI.Text import TextBlock
from PiMFD.UI.Widgets.Charts import BoxChart
from PiMFD.UI.Widgets.DashboardWidget import DashboardWidget, DashboardStatus


__author__ = 'Matt Eland'


class WeatherForecastDashboardWidget(DashboardWidget):
    """
    A dashboard widget containing weather condition information
    :type display: PiMFD.UI.DisplayManager.DisplayManager
    :type page: PiMFD.Applications.Core.DashboardPages.DashboardPage
    :type title: str The name of the widget
    :type value: str The value used in the widget
    """

    def __init__(self, display, page, title, weather=None, forecast=None, is_forecast=True):
        super(WeatherForecastDashboardWidget, self).__init__(display, page, DashboardStatus.Inactive)

        self.title = title
        self.forecast = forecast
        self.weather = weather
        self.is_forecast = is_forecast
        self.minutes_to_clean_frost = None

        self.panel = StackPanel(display, page)

        self.lbl_title = TextBlock(display, page, title, is_highlighted=True)
        self.lbl_title.font = display.fonts.list
        self.panel.children.append(self.lbl_title)

        pnl_value = StackPanel(display, page, is_horizontal=True)
        pnl_value.center_align = True

        self.lbl_condition = TextBlock(display, page, "{}")
        self.lbl_condition.font = display.fonts.weather

        self.lbl_value = TextBlock(display, page, "Offline")
        self.lbl_value.font = display.fonts.list

        pnl_value.children = [self.lbl_value, self.lbl_condition]
        
        self.panel.children.append(pnl_value)

        self.chart = BoxChart(display, page)
        self.chart.width = 150
        self.chart.range_low = -20
        self.chart.range_high = 120
        self.chart.is_highlighted = False
        self.chart.box_width = 0
        self.chart.ticks = (0, 32, 100)
        self.panel.children.append(self.chart)

        self.lbl_frost = TextBlock(display, page, None)
        self.lbl_frost.font = display.fonts.list
        self.panel.children.append(self.lbl_frost)

    def render(self):

        # Colorize as needed
        color = self.get_color()
        self.lbl_value.color = color
        self.lbl_title.color = self.get_title_color()
        self.lbl_condition.color = color
        self.chart.color = color

        # Render an outline around the entire control
        rect = Rect(self.pos[0], self.pos[1], self.panel.desired_size[0] + (self.padding * 2),
                    self.panel.desired_size[1] + (self.padding * 2))

        # Some statuses need custom backgrounds
        if self.status == DashboardStatus.Caution:
            render_rectangle(self.display, self.display.color_scheme.caution_bg, rect, width=0)
        elif self.status == DashboardStatus.Critical:
            render_rectangle(self.display, self.display.color_scheme.critical_bg, rect, width=0)

        # Render the outline
        render_rectangle(self.display, color, rect)

        # Render the base content with some padding
        pos = self.pos[0] + self.padding, self.pos[1] + self.padding
        self.panel.render_at(pos)

        # Assume the width of the outer outline
        return self.set_dimensions_from_rect(rect)

    def arrange(self):

        self.status = self.get_status()
        self.lbl_title.text = self.title
        if self.forecast and self.weather:
            if not self.is_forecast:
                self.lbl_condition.text_data = get_condition_icon(self.weather.code)
                self.lbl_value.text = u'{}{}'.format(self.weather.temperature, self.weather.temp_units)
            else:
                self.lbl_condition.text_data = get_condition_icon(self.forecast.code)
                self.lbl_value.text = u'{}'.format(self.forecast.temp_range)
        else:
            self.lbl_condition.text_data = None
            self.lbl_value.text = 'Offline'

        if self.minutes_to_clean_frost and self.minutes_to_clean_frost > 0.1:
            self.lbl_frost.visible = True
            self.lbl_frost.text = '{} Minutes Frost'.format(round(self.minutes_to_clean_frost, 1))
        else:
            self.lbl_frost.visible = False
            self.lbl_frost.text = None

        if self.forecast:

            if not self.is_forecast:
                temp = float(self.weather.temperature)
                if temp >= 0:
                    self.chart.value_low = 0
                    self.chart.value_high = temp
                else:
                    self.chart.value_low = temp
                    self.chart.value_high = 0

            else:
                self.chart.value_low = self.forecast.low
                self.chart.value_high = self.forecast.high

        self.panel.arrange()
        self.desired_size = self.panel.desired_size[0] + (self.padding * 2), self.panel.desired_size[1] + (self.padding * 2)
        return self.desired_size

    def get_status(self):

        if not self.weather or not self.forecast:
            return DashboardStatus.Inactive

        temp_status = self.get_temperature_status()
        cond_status = get_condition_status(self.forecast.code)
        
        if cond_status == DashboardStatus.Critical or temp_status == DashboardStatus.Critical:
            return DashboardStatus.Critical

        if cond_status == DashboardStatus.Caution or temp_status == DashboardStatus.Caution:
            return DashboardStatus.Caution
        
        return temp_status

    def get_temperature_status(self):

        if not self.weather or not self.forecast:
            return DashboardStatus.Inactive
           
        # Certain Temperatures should function as alerts
        low = self.forecast.low
        high = self.forecast.high

        # If it's today, we don't care about forecast - go off of current temperature
        if not self.is_forecast:
            low = high = float(self.weather.temperature)
        
        if low <= 10 or high >= 100:
            return DashboardStatus.Critical
        elif low <= 32 or high >= 90:
            return DashboardStatus.Caution
        else:
            return DashboardStatus.Passive
