import logging
import logging.config
logging.config.fileConfig('/a-fund/config/log.conf')
logger = logging.getLogger('fetch')
logger.info("fetch start")
print("1.py done")
logger.info("fetch end")