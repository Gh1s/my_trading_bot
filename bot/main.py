import logging
from analysis_and_prediction.analysis_services.bot_analysis import *
from bot.bot_services.bot_order import TradingOrder
from bot.bot_services.bot_services import log_mode_debug
from time import sleep


if __name__ == "__main__":   
    while True:
        log_mode_debug()
        #print("############  Get the data ###############")
        logging.info("############  Get the data ###############")
        df = get_data()
        #print("############  forecast beginning ###############")
        logging.info("############  forecast beginning ###############")
        forecast = prediction(df)
        yhat_upper = get_last_value(forecast['yhat_upper'])
        yhat_lower = get_last_value(forecast['yhat_lower'])
        yhat = get_last_value(forecast['yhat'])
        TradingOrder(yhat_upper, yhat_lower, yhat)
        logging.info("############  Displaying the chart on http://localhost:8050 ###############")


        sleep(300)
