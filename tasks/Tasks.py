#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

class SimpleTask:
    """A simple abstract task definition"""

    def __init__(self):
        """Instantiate a simple standard task"""
        self.logger = logging.getLogger('Scheduler')

    def run(self):
        """Running task method"""
        self.logger.warning("Task is not configured well: %s." %  "Need to override run method")
