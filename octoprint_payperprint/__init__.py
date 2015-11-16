# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
from octoprint.util import RepeatedTimer
from octoprint.events import Events
from octoprint.filemanager.destinations import FileDestinations

class PayPerPrint(octoprint.plugin.TemplatePlugin,
                              octoprint.plugin.AssetPlugin,
                              octoprint.plugin.SimpleApiPlugin,
                              octoprint.plugin.EventHandlerPlugin,
                              octoprint.plugin.SettingsPlugin,
                              octoprint.plugin.StartupPlugin):
    filenameG = "";
    targetG = "";
    sdG = "";

    def on_event(self, event, payload):
        if event != "Upload":
                
                if not self._printer.is_ready():
                    self._logger.debug("Printer is not ready, not autoselecting uploaded file")
                        return
            
                filename = payload["file"]
                target = payload["target"]
                
                filenameG = filename
                targetG = target
                
                if target == FileDestinations.SDCARD:
                    path = filename
                        sd = True
                        sdG = sd
                else:
                    path = self._file_manager.path_on_disk(target, filename)
                        sd = False
                        sdG = sd
                
                self._logger.info("Selecting {} on {} that was just uploaded".format(filename, target))
                if payment():
                    self._printer.select_file(path, sd, False)
                else:
                    self.logger.info("You have to pay before youo print!")
                    return
        #DA TESTARE
        if event != Events.PRINT_DONE:
            return
        else:
            remove_file(self, filenameG, targetG)

    def payment():
        #CALCOLO COSTO + COMPARIRE FORM PAYPAL
        
    def remove_file(self, destination, path):
        #DA TESTARE
        self._storage(destination).remove_file(path)
        eventManager().fire(Events.UPDATED_FILES, dict(type="printables"))


def __plugin_load__():
    global __plugin_implementation__
        __plugin_name__ = "Pay Per Print"
        __plugin_implementation__ = PayPerPrint()
