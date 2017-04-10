#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

class SimpleTask:
    """A simple abstract task definition"""

    def __init__(self, name=None, is_scheduled=False):
        """Instantiate a simple standard task"""
        self.logger = logging.getLogger('Scheduler')
        self.is_scheduled_task = is_scheduled
        self.task_name = name

    def run(self):
        """Running task method"""
        self.logger.warning("Task is not configured well: %s." %  "Need to override run method")

    def name(self):
        return self.task_name

    def is_scheduled(self):
        return self.is_scheduled_task