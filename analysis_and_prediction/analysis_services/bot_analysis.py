import numpy as np
import pandas as pd
import yfinance as yf
from prophet import Prophet
from config.bot_config import prophet_configuration, yahoo_config


def get_yahoo_data(ticker):
    df = yf.download(
        tickers=ticker,
        period=yahoo_config.period,
        interval=yahoo_config.interval)
    return df


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
    dt['cap'] = 8.5
    m = Prophet(growth="logistic",
                changepoint_prior_scale = 0.001,
                seasonality_prior_scale = 10.0).fit(dt)
    future = m.make_future_dataframe(periods=prophet_configuration.predictions)
    future['cap'] = 8.5
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
