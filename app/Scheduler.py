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

from app.jsonmodule import JsonModule
from tasks.Launcher import TaskLauncher

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
        self.task_queue_launcher = TaskLauncher()
        
        self.tasks = []
        if daemon:
            self.logger.info("Starting configurator watcher service")
            self.watcher.watch()
        else:
            self.logger.info("Load all tasks configured")
            self.moduleLaunchOrder = json.load(open("%s/%s" % (self.modulesLocation, self.moduleLaunchOrderFile)))["actives"]
            
            without_order = []
            for module_order_conf in self.moduleLaunchOrder:
                for module in self.modules:
                    if (module.name() == module_order_conf):
                        self.tasks.append(module)
                    else:
                        without_order.append(module)
            
            self.tasks.extend(without_order)

        self.task_queue_launcher.start(self.tasks)


    def configure(self):
        self.config.read("junxia.conf")
        self.modulesLocation = self.config.get("modules", "location")
        moduleFileConfig = "%s/%s" % (self.modulesLocation, "modules.conf")
        self.logger.info("Loading module configuration: %s" % moduleFileConfig)
        self.modulesConfiguration.read(moduleFileConfig)

        self.moduleLaunchOrderFile = self.modulesConfiguration.get("general", "order")
        self.logger.info("Order json file: %s" % self.moduleLaunchOrderFile)

    def scan(self):
        self.watcher = ConfigWatcher(self.modulesLocation)
        self.logger.info("Scan for modules stored into the folder: %s" % (self.modulesLocation))

        for module in os.listdir(self.modulesLocation):
            if module.endswith('.py') and module != "__init__.py":
                moduleName = module[:-3]
                self.logger.info("Loading module %s" % (moduleName))
                self.modules.append(TaskLoader(self.modulesLocation).load(moduleName));
            elif module.endswith('.json') and module != self.moduleLaunchOrderFile:
                self.logger.info("Loading module %s" % (module))
                moduleJson = JsonModule("%s/%s" % (self.modulesLocation, module))
                self.modules.append(moduleJson);
                

class TaskLoader:
    """This class load and controls the tasks written in python"""

    def __init__(self, moduleLocation):
        self.logger = logging.getLogger('TaskLoader')
        self.moduleLocation = moduleLocation

    def load(self, module):
        self.logger.info("Load a configured module: %s" % (module))
        modulePackage = importlib.import_module("%s.%s" % (self.moduleLocation, module))
        runner = modulePackage.Runner(module)
        return runner

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
