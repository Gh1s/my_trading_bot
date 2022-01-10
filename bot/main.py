import sys
from multiprocessing import Process
from time import sleep
import fxcmpy
from bot.bot_services.bot_order import TradingOrder
# from bot.bot_services.bot_services import deconnexion
from config.bot_config import logger, Config


fxcm_connection_configuration = Config().fxcm_connection_config
fxcm_trading_configuration = Config().fxcm_trading_config


def Bot_Starter():
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

        TradingOrder(connexion, fxcm_trading_configuration.devises)
        #forecast, sell_position, buy_position, trend, close_list = Multi_Devises_Strategy(connexion)
        logger.info("############  Close connection in progress  ###############")
        #deconnexion(forecast, sell_position, buy_position, trend, close_list)
        logger.info("############  Close connexion ok   ###############")
        #connexion.close()
    except Exception as e:
        logger.error("############  A problem occured when working on FXCM, {0}  ################".format(e))
        connexion.close()
        sys.exit(1)


if __name__ == "__main__":
    while True:
        p = Process(target=Bot_Starter, name='bot_process')
        p.start()
        p.join(timeout=360)
        p.terminate()
        # if p.exitcode is None:
        #     logger.error("############  A problem occured on FXCM server, timeout container reboot in process  ################")
        #     sys.exit(1)

        sleep(120)
