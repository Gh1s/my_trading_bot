import sys
import time
from multiprocessing import Process
from time import sleep
from bot.bot_services.bot_order import TradingOrder
from config.bot_config import logger, Config

fxcm_trading_configuration = Config().fxcm_trading_config

def multi_process_trading():
    p = Process(target=Bot_Starter, name='bot_process')
    p.start()
    p.join(timeout=295)
    p.terminate()

def Bot_Starter():
    logger.info("##############################  Trading Bot started  ##############################")
    try:
        for devise in fxcm_trading_configuration.devises:
            TradingOrder(devise)
        logger.info("############  Trading Analysis finish waiting for next process in 5 min  ###############")
        sys.exit(0)
    except Exception as e:
        logger.error("############  A problem occured when working on FXCM, {0}  ################".format(e))
        sys.exit(1)


if __name__ == "__main__":
    while True:
        start = time.time()
        multi_process_trading()
        end = time.time()
        range = end - start
        logger.info("##############################  Trading Bot ended in {0} seconds ##############################".format(int(range)))
        sleep(60)
