import sys
import time
from multiprocessing import Process
from time import sleep
from bot.bot_services.bot_order import TradingOrder
from bot.bot_services.bot_services import connexion_to_fxcm, deconnexion_from_fxcm
from config.bot_config import logger, Config

fxcm_trading_configuration = Config().fxcm_trading_config
trading_config = Config().trading_config

def multi_process_trading():
    #p = Process(target=Bot_Starter, name='bot_process')
    processes = [Process(target=Bot_Starter, args=(devise,), name='bot_process')
                 for devise in fxcm_trading_configuration.devises]
    for process in processes:
        process.start()
        process.join(timeout=trading_config.process_timeout)
        logger.info('process {0} done'.format(process))
        logger.info(process.exitcode)

def Bot_Starter(devise):
    logger.info("##############################  Trading Bot started  ##############################")
    try:
        #for devise in fxcm_trading_configuration.devises:
        connexion = connexion_to_fxcm()
        TradingOrder(devise, connexion)
        logger.info("############  Trading Analysis finish waiting for next process in 5 min  ###############")
        sys.exit(0)
    except Exception as e:
        logger.error("############  A problem occured when working on FXCM, {0}  ################".format(e))
        deconnexion_from_fxcm(connexion)
        sys.exit(1)
    finally:
        deconnexion_from_fxcm(connexion)

if __name__ == "__main__":
    while True:
        start = time.time()
        multi_process_trading()
        end = time.time()
        process_duration = end - start
        logger.info("##############################  Trading Bot ended in {0} seconds ##############################"
                    .format(int(process_duration)))
        sleep(trading_config.sleeping_time)
