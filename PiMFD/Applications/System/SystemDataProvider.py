# coding=utf-8

"""
This file contains a data provider for system data
"""
import psutil

from PiMFD.DataProvider import DataProvider


__author__ = 'Matt Eland'


class SystemDataProvider(DataProvider):
    last_proc_update = None
    last_perf_update = None
    
    process_update_interval = 60
    perf_update_interval = 1
    
    def __init__(self, name, application):
        super(SystemDataProvider, self).__init__(name)

        self.application = application
        self.processes = []
        self.percentages = []
        self.virt_mem = None
        self.swap_mem = None

    def get_dashboard_widgets(self, display, page):
        return []

    def update(self, now):

        # Update Perf Data as needed
        if not self.last_perf_update or (now - self.last_perf_update).seconds >= self.perf_update_interval:
            self.percentages = psutil.cpu_percent(percpu=True)
            self.last_perf_update = now
        
        # Update Processes as needed
        if not self.last_proc_update or (now - self.last_proc_update).seconds >= self.process_update_interval:
            self.processes = psutil.get_process_list()
            self.virt_mem = psutil.virtual_memory()
            self.swap_mem = psutil.swap_memory()
            self.last_proc_update = now

        super(SystemDataProvider, self).update(now)