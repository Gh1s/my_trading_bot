import itertools
import numpy as np
import pandas as pd
import yfinance as yf
from prophet import Prophet
from prophet.diagnostics import performance_metrics
from prophet.diagnostics import cross_validation
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
    m = Prophet(changepoint_prior_scale=0.001, seasonality_prior_scale=10.0).fit(dt)
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

def get_best_parameters(df):
    param_grid = {
        'changepoint_prior_scale': [0.001, 0.01, 0.1, 0.5],
        'seasonality_prior_scale': [0.01, 0.1, 1.0, 10.0],
    }

    # Generate all combinations of parameters
    all_params = [dict(zip(param_grid.keys(), v)) for v in itertools.product(*param_grid.values())]
    rmses = []  # Store the RMSEs for each params here

    # Use cross validation to evaluate all parameters
    for params in all_params:
        m = Prophet(**params).fit(df)  # Fit model with given params
        df_cv = cross_validation(m, horizon='5 days', parallel="processes")
        df_p = performance_metrics(df_cv, rolling_window=1)
        rmses.append(df_p['rmse'].values[0])

    # Find the best parameters
    tuning_results = pd.DataFrame(all_params)
    tuning_results['rmse'] = rmses
    print(tuning_results)
    best_params = all_params[np.argmin(rmses)]
    return best_params