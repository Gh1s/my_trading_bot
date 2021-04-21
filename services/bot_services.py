import pandas as pd
from fbprophet import Prophet
import yfinance as yf
from config.bot_config import *


def get_data():
    df = yf.download(
        tickers = yahoo_config(config_yaml).tickers,
        period = yahoo_config(config_yaml).period,
        interval = yahoo_config(config_yaml).interval,
        group_by = yahoo_config(config_yaml).group_by,
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
    future = m.make_future_dataframe(periods=prophet_config(config_yaml).predictions)
    frcst = m.predict(future)
    return frcst
