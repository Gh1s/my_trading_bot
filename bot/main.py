from config.bot_config import logger
from analysis_and_prediction.analysis_services.bot_analysis import *
from bot.bot_services.bot_order import TradingOrder
from bot.bot_services.bot_services import log_mode_debug
from time import sleep


if __name__ == "__main__":   
    while True:
        log_mode_debug()
        logger.info("############  Get the data ###############")
        df = get_data()
        logger.info("############  forecast beginning ###############")
        forecast = prediction(df)
        yhat_upper = get_last_value(forecast['yhat_upper'])
        yhat_lower = get_last_value(forecast['yhat_lower'])
        yhat = get_last_value(forecast['yhat'])
        close = df['Close'][-1:]
        try:
            TradingOrder(yhat_upper, yhat_lower, yhat, close)
        except:
            logger.error("############  Failed to connect to FXCM  ################")
        finally:
            TradingOrder(yhat_upper, yhat_lower, yhat, close)
        logger.info("############  Trading Bot in Action ###############")

        sleep(300)
