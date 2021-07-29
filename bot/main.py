from time import sleep
from bot.bot_services.bot_order import TradingOrder
from bot.bot_services.bot_services import log_mode_debug
from config.bot_config import logger


if __name__ == "__main__":
    while True:
        log_mode_debug()
        logger.info("############  Get the data ###############")

        logger.info("############  forecast beginning ###############")

        try:
            forecast = TradingOrder()
        except:
            logger.error("############  Failed to connect to FXCM  ################")

        sleep(900)
