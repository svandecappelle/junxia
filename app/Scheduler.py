#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import ConfigParser
import os
import importlib

class Scheduler:
    """Scheduler is the main entry for launch deferred scheduled tasks"""

    def __init__(self):
        """Initialize a Scheduler task launcher"""
        self.logger = logging.getLogger('Scheduler')
        self.config = ConfigParser.ConfigParser()
        self.modules = []

    def launch(self):
        """Launch the scheduled tasks configured"""
        self.logger.info("Loading tasks configured")
        self.configure()
        self.scan()
        for module in self.modules:
            TaskLoader(self.modulesLocation).load(module)

    def configure(self):
        self.config.read("junxia.conf")

    def scan(self):
        self.modulesLocation = self.config.get("modules", "location")
        self.logger.info("Scan for modules stored into the folder: %s" % (self.modulesLocation))
        
        for module in os.listdir(self.modulesLocation):
            if module.endswith('.py') and module != "__init__.py":
                moduleName = module[:-3]
                self.logger.info("Loading module %s" % (moduleName))
                self.modules.append(moduleName);

class TaskLoader:
    """This class load and controls the tasks written in python"""

    def __init__(self, moduleLocation):
        self.logger = logging.getLogger('TaskLoader')
        self.moduleLocation = moduleLocation

    def load(self, module):
        self.logger.info("Load a configured module: %s" % (module))
        modulePackage = importlib.import_module("%s.%s" % (self.moduleLocation, module))
        runner = modulePackage.Runner()
        runner.run()
