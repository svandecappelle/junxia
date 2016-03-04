#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

if __name__ == "__main__":
    FORMAT = '%(asctime)-15s %(clientip)s %(user)-8s %(message)s'
    logging.basicConfig(format=FORMAT)
    d = {'clientip': '192.168.0.1', 'user': 'fbloggs'}
    logger = logging.getLogger('junxia')

    logger.info('Launching junxia: %s', 'setup system tasks', extra=d)
