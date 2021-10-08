from time import sleep
import sys
import fxcmpy
from bot.bot_services.bot_order import TradingOrder
from bot.bot_services.bot_services import deconnexion
from config.bot_config import logger, Config


fxcm_connection_configuration = Config().fxcm_connection_config
fxcm_trading_configuration = Config().fxcm_trading_config


if __name__ == "__main__":
    while True:
        #log_mode_debug()
        logger.info("############  Get the data ###############")
        logger.info("############  forecast beginning ###############")
        logger.info("############  Get the instruments  ###############")

        try:
            connexion = fxcmpy.fxcmpy(access_token=fxcm_connection_configuration.token,
                            log_level="error",
                            server=fxcm_connection_configuration.server_mode,
                            log_file=fxcm_connection_configuration.log_file)
            logger.info("############################## Connected to FXCM sucessful  ##############################")
            logger.info("############  Analysis for the following devises: {0}  ###############"
                        .format(fxcm_trading_configuration.devises))
            forecast, sell_position, buy_position, trend, close_list = TradingOrder(connexion,
                                                                                    fxcm_trading_configuration.devises)
            logger.info("############  Close connection in progress  ###############")
        except Exception as e:
            logger.error("############  Failed to connect to FXCM, {0}  ################".format(e))
            connexion.close()
            sys.exit(1)
        finally:
            deconnexion(forecast, sell_position, buy_position, trend, close_list)
            logger.info("############  Close connexion   ###############")
            connexion.close()

        sleep(300)
