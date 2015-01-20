# coding=utf-8
"""
Holds the weather page
"""
from PiMFD.Applications.MFDPage import MFDPage
from PiMFD.UI.Panels import StackPanel

__author__ = 'Matt Eland'


class WeatherPage(MFDPage):
    """
    A page containing weather and forecast data.
    """

    pnl_today = None
    pnl_forecast = None
    lbl_today_header = None
    lbl_cond = None
    lbl_wind = None
    lbl_humidity = None
    lbl_visible = None
    lbl_pressure = None
    lbl_daylight = None
    lbl_gps = None
    lbl_updated = None
    lbl_forecast = None

    max_forecasts = 5

    # noinspection PyCompatibility
    def __init__(self, controller, application):
        super(WeatherPage, self).__init__(controller, application)

        # Build out the Today Panel
        self.pnl_today = StackPanel(controller.display, self)
        self.lbl_today_header = self.get_header_label("{} Weather")
        self.lbl_temp = self.get_label(u"      Temp: {} (Chill: {})")
        self.lbl_cond = self.get_label(u"Conditions: {}")
        self.lbl_wind = self.get_label(u"      Wind: {} {}")
        self.lbl_humidity = self.get_label(u"  Humidity: {}")
        self.lbl_visible = self.get_label(u"Visibility: {}")
        self.lbl_pressure = self.get_label(u"  Pressure: {}")
        self.lbl_daylight = self.get_label(u"  Daylight: {} - {}")
        self.lbl_gps = self.get_label(u"       GPS: {}, {}")
        self.lbl_updated = self.get_label(u"   Updated: {}")

        self.pnl_today.children = (
            self.lbl_today_header,
            self.lbl_temp,
            self.lbl_cond,
            self.lbl_wind,
            self.lbl_humidity,
            self.lbl_visible,
            self.lbl_pressure,
            self.lbl_daylight,
            self.lbl_gps,
            self.lbl_updated
        )

        # Build out the Forecast Panel
        self.pnl_forecast = StackPanel(controller.display, self)
        forecast_header = self.get_header_label("Forecast")
        self.pnl_forecast.children.append(forecast_header)

        # Add placeholders for the individual forecasts
        self.lbl_forecast = dict()
        for i in range(0, self.max_forecasts):
            label = self.get_label(u"{}: {}")
            self.lbl_forecast[i] = label
            self.pnl_forecast.children.append(label)

        # Set up the master panel
        self.panel.is_horizontal = True
        self.panel.children = (self.pnl_today, self.pnl_forecast)


    def get_button_text(self):
        """
        Gets the text for the application's button
        :return: Text for the application's button
        """
        return "WTHR"

    def render(self):
        """
        Renders the weather page
        """

        weather = self.application.weather_data

        self.lbl_today_header.text_data = weather.city
        self.lbl_temp.text_data = (weather.temperature, weather.windchill)
        self.lbl_cond.text_data = weather.conditions
        self.lbl_wind.text_data = (weather.wind_speed, weather.wind_cardinal_direction)
        self.lbl_humidity.text_data = weather.humidity
        self.lbl_visible.text_data = weather.visibility
        self.lbl_pressure.text_data = weather.pressure
        self.lbl_daylight.text_data = (weather.sunrise, weather.sunset)
        self.lbl_gps.text_data = (weather.lat, weather.long)
        self.lbl_updated.text_data = weather.last_result

        # Update Forecasts
        for i in range(0, self.max_forecasts):
            label = self.lbl_forecast[i]
            forecast = weather.forecasts[i]
            label.text_data = (forecast.day, forecast.temp_range)

        # y += render_text(display, display.font_weather, "abcdefghij", x, y, cs.foreground).height + display.padding_y

        super(WeatherPage, self).render()