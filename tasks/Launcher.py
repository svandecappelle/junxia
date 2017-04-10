#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import threading

from multiprocessing import Process, Queue, TimeoutError

class TaskLauncher:
    """
    Loop task launcher.
    """

    def __init__(self, workers=5):
        """
        Constructor
        """
        self.workers = workers


    def wait_for_process(self, parameters):
        """
        Wait for call process
        """
        while True:
            try:
                print("wait for process")

                time.sleep(1)
            except Queue.Empty:
                break

    def decode(self, task):
        """
        Decode task conf
        """
        print("decode task: %s" % task.name())
        if task.is_scheduled():
            print("Task is scheduled to: %s" % task.trigger())

    def start(self, tasks):
        """
        Start a process to call deferred launch
        """
        #res = PPool().amap(triple, PPool().map(squared, xrange(self.workers)))
        #res.get()
        for index, task in enumerate(tasks):
            self.decode(task)

        print('creating queue')
        q = Queue()

        print('enqueuing')
        for i in range(100):
            q.put(i)

        num_processes = self.workers
        pool = []

        for i in range(num_processes):
            print('launching process {0}'.format(i))
            p = Process(target=self.wait_for_process, args=(q,))
            p.start()
            pool.append(p)

        for p in pool:
            p.join()