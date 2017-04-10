#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import configparser
import os
import importlib
import json

import pyinotify
import asyncio
from multiprocessing import Process, Queue, TimeoutError
    
class Scheduler:
    """Scheduler is the main entry for launch deferred scheduled tasks"""

    def __init__(self):
        """Initialize a Scheduler task launcher"""
        self.logger = logging.getLogger('Scheduler')
        self.config = configparser.ConfigParser()
        self.modulesConfiguration = configparser.ConfigParser()
        self.modules = []

    def launch(self, daemon=False):
        """Launch the scheduled tasks configured"""
        self.logger.info("Loading tasks configured")
        self.configure()
        self.scan()
        
        if daemon:
            self.logger.info("Starting configurator watcher service")
            self.watcher.watch()
        else:
            moduleFileConfig = "%s/%s" % (self.modulesLocation, "modules.conf")
            self.logger.info("Loading module configuration: %s" % moduleFileConfig)
            self.modulesConfiguration.read(moduleFileConfig)

            moduleLaunchOrderFile = self.modulesConfiguration.get("general", "order")
            self.logger.info("Order json file: %s" % moduleLaunchOrderFile)
            
            self.logger.info("Load all tasks configured")
            self.moduleLaunchOrder = json.load(open("%s/%s" % (self.modulesLocation, moduleLaunchOrderFile)))["actives"]
            for module in self.moduleLaunchOrder:
                TaskLoader(self.modulesLocation).load(module)

    def configure(self):
        self.config.read("junxia.conf")

    def scan(self):
        self.modulesLocation = self.config.get("modules", "location")
        self.watcher = ConfigWatcher(self.modulesLocation)
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

class ConfigWatcher:

    def __init__(self, scan_folder):
        """
        """
        self.logger = logging.getLogger('ConfigWatcher')
        self.scan_folder = scan_folder

    def handle_read_callback(self, notifier):
        """
        Just stop receiving IO read events after the first
        iteration (unrealistic example).
        """
        print('Action on modules parameters folder.')

        #notifier.loop.stop()
    
    def scanner(self, watcher_process_queue):
        self.logger.info('Wartchong folder.')
        wm = pyinotify.WatchManager()
        loop = asyncio.get_event_loop()
        notifier = pyinotify.AsyncioNotifier(wm, loop,
                                            callback=self.handle_read_callback)
        wm.add_watch(self.scan_folder, pyinotify.ALL_EVENTS)
        loop.run_forever()
        notifier.stop()

    def watch(self):
        self.watcher_process_queue = Queue()
        self.process = Process(target=self.scanner, args=(self.watcher_process_queue,))
        self.process.start()
        self.process.join() 
