from time import sleep

import fxcmpy

from bot.bot_services.bot_order import TradingOrder
from bot.bot_services.bot_services import log_mode_debug, get_instruments
from config.bot_config import logger, fxcm_connection_configuration, fxcm_trading_configuration

if __name__ == "__main__":
    while True:
        log_mode_debug()
        logger.info("############  Get the data ###############")

        logger.info("############  forecast beginning ###############")
        logger.info("############  Get the instruments  ###############")
        devises = get_instruments()

        try:
            connexion = fxcmpy.fxcmpy(access_token=fxcm_connection_configuration.token,
                                log_level="error",
                                server=fxcm_connection_configuration.server_mode,
                                log_file=fxcm_connection_configuration.log_file)
            logger.info("############################## Connected to FXCM sucessful  ##############################")
            logger.info("############  Analysis for the following devises: {0}  ###############"
                        .format(fxcm_trading_configuration.devises))
            forecast = TradingOrder(connexion, fxcm_trading_configuration.devises)
            logger.info("############  Close connection in progress  ###############")
        except Exception as e:
            logger.error("############  Failed to connect to FXCM, {0}  ################".format(e))

        finally:
            logger.error("############  Close connexion   ###############")
            connexion.close()

        sleep(300)
