from flask import Flask
from services.bot_services import *

#app = Flask(__name__)

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
        #app.run(debug=True)

      

