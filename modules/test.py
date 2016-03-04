#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tasks.Tasks import SimpleTask

class Runner(SimpleTask):
    """Simple test runner"""

    def __init__(self):
        """Initialize test runner"""
        SimpleTask.__init__(self)
        self.logger.info("Init test runner")
