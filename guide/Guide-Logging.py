import os
import time
import logging
from datetime import datetime, timedelta
def setup_log(name):
    logger = logging.getLogger(name)  # > set up a new name for a new logger

    logger.setLevel(logging.DEBUG)  # here is the missing line
    log_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    path = f'data/Logs/{name}'
    filename = f"{path}/{name}_{datetime.now():%Y-%m-%d}.log"

    if not os.path.exists(path):
        os.makedirs(path)

    log_handler = logging.FileHandler(filename)
    log_handler.setLevel(logging.DEBUG)
    log_handler.setFormatter(log_format)

    logger.addHandler(log_handler)

    return logger


moduleName = __file__.split('\\')[-1][:-3]

logger = setup_log(moduleName)

t0 = time.time()

for i in range(0,100):
    print(i)
t1 = time.time()


logger.info(f'Prepare spending: {t1-t0:02f}')