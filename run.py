#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import sys, getopt

from settings.logger import LoggerConfigurator
from app.Scheduler import Scheduler
from app.Scheduler import ConfigWatcher

def main(argv):
    daemon = False
    try:
        opts, args = getopt.getopt(argv,"h",["daemon"])
    except getopt.GetoptError:
        print('test.py [-d] [--daemon]')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('test.py [-d] [--daemon]')
            sys.exit()
        elif opt in ("-d", "--daemon"):
            daemon = True
    logger = logging.getLogger('junxia')

    loggerConfigurator = LoggerConfigurator()
    loggerConfigurator.configure()

    logger.info('Launching junxia: %s', 'start scheduled tasks')
    schedulerRunner = Scheduler()
    schedulerRunner.launch(daemon=daemon)

if __name__ == "__main__":
    main(sys.argv[1:])
    
