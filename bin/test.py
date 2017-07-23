#!/usr/local/bin/python3
import logging
import logging.config
logging.config.fileConfig('/a-fund/config/log.conf')   
logger = logging.getLogger('all')
logger.info("autorun successful")

import os
os.system("/usr/local/bin/python3 /a-fund/fetch/1.py")
os.system("/usr/local/bin/python3 /a-fund/process/2.py")