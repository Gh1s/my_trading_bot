import pandas as pd
from fbprophet import Prophet
import yfinance as yf
import fxcmpy
from time import sleep
from config.bot_config import *


fxcm_connection = fxcm_connection_config()
fxcm_trading = fxcm_trading_config()
yahoo_config = yahoo_config()
prophet_config = prophet_config()

def get_data():
    df = yf.download(
        tickers = yahoo_config.tickers,
        period = yahoo_config.period,
        interval = yahoo_config.interval,
        group_by = yahoo_config.group_by,
        auto_adjust = True,
        threads = True,
        proxy = None
    )
    return df

def mise_en_forme(data):
    liste = []
    for i in range(0, len(data)):
        liste.append(data[i])
    return liste  

def get_last_value(list_temp):
    length_list = len(list_temp) - 30
    last_value = list_temp[length_list - 1]
    return last_value

def prediction(data):
    dt = pd.DataFrame()
    dt['ds'] = data.index
    ma_liste = mise_en_forme(data['Close'])
    dt['y'] = ma_liste
    m = Prophet().fit(dt)
    future = m.make_future_dataframe(periods=prophet_config.predictions)
    frcst = m.predict(future)
    return frcst


def TradingOrder(upper_limit, lower_limit, mean_limit):
    try:
        con = fxcmpy.fxcmpy(access_token=fxcm_connection.token, log_level="error", \
                            server=fxcm_connection.server_mode, log_file=fxcm_connection.log_file)
    except:
        print("Failed to connect to FXCM")
    con.subscribe_market_data(fxcm_trading.devises)
    price = con.get_last_price(fxcm_trading.devises)
    current_price_bid = price.Bid
    current_price_ask = price.Ask
    tradePosition = con.get_open_positions().T
    if tradePosition.empty is not True:
        if tradePosition[0][15] == True:
            buy_flag = True
            sell_flag = False
        else:
            buy_flag = False
            sell_flag = True
    else:
        buy_flag = False
        sell_flag = False

    if current_price_ask > upper_limit and sell_flag == False:

        print("Short Short Short")
        sell_flag = True
        order = con.create_market_sell_order(fxcm_trading.devises, fxcm_trading.order_amount)

    elif current_price_bid < lower_limit and buy_flag == False:

        print("Buy Buy Buy")
        buy_flag = True
        order = con.create_market_buy_order(fxcm_trading.devises, fxcm_trading.order_amount)

    elif sell_flag == True and current_price_bid <= mean_limit:

        print("Close the short position")
        sell_flag = False
        con.close_all_for_symbol(fxcm_trading.devises)

    elif buy_flag == True and current_price_ask >= mean_limit:

        print("Close the buy position")
        buy_flag = False
        con.close_all_for_symbol(fxcm_trading.devises)

    else:
        print("Stand By Position")

    #sleep(5)
    con.close()