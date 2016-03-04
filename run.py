#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from settings.logger import LoggerConfigurator
from app.Scheduler import Scheduler

if __name__ == "__main__":
    logger = logging.getLogger('junxia')

    loggerConfigurator = LoggerConfigurator()
    loggerConfigurator.configure()

    logger.info('Launching junxia: %s', 'start scheduled tasks')
    schedulerRunner = Scheduler()
    schedulerRunner.launch()
