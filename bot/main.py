import fxcmpy
from bot.bot_services.bot_order import TradingOrder
from config.bot_config import logger, Config
from multiprocessing import Process
import sys
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio

fxcm_connection_configuration = Config().fxcm_connection_config
fxcm_trading_configuration = Config().fxcm_trading_config

def multi_process_trading():
    p = Process(target=Bot_Starter, name='bot_process')
    p.start()
    p.join(timeout=295)
    p.terminate()

def Bot_Starter():
    global connexion
    logger.info("##############################  Trading Bot started  ##############################")

    try:
        connexion = fxcmpy.fxcmpy(access_token=fxcm_connection_configuration.token,
                                  log_level="error",
                                  server=fxcm_connection_configuration.server_mode,
                                  log_file=fxcm_connection_configuration.log_file)
        logger.info("############################## Connected to FXCM sucessful  ##############################")
    except Exception as e:
        logger.error("############  Failed to connect to FXCM, {0}  ################".format(e))
        connexion.close()
        sys.exit(1)

    try:

        for devise in fxcm_trading_configuration.devises:
            TradingOrder(connexion, devise)
            # forecast, sell_position, buy_position, trend, close_list = Multi_Devises_Strategy(connexion)
            logger.info("############  Close connection in progress  ###############")
            # deconnexion(forecast, sell_position, buy_position, trend, close_list)
            logger.info("############  Close connexion ok   ###############")
            # connexion.close()
    except Exception as e:
        logger.error("############  A problem occured when working on FXCM, {0}  ################".format(e))
        connexion.close()
        sys.exit(1)


if __name__ == "__main__":
    scheduler = AsyncIOScheduler()
    scheduler.add_job(multi_process_trading, 'interval', minutes=5)
    scheduler.start()
    asyncio.get_event_loop().run_forever()
