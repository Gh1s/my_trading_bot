import pandas as pd
import numpy as np
from prophet import Prophet
#import yfinance as yf
from config.bot_config import prophet_config, yahoo_config, config_yaml


yahoo_configuration = yahoo_config(config_yaml)
prophet_configuration = prophet_config(config_yaml)


# def get_data():
#     df = yf.download(
#         tickers = yahoo_configuration.tickers,
#         period = yahoo_configuration.period,
#         interval = yahoo_configuration.interval,
#         group_by = yahoo_configuration.group_by,
#         auto_adjust = True,
#         threads = True,
#         proxy = None
#     )
#     df = df.dropna()
#     df.index = df.index.strftime('%Y/%m/%d %H:%M:%S')
#     return df


def mise_en_forme(data):
    liste = []
    for i in range(0, len(data)):
        liste.append(data[i])
    return liste


def prediction(data):
    dt = pd.DataFrame()
    dt['ds'] = data.index
    ma_liste = mise_en_forme(data['Close'])
    dt['y'] = ma_liste
    m = Prophet(changepoint_prior_scale=prophet_configuration.changepoint).fit(dt)
    future = m.make_future_dataframe(periods=prophet_configuration.predictions)
    frcst = m.predict(future)
    frcst['close'] = dt['y']
    return frcst


def dataframe_to_list(dataframe):
    price_close = []
    for item in dataframe:
        price_close.append(item)
    return price_close


def sell_analysis(df):
    df['sell_signal'] = np.where(df['close'] > df['yhat_upper'], 1, 0)
    df['sell_position'] = df['sell_signal'].diff()
    sell_signal = df['sell_position'].iloc[-5:-1]
    sell_signal = dataframe_to_list(sell_signal)
    return sell_signal


def buy_analysis(df):
    df['buy_signal'] = np.where(df['close'] < df['yhat_lower'], 1, 0)
    df['buy_position'] = df['buy_signal'].diff()
    buy_signal = df['buy_position'].iloc[-5:-1]
    buy_signal = dataframe_to_list(buy_signal)
    return buy_signal