#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tasks.Tasks import SimpleTask

class Runner(SimpleTask):
    """Simple test runner"""

    def __init__(self, name):
        """Initialize test runner"""
        SimpleTask.__init__(self, name)
        self.logger.info("Init test runner")

    def run(self):
        """Running task method"""
        self.logger.info("Running test python module")