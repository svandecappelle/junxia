#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import ConfigParser
import os
import importlib
import json

class Scheduler:
    """Scheduler is the main entry for launch deferred scheduled tasks"""

    def __init__(self):
        """Initialize a Scheduler task launcher"""
        self.logger = logging.getLogger('Scheduler')
        self.config = ConfigParser.ConfigParser()
        self.modulesConfiguration = ConfigParser.ConfigParser()
        self.modules = []

    def launch(self):
        """Launch the scheduled tasks configured"""
        self.logger.info("Loading tasks configured")
        self.configure()
        self.scan()
        moduleFileConfig = "%s/%s" % (self.modulesLocation, "modules.conf")
        self.logger.info("Loading module configuration: %s" % moduleFileConfig)
        self.modulesConfiguration.read(moduleFileConfig)

        moduleLaunchOrderFile = self.modulesConfiguration.get("general", "order")
        self.logger.info("Order json file: %s" % moduleLaunchOrderFile)

        self.moduleLaunchOrder = json.load(open("%s/%s" % (self.modulesLocation, moduleLaunchOrderFile)))["actives"]
        for module in self.moduleLaunchOrder:
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
