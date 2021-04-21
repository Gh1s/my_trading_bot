from services.bot_services import *
from services.bot_order import TradingOrder
from time import sleep
global buy_flag
global sell_flag


if __name__ == "__main__":   
    while True:

        df = get_data()
        df = df.dropna()
        df.index = df.index.strftime('%Y/%m/%d %H:%M:%S')
        forecast = prediction(df)
        yhat_upper = get_last_value(forecast['yhat_upper'])
        yhat_lower = get_last_value(forecast['yhat_lower'])
        yhat = get_last_value(forecast['yhat'])
        TradingOrder(yhat_upper, yhat_lower, yhat)

              
        sleep(300)
