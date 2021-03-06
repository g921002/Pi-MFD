# coding=utf-8
from datetime import datetime

from PiMFD.Applications.System.ByteFormatting import format_size
from PiMFD.Applications.System.NetworkPages import NetworkPage
from PiMFD.UI.Widgets.Charts import BarChart
from PiMFD.UI.Panels import StackPanel


try:
    import psutil
except ImportError:
    psutil = None

from PiMFD.Applications.MFDPage import MFDPage
from PiMFD.UI.Widgets.MenuItem import TextMenuItem


__author__ = 'Matt Eland'


class ProcessDetailsPage(MFDPage):
    """
    :param controller: 
    :param application: 
    :param process: 
    :param auto_scroll:
    :type process: psutil.Process
    """

    def __init__(self, controller, application, process, auto_scroll=True):
        super(ProcessDetailsPage, self).__init__(controller, application, auto_scroll)

        self.process = process
        self.last_refresh = datetime.now()

        self.name = self.get_process_name(process)

        self.refresh_performance_counters()

    @staticmethod
    def get_process_name(process):
        try:
            return process.name()
        except:
            return "Unknown Process"        

    def render(self):
        return super(ProcessDetailsPage, self).render()

    def arrange(self):

        now = datetime.now()

        delta = now - self.last_refresh
        if delta.seconds >= 1:
            self.last_refresh = now
            self.refresh_performance_counters()

        return super(ProcessDetailsPage, self).arrange()

    def get_button_text(self):
        return "INFO"

    def refresh_performance_counters(self):

        self.panel.children = [self.get_header_label("{} (PID: {})".format(self.name, self.process.pid))]

        # Render CPU
        pct = self.process.cpu_percent()
        if not pct:
            pct = 0.0

        lbl_cpu = self.get_list_label("CPU:")
        lbl_cpu_pct = self.get_list_label("{} %".format(pct))
        chrt_cpu = BarChart(self.display, self, pct, width=25, height=lbl_cpu.font.size)
        pnl_cpu = StackPanel(self.display, self, is_horizontal=True)
        pnl_cpu.children = [lbl_cpu, chrt_cpu, lbl_cpu_pct]

        self.panel.children.append(pnl_cpu)

        # Render Memory
        mem = self.process.memory_info()
        if mem:
            pnl_mem = StackPanel(self.display, self)
            pnl_mem.children.append(self.get_label("Memory"))
            pnl_mem.children.append(self.get_list_label("Memory Usage: {}".format(format_size(mem.rss))))
            pnl_mem.children.append(self.get_list_label("Virtual Memory Size: {}".format(format_size(mem.vms))))
            self.panel.children.append(pnl_mem)

        # Render Connections
        try:
            connections = self.process.connections()
            if connections:
                pnl_connections = StackPanel(self.display, self)
                pnl_connections.children.append(self.get_label("Connections ({})".format(len(connections))))
                self.panel.children.append(pnl_connections)

                for c in connections:
                    if c.laddr == c.raddr:
                        address_text = NetworkPage.get_address_text(c.raddr)
                    else:
                        address_text = "{}({})".format(NetworkPage.get_address_text(c.raddr),
                                                       NetworkPage.get_address_text(c.laddr))

                    text = "{} {} {}/{}".format(c.status,
                                                address_text,
                                                NetworkPage.get_connection_type_text(c.type),
                                                NetworkPage.get_connection_family_text(c.family))

                    lbl = self.get_list_label(text)
                    pnl_connections.children.append(lbl)

        except psutil.NoSuchProcess or psutil.AccessDenied:
            pass

        # Render Files
        try:
            files = self.process.open_files()
        except psutil.AccessDenied:
            files = None
            
        if files:
            pnl_files = StackPanel(self.display, self)
            pnl_files.children.append(self.get_label("Files ({})".format(len(files))))

            for f in files:
                lbl = self.get_list_label(f.path)
                lbl.data_context = f
                pnl_files.children.append(lbl)

            self.panel.children.append(pnl_files)
                
        # Render Children
        try:
            children = self.process.children()
        except psutil.NoSuchProcess or psutil.AccessDenied:
            children = None

        if children:
            pnl_children = StackPanel(self.display, self)
            pnl_children.children.append(self.get_label("Children ({})".format(len(children))))

            for c in children:
                name = self.get_process_name(c)
                lbl = self.get_list_label("{}: {}".format(c.pid, name))
                lbl.data_context = c
                pnl_children.children.append(lbl)

            self.panel.children.append(pnl_children)

        # Render threads
        try:
            threads = self.process.threads()
        except psutil.AccessDenied or psutil.NoSuchProcess:
            threads = None
            
        if threads:
            pnl_threads = StackPanel(self.display, self)
            pnl_threads.children = [self.get_label("Threads ({})".format(len(threads)))]

            for t in threads:
                lbl = self.get_list_label("{}: User: {}, SYS: {}".format(t.id, t.user_time, t.system_time))
                pnl_threads.children.append(lbl)

            self.panel.children.append(pnl_threads)


class ProcessPage(MFDPage):

    def __init__(self, controller, application, auto_scroll=True):
        super(ProcessPage, self).__init__(controller, application, auto_scroll)

        self.last_refresh = datetime.now()
        self.refresh()

    def refresh(self,):

        if not psutil:
            return

        self.panel.children = [
            self.get_header_label('Processes ({})'.format(len(self.application.data_provider.processes)))]

        is_first_control = True

        for p in self.application.data_provider.processes:

            try:
                name = p.name()

            except psutil.AccessDenied:
                continue
                
            except psutil.NoSuchProcess:
                continue

            lbl = TextMenuItem(self.controller.display, self, "{}: {}".format(p.pid, name))
            lbl.font = self.display.fonts.list
            lbl.data_context = p

            self.panel.children.append(lbl)

            if is_first_control:
                self.set_focus(lbl)
                is_first_control = False

        self.last_refresh = datetime.now()

    def handle_control_state_changed(self, widget):

        process = widget.data_context

        if process:
            self.application.select_page(ProcessDetailsPage(self.controller, self.application, process))

        super(ProcessPage, self).handle_control_state_changed(widget)

    def arrange(self):

        if (len(self.panel.children) <= 1 and self.application.data_provider.processes) or (
            datetime.now() - self.last_refresh).seconds > 15:
            self.refresh()
        
        return super(ProcessPage, self).arrange()

    def render(self):

        if not psutil:
            self.center_text("psutil offline".upper())

        return super(ProcessPage, self).render()

    def handle_reselected(self):
        self.refresh()
        super(ProcessPage, self).handle_reselected()

    def get_button_text(self):
        return "PROC"




