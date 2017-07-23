import logging
import logging.config
logging.config.fileConfig('/a-fund/config/log.conf')
logger = logging.getLogger('process_db')
logger.info("process_db start")
print("2.py done")
logger.info("process_db end")