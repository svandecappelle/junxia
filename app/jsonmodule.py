#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

from tasks.Tasks import SimpleTask

class JsonModule(SimpleTask):

    def __init__(self, module_path):
        SimpleTask.__init__(self)
        self.module_path = module_path
        self.is_json = True
        with open(self.module_path) as json_file:
            self.json_content = json.load(json_file)
            print(self.json_content)
            self.module_name = self.json_content["name"]
            self.logger.info(self.module_name)
            if self.json_content["trigger"]:
                self.is_scheduled_task = True
                self.task_trigger = self.json_content["trigger"]

    def name(self):
        return self.module_name

    def trigger(self):
        return self.task_trigger

