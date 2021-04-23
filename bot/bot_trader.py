import logging
from analysis_and_prediction.analysis_services.bot_analysis import *
from bot.bot_services.bot_order import TradingOrder
from time import sleep


if __name__ == "__main__":   
    while True:

        print("Get the data")
        logging.info("Get the data")
        df = get_data()
        print("forecast beginning")
        logging.info("forecast beginning")
        forecast = prediction(df)
        yhat_upper = get_last_value(forecast['yhat_upper'])
        yhat_lower = get_last_value(forecast['yhat_lower'])
        yhat = get_last_value(forecast['yhat'])
        TradingOrder(yhat_upper, yhat_lower, yhat)
        print("############  Displaying the chart  ###############")


        sleep(300)
