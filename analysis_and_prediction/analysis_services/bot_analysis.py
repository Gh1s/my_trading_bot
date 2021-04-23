import pandas as pd
from fbprophet import Prophet
import yfinance as yf
from config.bot_config import prophet_config, yahoo_config, config_yaml


yahoo_configuration = yahoo_config(config_yaml)
prophet_configuration = prophet_config(config_yaml)


def get_data():
    df = yf.download(
        tickers = yahoo_configuration.tickers,
        period = yahoo_configuration.period,
        interval = yahoo_configuration.interval,
        group_by = yahoo_configuration.group_by,
        auto_adjust = True,
        threads = True,
        proxy = None
    )
    df = df.dropna()
    df.index = df.index.strftime('%Y/%m/%d %H:%M:%S')
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
    future = m.make_future_dataframe(periods=prophet_configuration.predictions)
    frcst = m.predict(future)
    return frcst
